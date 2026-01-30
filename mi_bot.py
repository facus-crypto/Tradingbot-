#!/usr/bin/env python3
"""
🤖 CEREBRO CUÁNTICO - Binance Futures 2x (50% wallet)
Nivel 1: Filtros Mercado
Nivel 2: Indicadores Específicos
"""
import requests
import time
import pandas as pd
import ta
from datetime import datetime

print("=" * 70)
print("🤖 CEREBRO CUÁNTICO ACTIVADO - Futuros 2x")
print("=" * 70)

# Monedas
MONEDAS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "LINKUSDT"]

# ========== FUNCIONES BÁSICAS ==========
def obtener_precio(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=5)
        return float(response.json()['price'])
    except:
        return 0

def obtener_velas_df(symbol, intervalo="1h", limite=100):
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
# =======================================

# ========== NIVEL 1: FILTROS MERCADO ==========
def verificar_tendencia_btc():
    velas = obtener_velas_df("BTCUSDT", "4h", 50)
    
    if velas.empty or len(velas) < 20:
        return "NEUTRAL"
    
    close = velas['close']
    
    if len(close) >= 20:
        ema_20 = ta.trend.EMAIndicator(close, window=20).ema_indicator()
        ema_50 = ta.trend.EMAIndicator(close, window=50).ema_indicator()
        
        if close.iloc[-1] > ema_20.iloc[-1] > ema_50.iloc[-1]:
            return "ALCISTA_FUERTE"
        elif close.iloc[-1] < ema_20.iloc[-1] < ema_50.iloc[-1]:
            return "BAJISTA_FUERTE"
        elif close.iloc[-1] > ema_20.iloc[-1]:
            return "ALCISTA"
        else:
            return "BAJISTA"
    
    return "NEUTRAL"

def filtro_mercado():
    print("\n🔍 NIVEL 1: Filtros de Mercado")
    
    tendencia = verificar_tendencia_btc()
    print(f"   📈 Tendencia BTC: {tendencia}")
    
    # Reglas simples
    if "BAJISTA_FUERTE" in tendencia:
        print("   ⚠️  NO OPERAR: Tendencia BTC muy bajista")
        return False, tendencia
    elif "ALCISTA" in tendencia:
        print("   ✅  MERCADO ACEPTABLE")
        return True, tendencia
    else:
        print("   🟡  MERCADO NEUTRAL")
        return False, tendencia
# ==============================================

# ========== NIVEL 2: INDICADORES ==========
def analizar_moneda(symbol):
    df = obtener_velas_df(symbol, "1h", 100)
    
    if df.empty:
        return None
    
    close = df['close']
    rsi = ta.momentum.RSIIndicator(close, window=14).rsi()
    
    resultado = {
        "precio": round(close.iloc[-1], 2),
        "rsi": round(rsi.iloc[-1], 2)
    }
    
    # BTC específico
    if symbol == "BTCUSDT":
        ema_21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
        ema_50 = ta.trend.EMAIndicator(close, window=50).ema_indicator()
        resultado["tendencia"] = "ALCISTA" if ema_21.iloc[-1] > ema_50.iloc[-1] else "BAJISTA"
    
    # SOL específico
    elif symbol == "SOLUSDT":
        ema_9 = ta.trend.EMAIndicator(close, window=9).ema_indicator()
        ema_21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
        resultado["ema_cross"] = "ALCISTA" if ema_9.iloc[-1] > ema_21.iloc[-1] else "BAJISTA"
    
    return resultado

def analizar_todas_monedas():
    print("\n📊 NIVEL 2: Indicadores por Moneda")
    
    for symbol in MONEDAS:
        datos = analizar_moneda(symbol)
        if datos:
            print(f"\n🔍 {symbol}:")
            print(f"   💰 Precio: ${datos['precio']:,.2f}")
            print(f"   📈 RSI: {datos['rsi']}")
            
            if 'tendencia' in datos:
                print(f"   📉 Tendencia: {datos['tendencia']}")
            if 'ema_cross' in datos:
                print(f"   ⚡ EMA Cross: {datos['ema_cross']}")
# ==========================================

# ========== BUCLE PRINCIPAL ==========
def main():
    ciclo = 0
    
    while True:
        ciclo += 1
        hora = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n{'='*60}")
        print(f"🔄 CICLO #{ciclo} - {hora}")
        print('='*60)
        
        # NIVEL 1: Filtros mercado
        mercado_ok, tendencia = filtro_mercado()
        
        if mercado_ok:
            # NIVEL 2: Análisis detallado
            analizar_todas_monedas()
            
            print("\n✅ Listo para trading (si hay señales)")
        else:
            print(f"\n⏸️  Esperando condiciones de mercado...")
        
        # Esperar 5 minutos entre ciclos
        print(f"\n⏰ Siguiente ciclo en 5 minutos...")
        time.sleep(300)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Cerebro detenido")
