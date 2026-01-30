import pandas as pd
import numpy as np
from .cerebro_base_futures import CerebroFuturesBase

class CerebroATOMFutures(CerebroFuturesBase):
    """Cerebro para ATOM - Estrategia Soporte/Resistencia + ADX"""
    
    def __init__(self, symbol="ATOMUSDT", binance_manager=None, telegram_bot=None):
        super().__init__(
            symbol=symbol,
            binance_manager=binance_manager,
            telegram_bot=telegram_bot
        )
        self.estrategia = "soporte_resistencia_adx"
        self.nombre = "ATOM_Soporte_Resistencia_ADX"
        self.timeframe = "4h"  # Análisis de swing
        print(f"✅ [ATOM] Cerebro inicializado - Estrategia: {self.estrategia}")
    
    def identificar_soportes_resistencias(self, df, window=20):
        """Identificar niveles de soporte y resistencia usando pivots"""
        df = df.copy()
        
        # Encontrar máximos y mínimos locales
        df['high_pivot'] = df['high'].rolling(window=window, center=True).apply(
            lambda x: 1 if x.iloc[window//2] == x.max() else 0, raw=False
        )
        df['low_pivot'] = df['low'].rolling(window=window, center=True).apply(
            lambda x: 1 if x.iloc[window//2] == x.min() else 0, raw=False
        )
        
        # Niveles de resistencia (máximos locales)
        resistencias = df[df['high_pivot'] == 1]['high'].values
        
        # Niveles de soporte (mínimos locales)
        soportes = df[df['low_pivot'] == 1]['low'].values
        
        return soportes, resistencias
    
    def calcular_indicadores(self, df):
        if len(df) < 50:
            return df
            
        # ADX (Average Directional Index) - Fuerza de tendencia
        # Calcular True Range
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )
        
        # Calcular +DM y -DM
        df['up_move'] = df['high'] - df['high'].shift(1)
        df['down_move'] = df['low'].shift(1) - df['low']
        
        df['plus_dm'] = np.where(
            (df['up_move'] > df['down_move']) & (df['up_move'] > 0),
            df['up_move'],
            0
        )
        
        df['minus_dm'] = np.where(
            (df['down_move'] > df['up_move']) & (df['down_move'] > 0),
            df['down_move'],
            0
        )
        
        # Suavizar con EMA de 14 periodos
        df['tr_smooth'] = df['tr'].ewm(span=14, adjust=False).mean()
        df['plus_dm_smooth'] = df['plus_dm'].ewm(span=14, adjust=False).mean()
        df['minus_dm_smooth'] = df['minus_dm'].ewm(span=14, adjust=False).mean()
        
        # Calcular DI+ y DI-
        df['plus_di'] = 100 * (df['plus_dm_smooth'] / df['tr_smooth'])
        df['minus_di'] = 100 * (df['minus_dm_smooth'] / df['tr_smooth'])
        
        # Calcular ADX
        df['dx'] = 100 * abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])
        df['ADX'] = df['dx'].ewm(span=14, adjust=False).mean()
        
        # Identificar soportes y resistencias
        soportes, resistencias = self.identificar_soportes_resistencias(df)
        
        # Agregar los niveles más recientes al dataframe
        if len(soportes) > 0:
            df['soporte_1'] = soportes[-1] if len(soportes) >= 1 else np.nan
            df['soporte_2'] = soportes[-2] if len(soportes) >= 2 else np.nan
        else:
            df['soporte_1'] = np.nan
            df['soporte_2'] = np.nan
            
        if len(resistencias) > 0:
            df['resistencia_1'] = resistencias[-1] if len(resistencias) >= 1 else np.nan
            df['resistencia_2'] = resistencias[-2] if len(resistencias) >= 2 else np.nan
        else:
            df['resistencia_1'] = np.nan
            df['resistencia_2'] = np.nan
        
        # EMA para tendencia
        df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()
        
        # Volumen analysis
        df['volume_sma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        # RSI para momentum
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Distancia a soportes/resistencias
        df['dist_soporte'] = df.apply(
            lambda row: min(
                abs(row['close'] - row['soporte_1']) if not np.isnan(row['soporte_1']) else np.inf,
                abs(row['close'] - row['soporte_2']) if not np.isnan(row['soporte_2']) else np.inf
            ),
            axis=1
        )
        
        df['dist_resistencia'] = df.apply(
            lambda row: min(
                abs(row['close'] - row['resistencia_1']) if not np.isnan(row['resistencia_1']) else np.inf,
                abs(row['close'] - row['resistencia_2']) if not np.isnan(row['resistencia_2']) else np.inf
            ),
            axis=1
        )
        
        return df
    
    def generar_senal(self, df):
        if len(df) < 50:
            return 0, 0, "Insuficientes datos"
        
        ultimo = df.iloc[-1]
        penultimo = df.iloc[-2]
        
        # Condiciones de mercado
        tendencia_fuerte = ultimo['ADX'] > 25  # ADX > 25 indica tendencia fuerte
        tendencia_alcista = ultimo['plus_di'] > ultimo['minus_di']
        tendencia_bajista = ultimo['plus_di'] < ultimo['minus_di']
        
        # Umbral de proximidad a S/R (2%)
        umbral_proximidad = ultimo['close'] * 0.02
        
        # Señal de COMPRA: Rebote en soporte con confirmación
        cerca_soporte = ultimo['dist_soporte'] < umbral_proximidad
        if cerca_soporte and not np.isinf(ultimo['dist_soporte']):
            # Condiciones para compra
            condicion_rsi = ultimo['RSI'] < 50  # No sobrecomprado
            condicion_volumen = ultimo['volume_ratio'] > 1.2  # Volumen arriba del promedio
            condicion_adx = ultimo['ADX'] > 20  # Alguna tendencia presente
            
            if condicion_rsi and condicion_volumen and condicion_adx:
                # Confirmación: precio empezando a subir desde soporte
                if ultimo['close'] > penultimo['close'] or tendencia_alcista:
                    confianza = min(0.85, 0.65 + (ultimo['ADX'] / 100))
                    nivel = 'soporte_1' if abs(ultimo['close'] - ultimo['soporte_1']) < abs(ultimo['close'] - ultimo['soporte_2']) else 'soporte_2'
                    return 1, confianza, f"LONG: Rebote {nivel} | ADX: {ultimo['ADX']:.1f} | RSI: {ultimo['RSI']:.1f}"
        
        # Señal de VENTA: Rechazo en resistencia con confirmación
        cerca_resistencia = ultimo['dist_resistencia'] < umbral_proximidad
        if cerca_resistencia and not np.isinf(ultimo['dist_resistencia']):
            # Condiciones para venta
            condicion_rsi = ultimo['RSI'] > 50  # No sobrevendido
            condicion_volumen = ultimo['volume_ratio'] > 1.2
            condicion_adx = ultimo['ADX'] > 20
            
            if condicion_rsi and condicion_volumen and condicion_adx:
                # Confirmación: precio empezando a bajar desde resistencia
                if ultimo['close'] < penultimo['close'] or tendencia_bajista:
                    confianza = min(0.85, 0.65 + (ultimo['ADX'] / 100))
                    nivel = 'resistencia_1' if abs(ultimo['close'] - ultimo['resistencia_1']) < abs(ultimo['close'] - ultimo['resistencia_2']) else 'resistencia_2'
                    return -1, confianza, f"SHORT: Rechazo {nivel} | ADX: {ultimo['ADX']:.1f} | RSI: {ultimo['RSI']:.1f}"
        
        # Breakout con ADX fuerte
        if tendencia_fuerte and ultimo['volume_ratio'] > 1.5:
            # Breakout alcista
            if tendencia_alcista and ultimo['close'] > ultimo['EMA_20'] and ultimo['RSI'] < 70:
                if ultimo['close'] > ultimo['resistencia_1'] * 1.01:  # 1% arriba de resistencia
                    return 1, 0.80, f"LONG: Breakout con ADX fuerte ({ultimo['ADX']:.1f})"
            
            # Breakdown bajista
            if tendencia_bajista and ultimo['close'] < ultimo['EMA_20'] and ultimo['RSI'] > 30:
                if ultimo['close'] < ultimo['soporte_1'] * 0.99:  # 1% abajo de soporte
                    return -1, 0.80, f"SHORT: Breakdown con ADX fuerte ({ultimo['ADX']:.1f})"
        
        return 0, 0, f"Esperando en S/R | ADX: {ultimo['ADX']:.1f}"
