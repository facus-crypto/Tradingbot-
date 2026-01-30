import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroXRPFutures(CerebroFuturesBase):
    """Cerebro para XRP con Bollinger Bands Squeeze."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("XRPUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "bandas_bollinger_squeeze"
        self.timeframe = "15m"
        logger.info(f"✅ Cerebro XRP inicializado - {self.nombre_estrategia}")
    
    def calcular_bollinger_squeeze(self, datos, window=20, num_std=2):
        """Calcula Bollinger Bands y detección de squeeze."""
        rolling_mean = datos['close'].rolling(window=window).mean()
        rolling_std = datos['close'].rolling(window=window).std()
        
        upper = rolling_mean + (rolling_std * num_std)
        lower = rolling_mean - (rolling_std * num_std)
        
        # Band Width (ancho de las bandas)
        band_width = (upper - lower) / rolling_mean
        
        # %B Indicator (posición del precio dentro de las bandas)
        percent_b = (datos['close'] - lower) / (upper - lower)
        
        return {
            'upper': upper.iloc[-1],
            'middle': rolling_mean.iloc[-1],
            'lower': lower.iloc[-1],
            'band_width': band_width.iloc[-1],
            'percent_b': percent_b.iloc[-1],
            'std': rolling_std.iloc[-1]
        }
    
    def analizar(self) -> Optional[Dict]:
        """Análisis XRP con Bollinger Squeeze."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 30:
                return None
            
            precio = datos['close'].iloc[-1]
            bb = self.calcular_bollinger_squeeze(datos)
            
            # Detectar squeeze (bandas muy estrechas)
            squeeze_threshold = 0.05  # 5% de ancho
            is_squeeze = bb['band_width'] < squeeze_threshold
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # COMPRA: Salida de squeeze + precio sobre banda media + %B > 0.5
            if is_squeeze and precio > bb['middle'] and bb['percent_b'] > 0.5:
                direccion = "COMPRA"
                confianza = 0.72
                if bb['percent_b'] > 0.7:
                    confianza = 0.82
            
            # VENTA: Salida de squeeze + precio bajo banda media + %B < 0.5
            elif is_squeeze and precio < bb['middle'] and bb['percent_b'] < 0.5:
                direccion = "VENTA"
                confianza = 0.68
                if bb['percent_b'] < 0.3:
                    confianza = 0.78
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'bb_upper': round(float(bb['upper']), 4),
                    'bb_middle': round(float(bb['middle']), 4),
                    'bb_lower': round(float(bb['lower']), 4),
                    'band_width': round(float(bb['band_width'] * 100), 2),  # en porcentaje
                    'percent_b': round(float(bb['percent_b'] * 100), 1),    # en porcentaje
                    'squeeze': is_squeeze,
                    'volatilidad': round(float(bb['std']), 4)
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(bb['lower'] * 0.995), 4) if direccion == "COMPRA" else round(float(bb['upper'] * 1.005), 4),
                    'take_profit': round(float(bb['upper'] * 0.995), 4) if direccion == "COMPRA" else round(float(bb['lower'] * 1.005), 4)
                }
            }
            
            estado = "SQUEEZE" if is_squeeze else "NORMAL"
            logger.info(f"{self.symbol}: {direccion} ({estado}, %B: {bb['percent_b']*100:.1f}%, Width: {bb['band_width']*100:.2f}%)")
            return resultado
            
        except Exception as e:
            logger.error(f"Error XRP: {e}")
            return None
