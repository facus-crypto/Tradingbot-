#!/usr/bin/env python3
"""
Test Binance API
"""
import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_SECRET_KEY')

print("🔑 API Key encontrada:", "✅" if api_key else "❌")
print("🔑 API Secret encontrada:", "✅" if api_secret else "❌")

if api_key and api_secret:
    try:
        client = Client(api_key, api_secret)
        # Probar conexión con endpoint seguro
        server_time = client.get_server_time()
        print("⏰ Hora servidor Binance:", server_time)
        print("✅ Conexión Binance: FUNCIONA")
        
        # Probar futures
        futures_balance = client.futures_account_balance()
        print(f"💰 Futuros: {len(futures_balance)} activos")
        for asset in futures_balance[:3]:  # Mostrar solo primeros 3
            if float(asset['balance']) > 0:
                print(f"   {asset['asset']}: {asset['balance']}")
                
    except Exception as e:
        print(f"❌ Error Binance: {e}")
