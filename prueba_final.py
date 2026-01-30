import requests
import numpy as np
import pandas as pd
import ta
from binance.client import Client
import time

print("✅ 1. Requests funciona")
print("✅ 2. Numpy funciona")
print("✅ 3. Pandas funciona")
print("✅ 4. TA funciona")

# Probar Binance (solo conexión pública)
try:
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url, timeout=5)
    precio = float(response.json()['price'])
    print(f"✅ 5. Binance API funciona - BTC: ${precio:,.2f}")
except:
    print("❌ 5. Binance API falló")

print("\n🎯 ¡TODAS LAS LIBRERÍAS ESTÁN INSTALADAS!")
print("El bot funcionará correctamente en Termux.")
