import pandas as pd
import numpy as np
from typing import Dict, Optional
import logging
from cerebros.cerebro_base_futures import CerebroFuturesBase

logger = logging.getLogger(__name__)

class CerebroBTCFutures(CerebroFuturesBase):
    """Cerebro para BTCUSDT - EMA Ribbon + RSI"""
    
    def __init__(self, binance_manager, telegram_bot=None):
        super().__init__(binance_manager, telegram_bot)
        self.nombre_estrategia = "ema_ribbon_rsi"
        self.timeframe = "1h"
        logger.info(f"✅ Cerebro TEMPLATE inicializado - {self.nombre_estrategia}")
    
    def analizar(self) -> Optional[Dict]:
        """Analiza BTCUSDT usando EMA Ribbon + RSI"""
        try:
            # Obtener velas
            velas = self.obtener_velas_reales(self.timeframe, 100)
            if len(velas) < 50:
                return None
            
            # Convertir a DataFrame
            df = pd.DataFrame(velas)
            df['close'] = pd.to_numeric(df['close'])
            
            # Calcular EMAs
            df['ema_9'] = df['close'].ewm(span=9).mean()
            df['ema_21'] = df['close'].ewm(span=21).mean()
            df['ema_50'] = df['close'].ewm(span=50).mean()
            df['ema_200'] = df['close'].ewm(span=200).mean()
            
            # Calcular RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # Últimos valores
            ultimo = df.iloc[-1]
            precio_actual = ultimo['close']
            
            # Señal EMA Ribbon
            ema_tendencia = "ALCISTA" if (ultimo['ema_9'] > ultimo['ema_21'] > ultimo['ema_50']) else "BAJISTA"
            
            # Señal RSI
            rsi_señal = "SOBREVENTA" if ultimo['rsi'] < 30 else "SOBRECOMPRA" if ultimo['rsi'] > 70 else "NEUTRAL"
            
            # Determinar dirección
            if ema_tendencia == "ALCISTA" and rsi_señal == "SOBREVENTA":
                direccion = "COMPRA"
                confianza = 0.75
            elif ema_tendencia == "BAJISTA" and rsi_señal == "SOBRECOMPRA":
                direccion = "VENTA"
                confianza = 0.75
            else:
                direccion = "NEUTRAL"
                confianza = 0.30
            
            # Niveles
            niveles = {
                'entrada': precio_actual,
                'stop': precio_actual * 0.98 if direccion == "COMPRA" else precio_actual * 1.02,
                'take': precio_actual * 1.03 if direccion == "COMPRA" else precio_actual * 0.97
            }
            
            return {
                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': confianza,
                'precio_actual': precio_actual,
                'indicadores': {
                    'ema_9': float(ultimo['ema_9']),
                    'ema_21': float(ultimo['ema_21']),
                    'ema_50': float(ultimo['ema_50']),
                    'ema_200': float(ultimo['ema_200']),
                    'rsi': float(ultimo['rsi']),
                    'tendencia': ema_tendencia,
                    'rsi_señal': rsi_señal
                },
                'niveles': niveles,
                'comentario': f"EMA: {ema_tendencia}, RSI: {rsi_señal}"
            }
            
        except Exception as e:
            logger.error(f"{self.symbol}: Error en análisis: {e}")
            return None
