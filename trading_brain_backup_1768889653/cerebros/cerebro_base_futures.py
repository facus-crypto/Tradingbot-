"""
Clase base para cerebros con integración Binance Futures
"""
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
from utilidades.validador_historico import ValidadorHistorico
import sys
import os

sys.path.append('.')

logger = logging.getLogger(__name__)

class CerebroFuturesBase:
    """Clase base para todos los cerebros con integración Futures"""
    
    def __init__(self, symbol: str, binance_manager=None, telegram_bot=None):
        """
        Inicializa el cerebro base
        
        Args:
            symbol: Símbolo de trading (ej: BTCUSDT)
            binance_manager: Instancia de BinanceFuturesManager
            telegram_bot: Instancia de TelegramAdvancedBot
        """
        self.symbol = symbol
        self.binance = binance_manager
        self.telegram = telegram_bot
        self.estrategia = "base"
        self.ultima_senal = None
        self.estado = "INACTIVO"
        self.historial_señales = []
        self.max_señales_diarias = 3
        
        # Configuración específica de Futures
        self.validador = ValidadorHistorico(binance_manager)  # Nuevo validador histórico
        self.leverage = 2
        print(f"[{self.symbol}] ✅ Validador histórico inicializado")
        self.position_percent = 0.25  # 25% del capital
        self.risk_per_trade = 0.02  # 2% máximo por trade
        
        # Parámetros de la estrategia
        self.timeframe = "15m"  # Timeframe por defecto
        self.min_confidence = 0.7  # 70% confianza mínima
        
        logger.info(f"🧠 Cerebro base inicializado para {symbol}")
    
    async def obtener_datos_binance(self, limit: int = 100) -> Optional[List[Dict]]:
        """
        Obtiene datos OHLCV de Binance para el símbolo
        
        Args:
            limit: Número de velas a obtener
            
        Returns:
            Lista de velas o None si hay error
        """
        if not self.binance:
            logger.error(f"No hay conexión Binance para {self.symbol}")
            return None
        
        try:
            # En producción real, esto se conectaría a la API de Binance
            # Por ahora simulamos con datos de prueba
            
            # Simulación de datos OHLCV
            import random
            import time
            
            datos = []
            precio_base = await self.obtener_precio_actual()
            
            if not precio_base or precio_base == 0:
                logger.error(f"No se pudo obtener precio para {self.symbol}")
                return None
            
            # Generar datos históricos simulados
            for i in range(limit):
                timestamp = int((time.time() - (i * 900)) * 1000)  # 15m intervals
                open_price = precio_base * (1 + random.uniform(-0.02, 0.02))
                high_price = open_price * (1 + random.uniform(0, 0.01))
                low_price = open_price * (1 - random.uniform(0, 0.01))
                close_price = random.uniform(low_price, high_price)
                volume = random.uniform(100, 1000)
                
                datos.append({
                    'timestamp': timestamp,
                    'open': open_price,
                    'high': high_price,
                    'low': low_price,
                    'close': close_price,
                    'volume': volume,
                    'symbol': self.symbol
                })
            
            logger.debug(f"Obtenidos {len(datos)} velas simuladas para {self.symbol}")
            return datos
            
        except Exception as e:
            logger.error(f"Error obteniendo datos para {self.symbol}: {e}")
            return None
    
    async def obtener_precio_actual(self) -> Optional[float]:
        """
        Obtiene el precio actual del símbolo desde Binance
        
        Returns:
            Precio actual o None si hay error
        """
        if not self.binance:
            logger.error(f"No hay conexión Binance para {self.symbol}")
            return None
        
        try:
            precio = self.binance.get_symbol_price(self.symbol)
            if precio and precio > 0:
                logger.debug(f"Precio actual {self.symbol}: {precio:.2f}")
                return precio
            else:
                logger.error(f"Precio inválido para {self.symbol}: {precio}")
                return None
                
        except Exception as e:
            logger.error(f"Error obteniendo precio de {self.symbol}: {e}")
            return None
    
    def calcular_stop_loss_take_profit(self, entry_price: float, 
                                      direction: str) -> Tuple[float, float]:
        """
        Calcula SL y TP basado en la estrategia y volatilidad
        
        Args:
            entry_price: Precio de entrada
            direction: "LONG" o "SHORT"
            
        Returns:
            (stop_loss, take_profit)
        """
        # Por defecto: SL 2%, TP 4% (relación riesgo:beneficio 1:2)
        sl_percent = 0.02
        tp_percent = 0.04
        
        if direction == "LONG":
            stop_loss = entry_price * (1 - sl_percent)
            take_profit = entry_price * (1 + tp_percent)
        else:  # SHORT
            stop_loss = entry_price * (1 + sl_percent)
            take_profit = entry_price * (1 - tp_percent)
        
        # Redondear a 2 decimales para mayoría de símbolos
        stop_loss = round(stop_loss, 2)
        take_profit = round(take_profit, 2)
        
        logger.debug(f"Cálculo SL/TP para {self.symbol} {direction}: "
                    f"Entry={entry_price:.2f}, SL={stop_loss:.2f}, TP={take_profit:.2f}")
        
        return stop_loss, take_profit
    
    def generar_senal(self, datos: List[Dict], 
                     precio_actual: float) -> Optional[Dict]:
        """
        Método base para generar señales (debe ser sobrescrito)
        
        Args:
            datos: Datos OHLCV históricos
            precio_actual: Precio actual del símbolo
            
        Returns:
            Dict con señal o None si no hay señal
        """
        # Este método debe ser implementado por cada cerebro específico
        raise NotImplementedError("Cada cerebro debe implementar su propia lógica")
    
    async def analizar(self) -> Optional[Dict]:
        """
        Ejecuta el análisis completo y genera señal si corresponde
        
        Returns:
            Señal generada o None
        """
        try:
            logger.info(f"🔍 {self.symbol} - Iniciando análisis...")
            self.estado = "ANALIZANDO"
            
            # 1. Obtener datos de Binance
            datos = await self.obtener_datos_binance(limit=50)
            if not datos:
                logger.error(f"No se pudieron obtener datos para {self.symbol}")
                self.estado = "ERROR_DATOS"
                return None
            
            # 2. Obtener precio actual
            precio_actual = await self.obtener_precio_actual()
            if not precio_actual:
                logger.error(f"No se pudo obtener precio actual para {self.symbol}")
                self.estado = "ERROR_PRECIO"
                return None
            
            # 3. Generar señal usando la estrategia específica
            senal = self.generar_senal(datos, precio_actual)
            
            if senal:
                # 4. Calcular SL y TP
                sl, tp = self.calcular_stop_loss_take_profit(
                    senal['entry_price'],
                    senal['action']
                )
                
                senal_completa = {
                    'symbol': self.symbol,
                    'action': senal['action'],
                    'confidence': senal['confidence'],
                    'entry_price': senal['entry_price'],
                    'stop_loss': sl,
                    'take_profit': tp,
                    'timestamp': datetime.now().isoformat(),
                    'cerebro_name': self.__class__.__name__,
                    'estrategia': self.estrategia,
                    'timeframe': self.timeframe,
                    'razones': senal.get('razones', []),
                    'indicadores': senal.get('indicadores', {})
                }
                
                # 5. Validar señal
                if self.validar_senal(senal_completa):
                    self.ultima_senal = senal_completa
                    self.historial_señales.append(senal_completa)
                    self.estado = "SEÑAL_GENERADA"
                    
                    logger.info(f"✅ {self.symbol} - Señal generada: "
                               f"{senal_completa['action']} "
                               f"(Conf: {senal_completa['confidence']:.0%})")
                    
                    return senal_completa
                else:
                    logger.info(f"⚠️  {self.symbol} - Señal no superó validación")
                    self.estado = "SEÑAL_RECHAZADA"
                    return None
            else:
                logger.info(f"ℹ️  {self.symbol} - No hay señal en este ciclo")
                self.estado = "SIN_SEÑAL"
                return None
                
        except Exception as e:
            logger.error(f"❌ {self.symbol} - Error en análisis: {e}")
            self.estado = "ERROR"
            return None
    
    def validar_senal(self, senal: Dict) -> bool:
        """
        Valida una señal antes de enviarla
        
        Args:
            senal: Señal a validar
            
        Returns:
            True si la señal es válida
        """
        # 1. Confianza mínima
        if senal['confidence'] < self.min_confidence:
            logger.debug(f"Señal rechazada: confianza {senal['confidence']:.0%} < {self.min_confidence:.0%}")
            return False
        
        # 2. Validar SL/TP
        if senal['action'] == "LONG":
            if senal['stop_loss'] >= senal['entry_price']:
                logger.debug(f"Señal rechazada: SL {senal['stop_loss']} >= Entry {senal['entry_price']}")
                return False
            if senal['take_profit'] <= senal['entry_price']:
                logger.debug(f"Señal rechazada: TP {senal['take_profit']} <= Entry {senal['entry_price']}")
                return False
        else:  # SHORT
            if senal['stop_loss'] <= senal['entry_price']:
                logger.debug(f"Señal rechazada: SL {senal['stop_loss']} <= Entry {senal['entry_price']}")
                return False
            if senal['take_profit'] >= senal['entry_price']:
                logger.debug(f"Señal rechazada: TP {senal['take_profit']} >= Entry {senal['entry_price']}")
                return False
        
        # 3. Límite de señales diarias
        señales_hoy = [s for s in self.historial_señales 
                      if datetime.fromisoformat(s['timestamp']).date() == datetime.now().date()]
        
        if len(señales_hoy) >= self.max_señales_diarias:
            logger.debug(f"Señal rechazada: límite diario alcanzado ({self.max_señales_diarias})")
            return False
        
        return True
    
    async def procesar_senal(self, senal: Dict) -> Dict:
        """
        Procesa una señal generada (envía a Telegram, etc.)
        
        Args:
            senal: Señal a procesar
            
        Returns:
            Resultado del procesamiento
        """
        try:
            if self.telegram:
                # Enviar señal a Telegram con botones
                message_id = await self.telegram.send_signal(senal)
                
                if message_id:
                    logger.info(f"📤 {self.symbol} - Señal enviada a Telegram (ID: {message_id})")
                    
                    return {
                        'status': 'sent_to_telegram',
                        'message_id': message_id,
                        'signal': senal,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    logger.error(f"❌ {self.symbol} - Error enviando señal a Telegram")
                    return {
                        'status': 'telegram_error',
                        'signal': senal,
                        'error': 'No se pudo enviar a Telegram'
                    }
            else:
                logger.warning(f"⚠️  {self.symbol} - No hay bot de Telegram, señal no enviada")
                return {
                    'status': 'no_telegram',
                    'signal': senal,
                    'warning': 'Bot de Telegram no configurado'
                }
                
        except Exception as e:
            logger.error(f"❌ {self.symbol} - Error procesando señal: {e}")
            return {
                'status': 'error',
                'signal': senal,
                'error': str(e)
            }
    
    def get_estado(self) -> Dict:
        """Devuelve el estado actual del cerebro"""
        return {
            'symbol': self.symbol,
            'estado': self.estado,
            'estrategia': self.estrategia,
            'ultima_senal': self.ultima_senal,
            'señales_hoy': len([s for s in self.historial_señales 
                              if datetime.fromisoformat(s['timestamp']).date() == datetime.now().date()]),
            'señales_totales': len(self.historial_señales),
            'config': {
                'leverage': self.leverage,
                'position_percent': self.position_percent,
                'risk_per_trade': self.risk_per_trade,
                'min_confidence': self.min_confidence,
                'timeframe': self.timeframe
            }
        }
    def calcular_trailing_directo(self, precio_entrada, precio_actual, ganancia_actual=None):
        """
        Calcula trailing stop con tres fases (mismo que XRP)
        
        Fases:
        1. INICIAL: Ganancia <= 1%
           - SL: 2% bajo entrada
           - TP: 3% sobre entrada
           
        2. TRAILING: Ganancia entre 1% y 7%
           - SL: 0.5% bajo precio actual  
           - TP: 2% sobre precio actual
           
        3. BLOQUEO: Ganancia >= 7%
           - SL: 0.25% bajo precio actual
           - TP: 1% sobre precio actual
           
        Args:
            precio_entrada (float): Precio de entrada
            precio_actual (float): Precio actual del mercado
            ganancia_actual (float, optional): Ganancia actual en decimal
            
        Returns:
            tuple: (sl_price, tp_price, fase_name)
        """
        # Calcular ganancia si no se proporciona
        if ganancia_actual is None:
            ganancia_actual = (precio_actual - precio_entrada) / precio_entrada
        
        # Umbrales de fase
        UMBRAL_INICIAL = 0.01      # 1%
        UMBRAL_BLOQUEO = 0.07      # 7%
        
        # FASE 1: INICIAL (ganancia <= 1%)
        if ganancia_actual <= UMBRAL_INICIAL:
            fase = "INICIAL"
            sl = precio_entrada * (1 - 0.02)  # -2%
            tp = precio_entrada * (1 + 0.03)  # +3%
        
        # FASE 2: TRAILING (ganancia entre 1% y 7%)  
        elif ganancia_actual < UMBRAL_BLOQUEO:
            fase = "TRAILING"
            sl = precio_actual * (1 - 0.005)  # -0.5%
            tp = precio_actual * (1 + 0.02)   # +2%
        
        # FASE 3: BLOQUEO (ganancia >= 7%)
        else:
            fase = "BLOQUEO"
            sl = precio_actual * (1 - 0.0025)  # -0.25%
            tp = precio_actual * (1 + 0.01)    # +1%
        
        return sl, tp, fase

if __name__ == "__main__":
    # Prueba básica de la clase base
    logging.basicConfig(level=logging.INFO)
    
    print("🧠 PRUEBA CEREBRO BASE FUTURES")
    print("=" * 50)
    
    cerebro = CerebroFuturesBase("BTCUSDT")
    
    estado = cerebro.get_estado()
    print(f"✅ Cerebro base creado para: {estado['symbol']}")
    print(f"   Estrategia: {estado['estrategia']}")
    print(f"   Estado: {estado['estado']}")
    print(f"   Configuración Futures:")
    print(f"     • Leverage: {estado['config']['leverage']}X")
    print(f"     • Posición: {estado['config']['position_percent']*100}%")
    print(f"     • Riesgo por trade: {estado['config']['risk_per_trade']*100}%")
    
    print("\n" + "=" * 50)
