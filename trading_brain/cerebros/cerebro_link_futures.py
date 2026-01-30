import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroLINKFutures(CerebroFuturesBase):
    """Cerebro para Chainlink con Fibonacci e Ichimoku."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("LINKUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "fibonacci_ichimoku_orderflow"
        self.timeframe = "4h"
        logger.info(f"✅ Cerebro LINK inicializado - {self.nombre_estrategia}")
    
    def calcular_fibonacci(self, datos):
        """Calcula niveles Fibonacci del último swing."""
        if len(datos) < 20:
            return {}
        
        high = datos['high'].max()
        low = datos['low'].min()
        diff = high - low
        
        return {
            '0.0': high,
            '0.236': high - diff * 0.236,
            '0.382': high - diff * 0.382,
            '0.5': high - diff * 0.5,
            '0.618': high - diff * 0.618,
            '0.786': high - diff * 0.786,
            '1.0': low
        }
    
    def analizar(self) -> Optional[Dict]:
        """Análisis LINK con Fibonacci e Ichimoku."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 30:
                return None
            
            precio = datos['close'].iloc[-1]
            fib = self.calcular_fibonacci(datos.tail(20))
            
            # Ichimoku simplificado (Tenkan-sen y Kijun-sen)
            high9 = datos['high'].rolling(window=9).max()
            low9 = datos['low'].rolling(window=9).min()
            tenkan = (high9 + low9) / 2
            
            high26 = datos['high'].rolling(window=26).max()
            low26 = datos['low'].rolling(window=26).min()
            kijun = (high26 + low26) / 2
            
            tenkan_actual = tenkan.iloc[-1]
            kijun_actual = kijun.iloc[-1]
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # COMPRA: Precio cerca de soporte Fibonacci, Tenkan > Kijun
            fib_soportes = [fib.get('0.618'), fib.get('0.786')]
            cerca_soporte = any(abs(precio - s) / s < 0.02 for s in fib_soportes if s)
            
            if tenkan_actual > kijun_actual and cerca_soporte:
                direccion = "COMPRA"
                confianza = 0.70
            
            # VENTA: Precio cerca de resistencia Fibonacci, Tenkan < Kijun
            fib_resistencias = [fib.get('0.236'), fib.get('0.382')]
            cerca_resistencia = any(abs(precio - r) / r < 0.02 for r in fib_resistencias if r)
            
            if tenkan_actual < kijun_actual and cerca_resistencia:
                direccion = "VENTA"
                confianza = 0.65
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'fib_0.236': round(fib.get('0.236', 0), 4),
                    'fib_0.382': round(fib.get('0.382', 0), 4),
                    'fib_0.618': round(fib.get('0.618', 0), 4),
                    'fib_0.786': round(fib.get('0.786', 0), 4),
                    'tenkan': round(float(tenkan_actual), 4),
                    'kijun': round(float(kijun_actual), 4),
                    'cloud_position': 'above' if tenkan_actual > kijun_actual else 'below'
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(precio * 0.975), 4) if direccion == "COMPRA" else round(float(precio * 1.025), 4),
                    'take_profit': round(float(precio * 1.05), 4) if direccion == "COMPRA" else round(float(precio * 0.95), 4)
                }
            }
            
            logger.info(f"{self.symbol}: {direccion} (Fib: {precio/fib.get('1.0', precio)*100:.1f}%, TK: {tenkan_actual:.4f})")
            return resultado
            
        except Exception as e:
            logger.error(f"Error LINK: {e}")
            return None
