import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroATOMFutures(CerebroFuturesBase):
    """Cerebro para Cosmos con Soporte/Resistencia dinámicos y ADX."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("ATOMUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "soporte_resistencia_adx"
        self.timeframe = "1h"
        logger.info(f"✅ Cerebro ATOM inicializado - {self.nombre_estrategia}")
    
    def calcular_soportes_resistencias(self, datos, window=20):
        """Calcula soportes y resistencias dinámicos."""
        # Pivot Points clásicos
        high = datos['high'].rolling(window=window).max()
        low = datos['low'].rolling(window=window).min()
        close = datos['close']
        
        # Pivot Point
        pp = (high + low + close) / 3
        
        # Soporte y resistencia
        r1 = (2 * pp) - low
        s1 = (2 * pp) - high
        r2 = pp + (high - low)
        s2 = pp - (high - low)
        
        return {
            'pivot': pp.iloc[-1],
            'r1': r1.iloc[-1],
            'r2': r2.iloc[-1],
            's1': s1.iloc[-1],
            's2': s2.iloc[-1],
            'high': high.iloc[-1],
            'low': low.iloc[-1]
        }
    
    def calcular_adx(self, datos, periodo=14):
        """Calcula ADX (Average Directional Index)."""
        high, low, close = datos['high'], datos['low'], datos['close']
        
        # True Range
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Directional Movement
        up_move = high - high.shift()
        down_move = low.shift() - low
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        plus_di = 100 * (pd.Series(plus_dm).rolling(periodo).mean() / tr.rolling(periodo).mean())
        minus_di = 100 * (pd.Series(minus_dm).rolling(periodo).mean() / tr.rolling(periodo).mean())
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(periodo).mean()
        
        return {
            'adx': adx.iloc[-1],
            'plus_di': plus_di.iloc[-1],
            'minus_di': minus_di.iloc[-1]
        }
    
    def analizar(self) -> Optional[Dict]:
        """Análisis ATOM con S/R + ADX."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 30:
                return None
            
            precio = datos['close'].iloc[-1]
            sr = self.calcular_soportes_resistencias(datos)
            adx_data = self.calcular_adx(datos)
            
            # Determinar zona de precio
            zona = "NEUTRAL"
            if precio >= sr['r1']:
                zona = "RESISTENCIA_FUERTE"
            elif precio <= sr['s1']:
                zona = "SOPORTE_FUERTE"
            elif sr['s1'] < precio < sr['r1']:
                zona = "RANGO_MEDIO"
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # COMPRA: Precio cerca de soporte + ADX > 25 (tendencia) + +DI > -DI
            if (abs(precio - sr['s1']) / sr['s1'] < 0.02 and 
                adx_data['adx'] > 25 and 
                adx_data['plus_di'] > adx_data['minus_di']):
                direccion = "COMPRA"
                confianza = 0.75
                if abs(precio - sr['s2']) / sr['s2'] < 0.02:
                    confianza = 0.85
            
            # VENTA: Precio cerca de resistencia + ADX > 25 + -DI > +DI
            elif (abs(precio - sr['r1']) / sr['r1'] < 0.02 and 
                  adx_data['adx'] > 25 and 
                  adx_data['minus_di'] > adx_data['plus_di']):
                direccion = "VENTA"
                confianza = 0.70
                if abs(precio - sr['r2']) / sr['r2'] < 0.02:
                    confianza = 0.80
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'pivot': round(float(sr['pivot']), 4),
                    'r1': round(float(sr['r1']), 4),
                    'r2': round(float(sr['r2']), 4),
                    's1': round(float(sr['s1']), 4),
                    's2': round(float(sr['s2']), 4),
                    'zona': zona,
                    'adx': round(float(adx_data['adx']), 2),
                    'plus_di': round(float(adx_data['plus_di']), 2),
                    'minus_di': round(float(adx_data['minus_di']), 2),
                    'tendencia_fuerza': "FUERTE" if adx_data['adx'] > 25 else "DEBIL"
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(sr['s2'] * 0.995), 4) if direccion == "COMPRA" else round(float(sr['r2'] * 1.005), 4),
                    'take_profit': round(float(sr['pivot']), 4) if direccion == "COMPRA" else round(float(sr['pivot']), 4)
                }
            }
            
            logger.info(f"{self.symbol}: {direccion} (Zona: {zona}, ADX: {adx_data['adx']:.1f}, +DI/-DI: {adx_data['plus_di']:.1f}/{adx_data['minus_di']:.1f})")
            return resultado
            
        except Exception as e:
            logger.error(f"Error ATOM: {e}")
            return None
