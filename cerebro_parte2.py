#!/usr/bin/env python3
"""
PARTE 2: Nivel 1 - Filtros de Mercado
"""
import requests
import time
from datetime import datetime

print("🔍 NIVEL 1: Filtros de Mercado")

def obtener_velas(symbol, intervalo="4h", limite=50):
    """Obtiene velas históricas"""
    try:
        url = f"https://api.binance.com/api/v3/klines"
        params = {"symbol": symbol, "interval": intervalo, "limit": limite}
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except:
        return []

def verificar_tendencia_btc():
    """Verifica tendencia del BTC"""
    velas = obtener_velas("BTCUSDT", "4h", 50)
    
    if len(velas) < 20:
        return "NEUTRAL"
    
    # Calcular precios de cierre
    precios = [float(v[4]) for v in velas]
    
    # EMA simple
    if len(precios) >= 20:
        ema_20 = sum(precios[-20:]) / 20
        ema_50 = sum(precios[-50:]) / 50 if len(precios) >= 50 else ema_20
        
        if precios[-1] > ema_20 > ema_50:
            return "ALCISTA_FUERTE"
        elif precios[-1] < ema_20 < ema_50:
            return "BAJISTA_FUERTE"
        elif precios[-1] > ema_20:
            return "ALCISTA"
        else:
            return "BAJISTA"
    
    return "NEUTRAL"

# Ejecutar filtro
tendencia = verificar_tendencia_btc()
print(f"📈 Tendencia BTC: {tendencia}")

# Reglas simples
if "BAJISTA_FUERTE" in tendencia:
    print("⚠️  NO OPERAR: Tendencia BTC muy bajista")
elif "ALCISTA" in tendencia:
    print("✅  MERCADO ACEPTABLE: Tendencia favorable")
else:
    print("🟡  MERCADO NEUTRAL: Esperar confirmación")
