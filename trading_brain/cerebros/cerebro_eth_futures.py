import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroETHFutures(CerebroFuturesBase):
    """Cerebro para Ethereum con MACD, Bollinger Bands y OBV."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("ETHUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "macd_bollinger_obv"
        self.timeframe = "15m"
        logger.info(f"✅ Cerebro ETH inicializado - {self.nombre_estrategia}")
    
    def calcular_macd(self, datos, fast=12, slow=26, signal=9):
        """Calcula MACD."""
        exp1 = datos['close'].ewm(span=fast, adjust=False).mean()
        exp2 = datos['close'].ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd.iloc[-1], signal_line.iloc[-1], histogram.iloc[-1]
    
    def calcular_bollinger(self, datos, window=20, num_std=2):
        """Calcula Bollinger Bands."""
        rolling_mean = datos['close'].rolling(window=window).mean()
        rolling_std = datos['close'].rolling(window=window).std()
        upper = rolling_mean + (rolling_std * num_std)
        lower = rolling_mean - (rolling_std * num_std)
        return upper.iloc[-1], rolling_mean.iloc[-1], lower.iloc[-1]
    
    def calcular_obv(self, datos):
        """Calcula On-Balance Volume."""
        obv = [0]
        for i in range(1, len(datos)):
            if datos['close'].iloc[i] > datos['close'].iloc[i-1]:
                obv.append(obv[-1] + datos['volume'].iloc[i])
            elif datos['close'].iloc[i] < datos['close'].iloc[i-1]:
                obv.append(obv[-1] - datos['volume'].iloc[i])
            else:
                obv.append(obv[-1])
        return obv[-1]
    
    def analizar(self) -> Optional[Dict]:
        """Análisis ETH con MACD + Bollinger + OBV."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 30:
                return None
            
            precio = datos['close'].iloc[-1]
            
            # Calcular indicadores
            macd, signal, hist = self.calcular_macd(datos)
            bb_upper, bb_middle, bb_lower = self.calcular_bollinger(datos)
            obv = self.calcular_obv(datos)
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # COMPRA: MACD > Signal, precio > BB middle, OBV creciente
            if macd > signal and precio > bb_middle and obv > 0:
                direccion = "COMPRA"
                confianza = 0.75
                if precio < bb_upper and hist > 0:
                    confianza = 0.85
            
            # VENTA: MACD < Signal, precio < BB middle, OBV decreciente
            elif macd < signal and precio < bb_middle and obv < 0:
                direccion = "VENTA"
                confianza = 0.70
                if precio > bb_lower and hist < 0:
                    confianza = 0.80
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'macd': round(float(macd), 4),
                    'macd_signal': round(float(signal), 4),
                    'macd_hist': round(float(hist), 4),
                    'bb_upper': round(float(bb_upper), 4),
                    'bb_middle': round(float(bb_middle), 4),
                    'bb_lower': round(float(bb_lower), 4),
                    'obv': round(float(obv), 2),
                    'bb_width': round(((bb_upper - bb_lower) / bb_middle) * 100, 2)
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(precio * 0.985), 4) if direccion == "COMPRA" else round(float(precio * 1.015), 4),
                    'take_profit': round(float(precio * 1.03), 4) if direccion == "COMPRA" else round(float(precio * 0.97), 4)
                }
            }
            
            logger.info(f"{self.symbol}: {direccion} (MACD: {macd:.2f}, BB%: {((precio-bb_lower)/(bb_upper-bb_lower)*100):.1f}%)")
            return resultado
            
        except Exception as e:
            logger.error(f"Error ETH: {e}")
            return None
