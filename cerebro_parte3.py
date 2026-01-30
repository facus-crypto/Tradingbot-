#!/usr/bin/env python3
"""
PARTE 3: Nivel 2 - Indicadores Específicos
"""
import requests
import pandas as pd
import ta

print("📊 NIVEL 2: Indicadores Específicos")

def obtener_velas_df(symbol, intervalo="1h", limite=100):
    """Obtiene velas en DataFrame"""
    try:
        url = f"https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": intervalo, "limit": limite}
        response = requests.get(url, params=params, timeout=10)
        datos = response.json()
        
        df = pd.DataFrame(datos, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        return df
    except:
        return pd.DataFrame()

def analizar_btc(df):
    """Indicadores específicos BTC"""
    close = df['close']
    
    rsi = ta.momentum.RSIIndicator(close, window=14).rsi()
    ema_21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
    ema_50 = ta.trend.EMAIndicator(close, window=50).ema_indicator()
    
    return {
        "rsi": round(rsi.iloc[-1], 2),
        "ema_21": round(ema_21.iloc[-1], 2),
        "ema_50": round(ema_50.iloc[-1], 2),
        "tendencia": "ALCISTA" if ema_21.iloc[-1] > ema_50.iloc[-1] else "BAJISTA",
        "precio": round(close.iloc[-1], 2)
    }

def analizar_sol(df):
    """Indicadores específicos SOL"""
    close = df['close']
    
    rsi = ta.momentum.RSIIndicator(close, window=14).rsi()
    ema_9 = ta.trend.EMAIndicator(close, window=9).ema_indicator()
    ema_21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
    
    return {
        "rsi": round(rsi.iloc[-1], 2),
        "ema_9": round(ema_9.iloc[-1], 2),
        "ema_21": round(ema_21.iloc[-1], 2),
        "ema_cross": "ALCISTA" if ema_9.iloc[-1] > ema_21.iloc[-1] else "BAJISTA",
        "precio": round(close.iloc[-1], 2)
    }

# Probar con BTC
print("\n🔍 Analizando BTC:")
df_btc = obtener_velas_df("BTCUSDT", "1h", 100)
if not df_btc.empty:
    btc_indicadores = analizar_btc(df_btc)
    print(f"   Precio: ${btc_indicadores['precio']:,.2f}")
    print(f"   RSI: {btc_indicadores['rsi']}")
    print(f"   Tendencia: {btc_indicadores['tendencia']}")

# Probar con SOL
print("\n🔍 Analizando SOL:")
df_sol = obtener_velas_df("SOLUSDT", "1h", 100)
if not df_sol.empty:
    sol_indicadores = analizar_sol(df_sol)
    print(f"   Precio: ${sol_indicadores['precio']:,.2f}")
    print(f"   RSI: {sol_indicadores['rsi']}")
    print(f"   EMA Cross: {sol_indicadores['ema_cross']}")

print("\n✅ Nivel 2 completado")
