#!/usr/bin/env python3
"""Prueba SIMPLE de apalancamiento."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("🔧 Prueba simple apalancamiento")

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

# Importar
from binance_manager_custom import BinanceFuturesManagerCustom

bm = BinanceFuturesManagerCustom(
    config['binance']['api_key'],
    config['binance']['api_secret'],
    config['binance'].get('testnet', False)
)

print("✅ Manager creado")

# Probar método básico manual
print("\n🔍 Probando endpoint de apalancamiento manualmente...")

try:
    # Hacer solicitud manual para BTC
    endpoint = "/fapi/v1/leverage"
    params = "symbol=BTCUSDT&leverage=2"
    
    # Usar método interno _hacer_solicitud
    response = bm._hacer_solicitud(endpoint, params, method="POST")
    
    print(f"📊 Respuesta Binance: {response}")
    
    if isinstance(response, dict):
        if 'leverage' in response:
            print(f"✅ Apalancamiento configurado: {response['leverage']}x")
        elif 'code' in response:
            print(f"⚠️  Código error: {response['code']} - {response.get('msg', '')}")
    else:
        print(f"❌ Respuesta inesperada: {type(response)}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎯 Prueba completada")
