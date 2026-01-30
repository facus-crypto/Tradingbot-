import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroDOTFutures(CerebroFuturesBase):
    """Cerebro para Polkadot con Fibonacci y EMA 200."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("DOTUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "fibonacci_ema_volumen"
        self.timeframe = "4h"
        logger.info(f"✅ Cerebro DOT inicializado - {self.nombre_estrategia}")
    
    def calcular_fibonacci_niveles(self, datos, lookback=50):
        """Calcula niveles Fibonacci del último swing."""
        if len(datos) < lookback:
            return {}
        
        # Encontrar swing alto y bajo
        datos_lookback = datos.tail(lookback)
        swing_high = datos_lookback['high'].max()
        swing_low = datos_lookback['low'].min()
        swing_range = swing_high - swing_low
        
        niveles = {
            '0.0': swing_high,
            '0.236': swing_high - swing_range * 0.236,
            '0.382': swing_high - swing_range * 0.382,
            '0.5': swing_high - swing_range * 0.5,
            '0.618': swing_high - swing_range * 0.618,
            '0.786': swing_high - swing_range * 0.786,
            '1.0': swing_low,
            '1.272': swing_low - swing_range * 0.272,
            '1.618': swing_low - swing_range * 0.618
        }
        
        return niveles
    
    def analizar(self) -> Optional[Dict]:
        """Análisis DOT con Fibonacci + EMA 200."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 60:
                return None
            
            # Calcular EMA 200
            datos['ema200'] = datos['close'].ewm(span=200, adjust=False).mean()
            
            precio = datos['close'].iloc[-1]
            ema200 = datos['ema200'].iloc[-1]
            
            # Calcular Fibonacci
            fib = self.calcular_fibonacci_niveles(datos, 50)
            
            # Determinar nivel Fibonacci más cercano
            nivel_mas_cercano = None
            distancia_min = float('inf')
            
            for nivel, valor in fib.items():
                if valor:
                    distancia = abs(precio - valor) / valor
                    if distancia < distancia_min:
                        distancia_min = distancia
                        nivel_mas_cercano = nivel
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # Niveles Fibonacci clave de soporte
            soportes_clave = ['0.618', '0.786', '1.0']
            resistencias_clave = ['0.236', '0.382', '0.5']
            
            # COMPRA: Precio cerca de soporte Fibonacci + sobre EMA200
            if nivel_mas_cercano in soportes_clave and distancia_min < 0.02 and precio > ema200:
                direccion = "COMPRA"
                confianza = 0.70
                if nivel_mas_cercano == '0.618':
                    confianza = 0.80
            
            # VENTA: Precio cerca de resistencia Fibonacci + bajo EMA200
            elif nivel_mas_cercano in resistencias_clave and distancia_min < 0.02 and precio < ema200:
                direccion = "VENTA"
                confianza = 0.65
                if nivel_mas_cercano == '0.236':
                    confianza = 0.75
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'ema200': round(float(ema200), 4),
                    'distancia_ema200': round(((precio - ema200) / ema200) * 100, 2),
                    'fib_nivel': nivel_mas_cercano or 'N/A',
                    'fib_valor': round(float(fib.get(nivel_mas_cercano, 0)), 4) if nivel_mas_cercano else 0,
                    'fib_0.382': round(float(fib.get('0.382', 0)), 4),
                    'fib_0.618': round(float(fib.get('0.618', 0)), 4),
                    'fib_1.0': round(float(fib.get('1.0', 0)), 4),
                    'volumen': round(float(datos['volume'].iloc[-1]), 2)
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(fib.get('1.0', precio * 0.97)), 4) if direccion == "COMPRA" else round(float(fib.get('0.236', precio * 1.03)), 4),
                    'take_profit': round(float(fib.get('0.382', precio * 1.04)), 4) if direccion == "COMPRA" else round(float(fib.get('0.786', precio * 0.96)), 4)
                }
            }
            
            logger.info(f"{self.symbol}: {direccion} (Fib: {nivel_mas_cercano}, EMA200: {((precio-ema200)/ema200*100):.1f}%)")
            return resultado
            
        except Exception as e:
            logger.error(f"Error DOT: {e}")
            return None
