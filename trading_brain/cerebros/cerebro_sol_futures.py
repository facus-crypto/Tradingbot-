import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase
import logging

logger = logging.getLogger(__name__)

class CerebroSOLFutures(CerebroFuturesBase):
    """Cerebro para Solana con RSI ajustado y EMAs rápidas."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("SOLUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "rsi_ajustado_emas_rapidas"
        self.timeframe = "15m"
        logger.info(f"✅ Cerebro SOL inicializado - {self.nombre_estrategia}")
    
    def calcular_rsi_ajustado(self, datos, periodo=14, smoothing=3):
        """RSI ajustado con suavizado."""
        delta = datos['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
        
        # Suavizado adicional
        gain_smooth = gain.rolling(window=smoothing).mean()
        loss_smooth = loss.rolling(window=smoothing).mean()
        
        rs = gain_smooth / loss_smooth
        return 100 - (100 / (1 + rs))
    
    def analizar(self) -> Optional[Dict]:
        """Análisis SOL con RSI ajustado y EMAs 9/21."""
        try:
            datos = self.obtener_datos(self.timeframe, limite=100)
            if len(datos) < 30:
                return None
            
            # Calcular EMAs
            datos['ema9'] = datos['close'].ewm(span=9, adjust=False).mean()
            datos['ema21'] = datos['close'].ewm(span=21, adjust=False).mean()
            
            # RSI ajustado
            datos['rsi_ajustado'] = self.calcular_rsi_ajustado(datos)
            
            ultimo = datos.iloc[-1]
            precio = ultimo['close']
            ema9 = ultimo['ema9']
            ema21 = ultimo['ema21']
            rsi = ultimo['rsi_ajustado']
            
            # Condiciones
            direccion = "NEUTRAL"
            confianza = 0.3
            
            # COMPRA: EMA9 > EMA21, RSI entre 40-60 (zona de acumulación)
            if ema9 > ema21 and 40 < rsi < 60:
                direccion = "COMPRA"
                confianza = 0.72
                if 45 < rsi < 55:  # Zona óptima
                    confianza = 0.82
            
            # VENTA: EMA9 < EMA21, RSI entre 40-60
            elif ema9 < ema21 and 40 < rsi < 60:
                direccion = "VENTA"
                confianza = 0.68
                if 45 < rsi < 55:
                    confianza = 0.78
            
            resultado = {
                'timestamp': datos.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                'par': self.symbol,
                'direccion': direccion,
                'confianza': round(confianza, 2),
                'precio_actual': round(float(precio), 4),
                'indicadores': {
                    'rsi_ajustado': round(float(rsi), 2),
                    'ema9': round(float(ema9), 4),
                    'ema21': round(float(ema21), 4),
                    'ema_spread': round(((ema9 - ema21) / ema21) * 100, 2),
                    'volumen': round(float(ultimo['volume']), 2)
                },
                'niveles': {
                    'entrada': round(float(precio), 4),
                    'stop_loss': round(float(precio * 0.982), 4) if direccion == "COMPRA" else round(float(precio * 1.018), 4),
                    'take_profit': round(float(precio * 1.035), 4) if direccion == "COMPRA" else round(float(precio * 0.965), 4)
                }
            }
            
            logger.info(f"{self.symbol}: {direccion} (RSI: {rsi:.1f}, EMA9-21: {((ema9-ema21)/ema21*100):.2f}%)")
            return resultado
            
        except Exception as e:
            logger.error(f"Error SOL: {e}")
            return None
