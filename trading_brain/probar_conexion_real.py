#!/usr/bin/env python3
"""Probar conexión REAL a Binance con las keys existentes."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

api_key = config['binance']['api_key']
api_secret = config['binance']['api_secret']
testnet = config['binance'].get('testnet', False)

print(f"🔑 API Key: {api_key[:20]}...")
print(f"🔐 API Secret: {api_secret[:20]}...")
print(f"🌐 Testnet: {testnet}")

try:
    from binance_manager_custom import BinanceFuturesManagerCustom
    print("\n✅ Módulo Binance importado")
    
    # Crear manager
    bm = BinanceFuturesManagerCustom(api_key, api_secret, testnet)
    print("✅ Binance Manager creado")
    
    # Probar conexión simple
    print("\n🔄 Probando conexión a Binance...")
    
    # Intentar obtener precio de BTC
    from cerebros.cerebro_base_futures import CerebroFuturesBase
    
    cerebro_test = CerebroFuturesBase("BTCUSDT", bm, None)
    datos = cerebro_test.obtener_datos("1h", limite=10)
    
    if not datos.empty:
        print(f"✅ Datos REALES obtenidos:")
        print(f"   • Precio BTC: {datos['close'].iloc[-1]:.2f}")
        print(f"   • Velas: {len(datos)}")
        print(f"   • Rango: {datos.index[0]} a {datos.index[-1]}")
    else:
        print("❌ No se pudieron obtener datos")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
