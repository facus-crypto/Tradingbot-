import pandas as pd
import numpy as np
from .cerebro_base_futures import CerebroFuturesBase

class CerebroDOTFutures(CerebroFuturesBase):
    """Cerebro para DOT - Estrategia Fibonacci + EMA + Volumen"""
    
    def __init__(self, symbol="DOTUSDT", binance_manager=None, telegram_bot=None):
        super().__init__(
            symbol=symbol,
            binance_manager=binance_manager,
            telegram_bot=telegram_bot
        )
        self.estrategia = "fibonacci_ema_volumen"
        self.nombre = "DOT_Fibonacci_EMA_Volumen"
        self.timeframe = "1h"
        print(f"✅ [DOT] Cerebro inicializado - Estrategia: {self.estrategia}")
    
    def calcular_indicadores(self, df):
        if len(df) < 100:
            return df
            
        # EMAs para tendencia
        df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['EMA_100'] = df['close'].ewm(span=100, adjust=False).mean()
        
        # EMA alignment score
        df['EMA_alignment'] = 0
        df.loc[df['EMA_20'] > df['EMA_50'], 'EMA_alignment'] += 1
        df.loc[df['EMA_50'] > df['EMA_100'], 'EMA_alignment'] += 1
        df.loc[df['close'] > df['EMA_20'], 'EMA_alignment'] += 1
        
        # Niveles Fibonacci (últimas 50 velas)
        df['high_50'] = df['high'].rolling(window=50).max()
        df['low_50'] = df['low'].rolling(window=50).min()
        df['range_50'] = df['high_50'] - df['low_50']
        
        # Niveles Fibonacci clave
        df['FIB_0'] = df['low_50']
        df['FIB_0.236'] = df['low_50'] + 0.236 * df['range_50']
        df['FIB_0.382'] = df['low_50'] + 0.382 * df['range_50']
        df['FIB_0.5'] = df['low_50'] + 0.5 * df['range_50']
        df['FIB_0.618'] = df['low_50'] + 0.618 * df['range_50']
        df['FIB_0.786'] = df['low_50'] + 0.786 * df['range_50']
        df['FIB_1'] = df['high_50']
        
        # Distancia al nivel Fibonacci más cercano
        niveles_fib = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
        df['distancia_fib'] = df.apply(
            lambda row: min([abs(row['close'] - row[f'FIB_{nivel}']) for nivel in niveles_fib]),
            axis=1
        )
        
        # Volumen analysis
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        # Volume-weighted price
        df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
        df['price_vs_vwap'] = (df['close'] - df['vwap']) / df['vwap'] * 100
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    
    def generar_senal(self, df):
        if len(df) < 100:
            return 0, 0, "Insuficientes datos"
        
        ultimo = df.iloc[-1]
        penultimo = df.iloc[-2]
        
        # Condiciones básicas
        ema_aligned = ultimo['EMA_alignment'] >= 2
        volumen_alto = ultimo['volume_ratio'] > 1.2
        cerca_fib = ultimo['distancia_fib'] < (ultimo['close'] * 0.01)
        
        # Señal de COMPRA: tendencia alcista + rebote en soporte Fibonacci
        if ema_aligned and ultimo['close'] > ultimo['EMA_20']:
            for nivel in [0, 0.236, 0.382]:
                fib_key = f'FIB_{nivel}'
                if abs(ultimo['close'] - ultimo[fib_key]) < (ultimo['close'] * 0.01):
                    if ultimo['RSI'] < 60 and volumen_alto:
                        if ultimo['RSI'] > 30 or (penultimo['RSI'] < 30 and ultimo['RSI'] > penultimo['RSI']):
                            confianza = min(0.85, 0.6 + (ultimo['volume_ratio'] * 0.1))
                            return 1, confianza, f"LONG: Rebote FIB {nivel*100}% | RSI: {ultimo['RSI']:.1f} | Vol: {ultimo['volume_ratio']:.1f}x"
        
        # Señal de VENTA: tendencia bajista + rechazo en resistencia Fibonacci
        if not ema_aligned and ultimo['close'] < ultimo['EMA_20']:
            for nivel in [0.618, 0.786, 1]:
                fib_key = f'FIB_{nivel}'
                if abs(ultimo['close'] - ultimo[fib_key]) < (ultimo['close'] * 0.01):
                    if ultimo['RSI'] > 40 and volumen_alto:
                        if ultimo['RSI'] < 70 or (penultimo['RSI'] > 70 and ultimo['RSI'] < penultimo['RSI']):
                            confianza = min(0.85, 0.6 + (ultimo['volume_ratio'] * 0.1))
                            return -1, confianza, f"SHORT: Rechazo FIB {nivel*100}% | RSI: {ultimo['RSI']:.1f} | Vol: {ultimo['volume_ratio']:.1f}x"
        
        # Breakout de rango Fibonacci
        if volumen_alto and ultimo['volume_ratio'] > 1.5:
            if ultimo['close'] > ultimo['FIB_0.618'] and penultimo['close'] <= ultimo['FIB_0.618']:
                if ultimo['EMA_alignment'] >= 2:
                    return 1, 0.75, f"LONG: Breakout FIB 61.8% | EMA aligned: {ultimo['EMA_alignment']}"
            
            if ultimo['close'] < ultimo['FIB_0.382'] and penultimo['close'] >= ultimo['FIB_0.382']:
                if ultimo['EMA_alignment'] <= 1:
                    return -1, 0.75, f"SHORT: Breakdown FIB 38.2% | EMA aligned: {ultimo['EMA_alignment']}"
        
        return 0, 0, "Esperando señal Fibonacci clara"
