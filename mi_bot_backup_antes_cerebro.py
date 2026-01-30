#!/usr/bin/env python3
"""
Bot básico para Termux - Monitoreo de cripto
"""
import requests
import time
from datetime import datetime
import sys

print("=" * 50)
print("🤖 BOT TERMUX INICIADO")
print("=" * 50)

def obtener_precio(symbol="BTCUSDT"):
    """Obtiene precio de Binance"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['price'])
    except:
        return 0

def main():
    ciclo = 0
    
    while True:
        ciclo += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n🔄 Ciclo #{ciclo} - {timestamp}")
        
        # Monitorear 5 monedas
        monedas = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "LINKUSDT"]
        
        for moneda in monedas:
            precio = obtener_precio(moneda)
            nombre = moneda.replace("USDT", "")
            print(f"   {nombre}: ${precio:,.2f}")
        
        # Esperar 30 segundos
        time.sleep(30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido")
