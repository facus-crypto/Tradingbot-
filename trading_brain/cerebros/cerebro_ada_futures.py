import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroADAFutures(CerebroFuturesBase):
    """Cerebro para Cardano con Canal Donchian y RSI divergencias."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("ADAUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "canal_tendencia_rsi_div"
        self.timeframe = "15m"
        logger.info(f"✅ Cerebro ADA inicializado - {self.nombre_estrategia}")
    
    def calcular_donchian(self, datos, periodo=20):
        """Calcula Canal Donchian."""
        upper = datos['high'].rolling(window=periodo).max()
        lower = datos['low'].rolling(window=periodo).min()
        middle = (upper + lower) / 2
        return upper.iloc[-1], middle.iloc[-1], lower.iloc[-1]
    
    def calcular_rsi_divergencia(self, datos, periodo=14):
        """Busca divergencias RSI."""
        delta = datos['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Buscar divergencias simples
        if len(datos) >= 10:
            precios = datos['close'].tail(10).values
            rsi_vals = rsi.tail(10).values
            
            # Máximos/mínimos recientes
            precio_max_idx = precios.argmax()
            precio_min_idx = precios.argmin()
            
            divergencia = "NONE"
            if precio_max_idx >= 5:  # Máximo reciente
                if precios[-1] > precios[-6] and rsi_vals[-1] < rsi_vals[-6]:
                    divergencia = "BAJISTA"
                elif precios[-1] < precios[-6] and rsi_vals[-1] > rsi_vals[-6]:
                    divergencia = "ALCISTA"
            
            return rsi.iloc[-1], divergencia
        
        return rsi.iloc[-1], "NONE"
    
    def analizar(self) -> Optional[Dict]:
        """Análisis ADA con Canal Donchian y RSI divergencias."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 30:
                return None
            
            precio = datos['close'].iloc[-1]
            don_upper, don_middle, don_lower = self.calcular_donchian(datos)
            rsi, divergencia = self.calcular_rsi_divergencia(datos)
            
            # Posición en canal
            canal_width = don_upper - don_lower
            if canal_width > 0:
                posicion_canal = (precio - don_lower) / canal_width
            else:
                posicion_canal = 0.5
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # COMPRA: Precio cerca parte inferior canal, RSI divergencia alcista
            if posicion_canal < 0.3 and divergencia == "ALCISTA":
                direccion = "COMPRA"
                confianza = 0.75
            
            # VENTA: Precio cerca parte superior canal, RSI divergencia bajista
            elif posicion_canal > 0.7 and divergencia == "BAJISTA":
                direccion = "VENTA"
                confianza = 0.70
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'donchian_upper': round(float(don_upper), 4),
                    'donchian_middle': round(float(don_middle), 4),
                    'donchian_lower': round(float(don_lower), 4),
                    'canal_position': round(posicion_canal * 100, 1),
                    'rsi': round(float(rsi), 2),
                    'rsi_divergencia': divergencia,
                    'canal_width': round(canal_width, 4)
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(don_lower * 0.995), 4) if direccion == "COMPRA" else round(float(don_upper * 1.005), 4),
                    'take_profit': round(float(don_middle), 4) if direccion == "COMPRA" else round(float(don_middle), 4)
                }
            }
            
            logger.info(f"{self.symbol}: {direccion} (Canal: {posicion_canal*100:.1f}%, RSI: {rsi:.1f}, Div: {divergencia})")
            return resultado
            
        except Exception as e:
            logger.error(f"Error ADA: {e}")
            return None
