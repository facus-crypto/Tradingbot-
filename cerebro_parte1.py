#!/usr/bin/env python3
"""
PARTE 1: Cerebro Cuántico - Estructura Base
"""
import requests
import time
from datetime import datetime

print("🧠 PARTE 1: Estructura base creada")

# Monedas
MONEDAS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "LINKUSDT"]

def obtener_precio(symbol):
    """Obtiene precio de Binance"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=5)
        return float(response.json()['price'])
    except:
        return 0

# Prueba
print("Monedas:", MONEDAS)
for m in MONEDAS[:2]:
    p = obtener_precio(m)
    print(f"{m}: ${p:,.2f}")
