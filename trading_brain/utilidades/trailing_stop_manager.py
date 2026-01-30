import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

logger = logging.getLogger(__name__)

class TrailingStopManager:
    """Gestor de Trailing Stop automático para posiciones abiertas."""
    
    def __init__(self, binance_manager):
        self.bm = binance_manager
        self.posiciones_activas = {}  # symbol -> posición data
        self.historial_ajustes = []
        logger.info("✅ Trailing Stop Manager inicializado")
    
    def abrir_posicion(self, symbol: str, entry_price: float, stop_loss: float, 
                       take_profit: float, side: str, signal_id: int):
        """Registra una nueva posición para monitoreo."""
        posicion = {
            'symbol': symbol,
            'entry_price': entry_price,
            'current_sl': stop_loss,
            'original_sl': stop_loss,
            'take_profit': take_profit,
            'side': side.upper(),  # 'COMPRA' o 'VENTA'
            'signal_id': signal_id,
            'status': 'ACTIVA',
            'open_time': datetime.now(),
            'last_update': datetime.now(),
            'best_price': entry_price,
            'fase_trailing': 0,
            'ajustes_realizados': 0,
            'max_profit_pct': 0.0,
            'current_profit_pct': 0.0
        }
        
        self.posiciones_activas[symbol] = posicion
        logger.info(f"📈 Posición {symbol} registrada para trailing stop (SL: {stop_loss:.2f})")
        return posicion

    def obtener_precio_actual(self, symbol: str) -> Optional[float]:
        """Obtiene precio actual desde Binance."""
        try:
            if not self.bm:
                logger.warning(f"Sin Binance Manager para {symbol}")
                return None
            
            endpoint = "/fapi/v1/ticker/price"
            params = f"symbol={symbol}"
            
            response = self.bm._hacer_solicitud(endpoint, params)
            if isinstance(response, dict) and 'price' in response:
                return float(response['price'])
            return None
        except Exception as e:
            logger.error(f"Error obteniendo precio {symbol}: {e}")
            return None

    def calcular_trailing_stop(self, posicion: Dict, precio_actual: float) -> Optional[float]:
        """Calcula nuevo stop loss basado en trailing stop de 3 fases."""
        entry = posicion['entry_price']
        current_sl = posicion['current_sl']
        side = posicion['side']
        best_price = posicion['best_price']
        
        # Calcular ganancia actual
        if side == "COMPRA":
            profit_pct = ((precio_actual - entry) / entry) * 100
        else:  # VENTA
            profit_pct = ((entry - precio_actual) / entry) * 100
        
        posicion['current_profit_pct'] = profit_pct
        posicion['max_profit_pct'] = max(posicion['max_profit_pct'], profit_pct)
        
        # Actualizar mejor precio
        if side == "COMPRA" and precio_actual > best_price:
            posicion['best_price'] = precio_actual
        elif side == "VENTA" and precio_actual < best_price:
            posicion['best_price'] = precio_actual
        
        # TRAILING STOP DE 3 FASES
        nuevo_sl = current_sl
        nueva_fase = 0
        
        # FASE 1: 1-3% ganancia - Trailing muy ajustado
        if 1.0 <= profit_pct < 3.0:
            nueva_fase = 1
            if side == "COMPRA":
                # SL se mueve a entrada (break even)
                nuevo_sl = entry
            else:
                nuevo_sl = entry
        
        # FASE 2: 3-6% ganancia - Trailing medio
        elif 3.0 <= profit_pct < 6.0:
            nueva_fase = 2
            trailing_distance = 1.5  # 1.5% del precio
            if side == "COMPRA":
                nuevo_sl = precio_actual * (1 - trailing_distance/100)
            else:
                nuevo_sl = precio_actual * (1 + trailing_distance/100)
        
        # FASE 3: >6% ganancia - Trailing agresivo
        elif profit_pct >= 6.0:
            nueva_fase = 3
            trailing_distance = 0.8  # 0.8% del precio
            if side == "COMPRA":
                nuevo_sl = precio_actual * (1 - trailing_distance/100)
            else:
                nuevo_sl = precio_actual * (1 + trailing_distance/100)
        
        # Solo ajustar si el nuevo SL es mejor que el actual
        if side == "COMPRA" and nuevo_sl > current_sl:
            ajuste_valido = True
        elif side == "VENTA" and nuevo_sl < current_sl:
            ajuste_valido = True
        else:
            ajuste_valido = False
        
        if ajuste_valido and nueva_fase > posicion['fase_trailing']:
            posicion['fase_trailing'] = nueva_fase
            posicion['ajustes_realizados'] += 1
            return nuevo_sl
        
        return None

    def verificar_cierre_posicion(self, posicion: Dict, precio_actual: float) -> bool:
        """Verifica si la posición debe cerrarse por SL o TP."""
        symbol = posicion['symbol']
        side = posicion['side']
        current_sl = posicion['current_sl']
        take_profit = posicion['take_profit']
        
        # Verificar Stop Loss
        if side == "COMPRA" and precio_actual <= current_sl:
            logger.info(f"🔴 {symbol} alcanzó STOP LOSS ({current_sl:.2f})")
            return True, 'STOP_LOSS'
        elif side == "VENTA" and precio_actual >= current_sl:
            logger.info(f"🔴 {symbol} alcanzó STOP LOSS ({current_sl:.2f})")
            return True, 'STOP_LOSS'
        
        # Verificar Take Profit
        if side == "COMPRA" and precio_actual >= take_profit:
            logger.info(f"🟢 {symbol} alcanzó TAKE PROFIT ({take_profit:.2f})")
            return True, 'TAKE_PROFIT'
        elif side == "VENTA" and precio_actual <= take_profit:
            logger.info(f"🟢 {symbol} alcanzó TAKE PROFIT ({take_profit:.2f})")
            return True, 'TAKE_PROFIT'
        
        return False, None

    def monitorear_posiciones(self):
        """Monitorea y ajusta todas las posiciones activas."""
        if not self.posiciones_activas:
            return
        
        logger.info(f"🔍 Monitoreando {len(self.posiciones_activas)} posiciones...")
        
        for symbol, posicion in list(self.posiciones_activas.items()):
            try:
                # Obtener precio actual
                precio_actual = self.obtener_precio_actual(symbol)
                if not precio_actual:
                    continue
                
                # Verificar cierre
                debe_cerrar, razon = self.verificar_cierre_posicion(posicion, precio_actual)
                if debe_cerrar:
                    self.cerrar_posicion(symbol, razon, precio_actual)
                    continue
                
                # Calcular y aplicar trailing stop
                nuevo_sl = self.calcular_trailing_stop(posicion, precio_actual)
                if nuevo_sl:
                    # Aplicar nuevo stop loss
                    posicion['current_sl'] = nuevo_sl
                    posicion['last_update'] = datetime.now()
                    
                    # Registrar ajuste
                    ajuste = {
                        'symbol': symbol,
                        'timestamp': datetime.now(),
                        'old_sl': posicion['current_sl'],
                        'new_sl': nuevo_sl,
                        'precio_actual': precio_actual,
                        'fase': posicion['fase_trailing'],
                        'profit_pct': posicion['current_profit_pct']
                    }
                    self.historial_ajustes.append(ajuste)
                    
                    logger.info(f"📐 {symbol}: SL ajustado a {nuevo_sl:.2f} (Fase {posicion['fase_trailing']}, Profit: {posicion['current_profit_pct']:.1f}%)")
                
                # Actualizar posición
                self.posiciones_activas[symbol] = posicion
                
            except Exception as e:
                logger.error(f"Error monitoreando {symbol}: {e}")

    def cerrar_posicion(self, symbol: str, razon: str, precio_cierre: float):
        """Cierra una posición y la elimina del monitoreo."""
        if symbol not in self.posiciones_activas:
            return
        
        posicion = self.posiciones_activas.pop(symbol)
        
        # Calcular resultado final
        if posicion['side'] == "COMPRA":
            profit = precio_cierre - posicion['entry_price']
            profit_pct = (profit / posicion['entry_price']) * 100
        else:
            profit = posicion['entry_price'] - precio_cierre
            profit_pct = (profit / posicion['entry_price']) * 100
        
        resultado = {
            'symbol': symbol,
            'signal_id': posicion['signal_id'],
            'side': posicion['side'],
            'entry_price': posicion['entry_price'],
            'exit_price': precio_cierre,
            'profit': profit,
            'profit_pct': profit_pct,
            'razon_cierre': razon,
            'open_time': posicion['open_time'],
            'close_time': datetime.now(),
            'duration': (datetime.now() - posicion['open_time']).total_seconds() / 60,
            'ajustes_realizados': posicion['ajustes_realizados'],
            'max_profit_pct': posicion['max_profit_pct'],
            'fase_final': posicion['fase_trailing']
        }
        
        logger.info(f"🔒 {symbol} cerrada: {razon} | Profit: {profit_pct:.2f}%")
        return resultado

# Función helper para integración rápida
def crear_trailing_manager(binance_manager):
    """Crea y retorna instancia de TrailingStopManager."""
    return TrailingStopManager(binance_manager)

    def get_estado_posiciones(self) -> Dict:
        """Retorna estado de todas las posiciones."""
        estado = {
            'total_posiciones': len(self.posiciones_activas),
            'posiciones_activas': {},
            'resumen': {
                'total_ajustes': len(self.historial_ajustes),
                'posiciones_cerradas': 0,
                'ganancias_totales': 0
            }
        }
        
        for symbol, pos in self.posiciones_activas.items():
            estado['posiciones_activas'][symbol] = {
                'side': pos['side'],
                'entry_price': pos['entry_price'],
                'current_sl': pos['current_sl'],
                'take_profit': pos['take_profit'],
                'current_profit_pct': pos.get('current_profit_pct', 0),
                'max_profit_pct': pos.get('max_profit_pct', 0),
                'fase_trailing': pos['fase_trailing'],
                'ajustes': pos['ajustes_realizados'],
                'tiempo_abierta': (datetime.now() - pos['open_time']).total_seconds() / 60
            }
        
        return estado
