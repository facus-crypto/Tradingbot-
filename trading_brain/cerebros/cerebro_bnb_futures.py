import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroBNBFutures(CerebroFuturesBase):
    """Cerebro para BNB con ADX y Volume Profile."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("BNBUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "adx_volume_profile_correlation"
        self.timeframe = "1h"
        logger.info(f"✅ Cerebro BNB inicializado - {self.nombre_estrategia}")
    
    def calcular_adx(self, datos, periodo=14):
        """Calcula ADX (Average Directional Index)."""
        high, low, close = datos['high'], datos['low'], datos['close']
        
        # True Range
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(periodo).mean()
        
        # Directional Movement
        up_move = high - high.shift()
        down_move = low.shift() - low
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        plus_di = 100 * (pd.Series(plus_dm).rolling(periodo).mean() / atr)
        minus_di = 100 * (pd.Series(minus_dm).rolling(periodo).mean() / atr)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(periodo).mean()
        
        return adx.iloc[-1], plus_di.iloc[-1], minus_di.iloc[-1]
    
    def analizar(self) -> Optional[Dict]:
        """Análisis BNB con ADX y Volume Profile."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 30:
                return None
            
            precio = datos['close'].iloc[-1]
            volumen_total = datos['volume'].sum()
            volumen_promedio = datos['volume'].mean()
            volumen_actual = datos['volume'].iloc[-1]
            
            # ADX
            adx, plus_di, minus_di = self.calcular_adx(datos)
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # COMPRA: ADX > 25 (tendencia fuerte), +DI > -DI, volumen sobre promedio
            if adx > 25 and plus_di > minus_di and volumen_actual > volumen_promedio * 1.5:
                direccion = "COMPRA"
                confianza = 0.78
                if adx > 35:
                    confianza = 0.85
            
            # VENTA: ADX > 25, -DI > +DI, volumen sobre promedio
            elif adx > 25 and minus_di > plus_di and volumen_actual > volumen_promedio * 1.5:
                direccion = "VENTA"
                confianza = 0.73
                if adx > 35:
                    confianza = 0.80
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'adx': round(float(adx), 2),
                    'plus_di': round(float(plus_di), 2),
                    'minus_di': round(float(minus_di), 2),
                    'volumen_actual': round(float(volumen_actual), 2),
                    'volumen_ratio': round(volumen_actual / volumen_promedio, 2),
                    'vwap': round((datos['close'] * datos['volume']).sum() / volumen_total, 4)
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(precio * 0.98), 4) if direccion == "COMPRA" else round(float(precio * 1.02), 4),
                    'take_profit': round(float(precio * 1.04), 4) if direccion == "COMPRA" else round(float(precio * 0.96), 4)
                }
            }
            
            logger.info(f"{self.symbol}: {direccion} (ADX: {adx:.1f}, +DI/-DI: {plus_di:.1f}/{minus_di:.1f})")
            return resultado
            
        except Exception as e:
            logger.error(f"Error BNB: {e}")
            return None
