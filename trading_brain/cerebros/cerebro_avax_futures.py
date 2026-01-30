# cerebros/cerebro_avax_futures.py
# Cerebro para Avalanche (AVAXUSDT) - Estrategia: ema_multiple_macd_hist

import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase


class CerebroAVAXFutures(CerebroFuturesBase):
    """Cerebro para Avalanche (AVAX) con EMAs múltiples y MACD Histograma."""

    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("AVAXUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "ema_multiple_macd_hist"
        self.timeframe = "1h"  # Para tendencias
        print(
            f"[AVAXUSDT] ✅ Cerebro AVAX inicializado - {self.nombre_estrategia}")

    def calcular_emas_multiples(self, datos: pd.DataFrame) -> Dict:
        """Calcula múltiples EMAs (20, 50, 100)."""
        if len(datos) < 100:
            return {'ema20': None, 'ema50': None,
                    'ema100': None, 'tendencia': 'NEUTRAL'}

        datos['ema20'] = datos['close'].ewm(span=20, adjust=False).mean()
        datos['ema50'] = datos['close'].ewm(span=50, adjust=False).mean()
        datos['ema100'] = datos['close'].ewm(span=100, adjust=False).mean()

        ultimo = datos.iloc[-1]

        # Determinar tendencia por alineación de EMAs
        if ultimo['ema20'] > ultimo['ema50'] > ultimo['ema100']:
            tendencia = "ALCISTA"
        elif ultimo['ema20'] < ultimo['ema50'] < ultimo['ema100']:
            tendencia = "BAJISTA"
        else:
            tendencia = "NEUTRAL"

        return {
            'ema20': ultimo['ema20'],
            'ema50': ultimo['ema50'],
            'ema100': ultimo['ema100'],
            'tendencia': tendencia,
            'distancia_20_50': abs(ultimo['ema20'] - ultimo['ema50']) / ultimo['ema50'] * 100,
            'distancia_50_100': abs(ultimo['ema50'] - ultimo['ema100']) / ultimo['ema100'] * 100
        }

    def calcular_macd_histograma(self, datos: pd.DataFrame) -> Dict:
        """Calcula MACD con enfoque en el histograma."""
        if len(datos) < 50:
            return {'macd': None, 'signal': None,
                    'histograma': None, 'cruce': 'NEUTRAL'}

        # Calcular MACD manualmente
        exp1 = datos['close'].ewm(span=12, adjust=False).mean()
        exp2 = datos['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histograma = macd - signal

        ultimo_hist = histograma.iloc[-1]
        previo_hist = histograma.iloc[-2]

        # Detectar cruces por histograma (más sensible)
        if previo_hist < 0 and ultimo_hist > 0:
            cruce = "ALCISTA"  # Histograma cruza de negativo a positivo
        elif previo_hist > 0 and ultimo_hist < 0:
            cruce = "BAJISTA"  # Histograma cruza de positivo a negativo
        else:
            cruce = "NEUTRAL"

        return {
            'macd': macd.iloc[-1],
            'signal': signal.iloc[-1],
            'histograma': ultimo_hist,
            'cruce': cruce,
            'creciendo': ultimo_hist > previo_hist  # Histograma creciendo/decreciendo
        }


    def analizar(self):
        """Análisis simplificado y funcional para AVAX."""
        try:
            # Obtener datos
            datos = self.obtener_datos(self.timeframe, limite=100)
            if datos.empty:
                return {"direccion": "NEUTRAL", "confianza": 0.0}
            
            precio = datos['close'].iloc[-1]
            
            # EMA simple (sin errores)
            datos['ema20'] = datos['close'].ewm(span=20, adjust=False).mean()
            datos['ema50'] = datos['close'].ewm(span=50, adjust=False).mean()
            
            ultimo = datos.iloc[-1]
            ema20 = ultimo['ema20']
            ema50 = ultimo['ema50']
            
            # Dirección simple
            if ema20 > ema50:
                return {
                    "direccion": "COMPRA",
                    "confianza": 0.7,
                    "precio_actual": float(precio),
                    "indicadores": {"ema20": float(ema20), "ema50": float(ema50)},
                    "niveles": {
                        "entrada": float(precio),
                        "stop_loss": float(precio * 0.97),
                        "take_profit": float(precio * 1.04)
                    }
                }
            elif ema20 < ema50:
                return {
                    "direccion": "VENTA", 
                    "confianza": 0.65,
                    "precio_actual": float(precio),
                    "indicadores": {"ema20": float(ema20), "ema50": float(ema50)},
                    "niveles": {
                        "entrada": float(precio),
                        "stop_loss": float(precio * 1.03),
                        "take_profit": float(precio * 0.96)
                    }
                }
            else:
                return {"direccion": "NEUTRAL", "confianza": 0.3}
                
        except Exception as e:
            print(f"Error AVAX: {e}")
            return {"direccion": "NEUTRAL", "confianza": 0.0}
