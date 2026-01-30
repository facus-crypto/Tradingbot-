#!/usr/bin/env python3
"""
NIVEL 2: Indicadores Específicos por Moneda
"""
import requests
import pandas as pd
import numpy as np
import ta

def obtener_velas_dataframe(symbol, intervalo="1h", limite=100):
    """Obtiene velas y las convierte a DataFrame"""
    try:
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": intervalo,
            "limit": limite
        }
        response = requests.get(url, params=params, timeout=10)
        datos = response.json()
        
        # Convertir a DataFrame
        df = pd.DataFrame(datos, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        # Convertir tipos
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        
        return df
    except:
        return pd.DataFrame()

def calcular_indicadores_btc(df):
    """Indicadores específicos para BTC"""
    if df.empty or len(df) < 50:
        return {"error": "Datos insuficientes"}
    
    close = df['close']
    
    # 1. RSI (14)
    rsi = ta.momentum.RSIIndicator(close, window=14).rsi()
    
    # 2. EMA 21 y EMA 50
    ema_21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
    ema_50 = ta.trend.EMAIndicator(close, window=50).ema_indicator()
    
    # 3. MACD
    macd = ta.trend.MACD(close)
    
    # 4. Volumen promedio
    volumen_prom = df['volume'].rolling(20).mean()
    
    return {
        "rsi": round(rsi.iloc[-1], 2),
        "ema_21": round(ema_21.iloc[-1], 2),
        "ema_50": round(ema_50.iloc[-1], 2),
        "macd_histogram": round(macd.macd_diff().iloc[-1], 4),
        "volumen_ratio": round(df['volume'].iloc[-1] / volumen_prom.iloc[-1], 2),
        "precio": round(close.iloc[-1], 2),
        "tendencia": "ALCISTA" if ema_21.iloc[-1] > ema_50.iloc[-1] else "BAJISTA"
    }

def calcular_indicadores_sol(df):
    """Indicadores específicos para SOL (más agresivos)"""
    if df.empty or len(df) < 30:
        return {"error": "Datos insuficientes"}
    
    close = df['close']
    
    # SOL usa indicadores más rápidos
    rsi = ta.momentum.RSIIndicator(close, window=14).rsi()
    ema_9 = ta.trend.EMAIndicator(close, window=9).ema_indicator()
    ema_21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
    
    # Volumen más estricto para SOL
    volumen_prom = df['volume'].rolling(10).mean()
    
    return {
        "rsi": round(rsi.iloc[-1], 2),
        "ema_9": round(ema_9.iloc[-1], 2),
        "ema_21": round(ema_21.iloc[-1], 2),
        "volumen_ratio": round(df['volume'].iloc[-1] / volumen_prom.iloc[-1], 2),
        "precio": round(close.iloc[-1], 2),
        "ema_cross": "ALCISTA" if ema_9.iloc[-1] > ema_21.iloc[-1] else "BAJISTA"
    }

def analizar_moneda(symbol):
    """Analiza una moneda específica"""
    print(f"\n🔍 Analizando {symbol}:")
    
    # Obtener datos
    df = obtener_velas_dataframe(symbol, "1h", 100)
    
    if df.empty:
        print(f"   ⚠️ No se pudieron obtener datos para {symbol}")
        return None
    
    # Seleccionar indicadores según moneda
    if symbol == "BTCUSDT":
        indicadores = calcular_indicadores_btc(df)
    elif symbol == "SOLUSDT":
        indicadores = calcular_indicadores_sol(df)
    else:
        # Indicadores básicos para otras monedas
        close = df['close']
        rsi = ta.momentum.RSIIndicator(close, window=14).rsi()
        indicadores = {
            "rsi": round(rsi.iloc[-1], 2),
            "precio": round(close.iloc[-1], 2)
        }
    
    # Mostrar resultados
    if "error" not in indicadores:
        print(f"   📊 Precio: ${indicadores['precio']:,.2f}")
        print(f"   📈 RSI: {indicadores.get('rsi', 'N/A')}")
        
        if 'tendencia' in indicadores:
            print(f"   📉 Tendencia: {indicadores['tendencia']}")
        
        if 'volumen_ratio' in indicadores:
            print(f"   🔊 Volumen: {indicadores['volumen_ratio']}x promedio")
    
    return indicadores

# Prueba del Nivel 2
print("="*60)
print("🧠 NIVEL 2: Indicadores Específicos por Moneda")
print("="*60)

# Analizar cada moneda
monedas = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "LINKUSDT"]
resultados = {}

for moneda in monedas:
    resultados[moneda] = analizar_moneda(moneda)

print("\n✅ Nivel 2 completado.")
print("📊 Resumen indicadores calculados correctamente.")
