"""
RISK MANAGER - Gestión de riesgo institucional
Calcula tamaño de posición, stops y exposición.
"""
import logging
from typing import Dict, Optional, Tuple
from decimal import Decimal, ROUND_DOWN
import requests

logger = logging.getLogger(__name__)

class RiskManager:
    """Gestiona riesgo, posición size y stops"""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.config = {
            "porcentaje_por_operacion": 0.25,  # 25% de la wallet
            "apalancamiento": 2,               # Apalancamiento x2
            "stop_loss_porcentaje": 0.02,      # 2% máximo por operación
            "max_operaciones_simultaneas": 3,
            "risk_reward_minimo": 1.5,         # Mínimo 1.5:1
            "max_riesgo_diario": 0.05,         # 5% máximo diario
        }
        
        # Estadísticas
        self.riesgo_acumulado_hoy = 0.0
        self.operaciones_hoy = 0
        
        logger.info("🛡️  RISK MANAGER INICIADO - Configuración institucional")
    
    def obtener_balance_binance(self) -> Optional[Dict]:
        """Obtiene balance actual de Binance (Futures)"""
        try:
            # URL para Futures balance
            url = "https://fapi.binance.com/fapi/v2/balance"
            
            # Para una implementación real necesitarías firmar la request
            # Esta es una versión simplificada para la estructura
            headers = {}
            if self.api_key:
                headers["X-MBX-APIKEY"] = self.api_key
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                balances = response.json()
                # Filtrar solo balances con fondos
                balances_con_fondos = [
                    bal for bal in balances 
                    if float(bal.get('balance', 0)) > 0 or float(bal.get('availableBalance', 0)) > 0
                ]
                return {"balances": balances_con_fondos, "total": len(balances_con_fondos)}
            else:
                logger.error(f"Error API Binance: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error obteniendo balance: {e}")
            # Modo simulación para desarrollo
            return self.simular_balance()
    
    def simular_balance(self) -> Dict:
        """Simula balance para desarrollo (remover en producción)"""
        logger.warning("⚠️  Usando balance simulado para desarrollo")
        
        return {
            "balances": [
                {"asset": "USDT", "balance": "10000.0", "availableBalance": "10000.0"},
                {"asset": "BTC", "balance": "0.1", "availableBalance": "0.1"},
            ],
            "total": 2,
            "simulado": True
        }
    
    def obtener_precio_actual(self, simbolo: str) -> Optional[float]:
        """Obtiene precio actual de un símbolo"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/price"
            params = {"symbol": simbolo}
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return float(data.get('price', 0))
            
        except Exception as e:
            logger.error(f"Error obteniendo precio de {simbolo}: {e}")
            return None
    
    def calcular_tamano_posicion(self, simbolo: str, precio_entrada: float, 
                                stop_loss: float, balance_usdt: float) -> Dict:
        """
        Calcula tamaño de posición según reglas institucionales:
        1. 25% de la wallet por operación
        2. Apalancamiento x2
        3. Stop-loss del 2%
        4. Risk-Reward mínimo 1.5:1
        """
        try:
            # 1. Capital disponible para esta operación (25% del balance)
            capital_disponible = balance_usdt * self.config["porcentaje_por_operacion"]
            
            # 2. Exposición con apalancamiento
            exposicion_maxima = capital_disponible * self.config["apalancamiento"]
            
            # 3. Calcular riesgo por unidad (precio_entrada - stop_loss)
            riesgo_por_unidad = abs(precio_entrada - stop_loss)
            if riesgo_por_unidad == 0:
                logger.error("Stop-loss igual a precio de entrada")
                return {"error": "Stop-loss inválido"}
            
            # 4. Riesgo máximo por operación (2% del capital TOTAL)
            riesgo_maximo = balance_usdt * self.config["stop_loss_porcentaje"]
            
            # 5. Calcular cantidad basada en riesgo
            cantidad_por_riesgo = riesgo_maximo / riesgo_por_unidad
            
            # 6. Calcular cantidad basada en exposición
            cantidad_por_exposicion = exposicion_maxima / precio_entrada
            
            # 7. Tomar el MÍNIMO entre riesgo y exposición (más conservador)
            cantidad_final = min(cantidad_por_riesgo, cantidad_por_exposicion)
            
            # 8. Asegurar que no exceda la exposición máxima
            valor_posicion = cantidad_final * precio_entrada
            if valor_posicion > exposicion_maxima:
                cantidad_final = exposicion_maxima / precio_entrada
            
            # 9. Redondear según reglas de Binance
            cantidad_final = self.redondear_cantidad_binance(simbolo, cantidad_final)
            
            # 10. Calcular Take Profit basado en risk-reward
            risk_reward = self.config["risk_reward_minimo"]
            if precio_entrada > stop_loss:  # LONG
                take_profit = precio_entrada + (riesgo_por_unidad * risk_reward)
            else:  # SHORT
                take_profit = precio_entrada - (riesgo_por_unidad * risk_reward)
            
            # 11. Verificar riesgo diario acumulado
            riesgo_operacion = cantidad_final * riesgo_por_unidad
            riesgo_diario_total = self.riesgo_acumulado_hoy + riesgo_operacion
            
            if riesgo_diario_total > (balance_usdt * self.config["max_riesgo_diario"]):
                logger.warning(f"Riesgo diario excedido: {riesgo_diario_total:.2f} > "
                              f"{balance_usdt * self.config['max_riesgo_diario']:.2f}")
                cantidad_final = 0  # No operar
            
            # Resultados
            resultados = {
                "cantidad": round(float(cantidad_final), 6),
                "valor_posicion": round(float(cantidad_final * precio_entrada), 2),
                "exposicion_real": round(float(cantidad_final * precio_entrada), 2),
                "riesgo_operacion": round(float(riesgo_operacion), 2),
                "riesgo_porcentaje": round(float((riesgo_operacion / balance_usdt) * 100), 2),
                "stop_loss": round(float(stop_loss), 2),
                "take_profit": round(float(take_profit), 2),
                "risk_reward_actual": round(float(risk_reward), 2),
                "balance_usado": round(float(capital_disponible), 2),
                "balance_total": round(float(balance_usdt), 2),
                "aprobado": cantidad_final > 0
            }
            
            logger.info(f"📊 Cálculo de posición para {simbolo}:")
            logger.info(f"   • Cantidad: {resultados['cantidad']} {simbolo.replace('USDT', '')}")
            logger.info(f"   • Valor: ${resultados['valor_posicion']}")
            logger.info(f"   • Riesgo: ${resultados['riesgo_operacion']} ({resultados['riesgo_porcentaje']}%)")
            logger.info(f"   • Stop: ${resultados['stop_loss']}")
            logger.info(f"   • TP: ${resultados['take_profit']}")
            
            return resultados
            
        except Exception as e:
            logger.error(f"Error calculando tamaño de posición: {e}", exc_info=True)
            return {"error": str(e)}
    
    def redondear_cantidad_binance(self, simbolo: str, cantidad: float) -> float:
        """Redondea cantidad según reglas de lot size de Binance"""
        # Reglas de redondeo según símbolo (simplificado)
        # En producción, obtener de https://api.binance.com/api/v3/exchangeInfo
        reglas_lot_size = {
            "BTCUSDT": 0.001,  # Step size: 0.001 BTC
            "ETHUSDT": 0.01,   # Step size: 0.01 ETH
            "SOLUSDT": 0.1,    # Step size: 0.1 SOL
            "LINKUSDT": 0.1,   # Step size: 0.1 LINK
            "BNBUSDT": 0.01,   # Step size: 0.01 BNB
        }
        
        step = reglas_lot_size.get(simbolo, 0.001)
        
        # Redondear hacia abajo al step más cercano
        cantidad_redondeada = (cantidad // step) * step
        
        # Mínimo 0.001 (o el step)
        if cantidad_redondeada < step:
            cantidad_redondeada = step
        
        return round(cantidad_redondeada, 6)
    
    def calcular_stop_loss_auto(self, simbolo: str, direccion: str, 
                               precio_entrada: float, atr: Optional[float] = None) -> float:
        """Calcula stop-loss automático basado en volatilidad"""
        try:
            # Si tenemos ATR (Average True Range), usarlo
            if atr and atr > 0:
                distancia = atr * 1.5  # 1.5x ATR
            else:
                # Distancia basada en porcentaje configurado
                distancia = precio_entrada * self.config["stop_loss_porcentaje"]
            
            if direccion.upper() == "LONG":
                stop_loss = precio_entrada - distancia
                # Asegurar que no sea menor que un mínimo razonable
                stop_loss = max(stop_loss, precio_entrada * 0.95)  # Máximo 5% de stop
            else:  # SHORT
                stop_loss = precio_entrada + distancia
                stop_loss = min(stop_loss, precio_entrada * 1.05)  # Máximo 5% de stop
            
            return round(stop_loss, 2)
            
        except Exception as e:
            logger.error(f"Error calculando stop-loss: {e}")
            # Fallback: porcentaje fijo
            if direccion.upper() == "LONG":
                return round(precio_entrada * 0.98, 2)  # -2%
            else:
                return round(precio_entrada * 1.02, 2)  # +2%
    
    def verificar_riesgo_diario(self, balance_usdt: float) -> bool:
        """Verifica si se puede operar según riesgo diario acumulado"""
        riesgo_maximo_diario = balance_usdt * self.config["max_riesgo_diario"]
        
        if self.riesgo_acumulado_hoy >= riesgo_maximo_diario:
            logger.warning(f"⚠️  Riesgo diario excedido: {self.riesgo_acumulado_hoy:.2f} >= {riesgo_maximo_diario:.2f}")
            return False
        
        riesgo_disponible = riesgo_maximo_diario - self.riesgo_acumulado_hoy
        logger.info(f"📅 Riesgo diario: {self.riesgo_acumulado_hoy:.2f}/{riesgo_maximo_diario:.2f} "
                   f"(Disponible: ${riesgo_disponible:.2f})")
        
        return True
    
    def registrar_operacion(self, riesgo: float, resultado: Optional[str] = None):
        """Registra una operación para tracking de riesgo diario"""
        self.riesgo_acumulado_hoy += riesgo
        self.operaciones_hoy += 1
        
        logger.info(f"📝 Operación registrada: Riesgo +${riesgo:.2f} "
                   f"(Total hoy: ${self.riesgo_acumulado_hoy:.2f})")
    
    def reset_riesgo_diario(self):
        """Resetea el riesgo diario (ejecutar a medianoche)"""
        logger.info(f"🔄 Reseteando riesgo diario: {self.riesgo_acumulado_hoy:.2f} → 0")
        self.riesgo_acumulado_hoy = 0.0
        self.operaciones_hoy = 0
    
    def get_estado(self) -> Dict:
        """Devuelve estado actual del risk manager"""
        return {
            "riesgo_acumulado_hoy": round(self.riesgo_acumulado_hoy, 2),
            "operaciones_hoy": self.operaciones_hoy,
            "config": self.config,
            "puede_operar": self.riesgo_acumulado_hoy < (10000 * self.config["max_riesgo_diario"])  # Asume $10k balance
        }

# Prueba del risk manager
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Crear risk manager
    rm = RiskManager()
    
    # Simular cálculo de posición
    print("\n🧪 PRUEBA RISK MANAGER")
    print("=" * 50)
    
    # Balance simulado
    balance_usdt = 10000.0
    simbolo = "BTCUSDT"
    precio_entrada = 50000.0
    stop_loss = 49000.0  # -2%
    
    print(f"💰 Balance: ${balance_usdt:.2f}")
    print(f"📈 {simbolo} a ${precio_entrada:.2f}")
    print(f"🛑 Stop-loss: ${stop_loss:.2f}")
    print(f"📏 Config: {rm.config['porcentaje_por_operacion']*100}% wallet, "
          f"x{rm.config['apalancamiento']} leverage, {rm.config['stop_loss_porcentaje']*100}% max riesgo")
    
    # Calcular posición
    resultado = rm.calcular_tamano_posicion(simbolo, precio_entrada, stop_loss, balance_usdt)
    
    if "error" not in resultado:
        print("\n✅ RESULTADO DEL CÁLCULO:")
        for key, value in resultado.items():
            if key != "aprobado" or value:
                print(f"   • {key.replace('_', ' ').title()}: {value}")
        
        if resultado["aprobado"]:
            print("\n🟢 POSICIÓN APROBADA - Lista para ejecutar")
        else:
            print("\n🔴 POSICIÓN RECHAZADA - Excede límites de riesgo")
    else:
        print(f"\n❌ Error: {resultado['error']}")
