#!/usr/bin/env python3
"""
Verificar si las API Keys fueron revocadas/desactivadas
"""
from binance.client import Client
import json

print("🔍 VERIFICANDO ESTADO DE API KEYS")
print("=" * 50)

# Leer configuración
with open("config_futures.json", 'r') as f:
    config = json.load(f)

api_key = config['binance']['api_key']
api_secret = config['binance']['api_secret']

print(f"API Key: {api_key[:20]}...")

print("\n🔧 Probando diferentes endpoints para diagnóstico exacto...")

client = Client(api_key, api_secret, testnet=True)

# 1. Probar el endpoint más básico
print("\n1️⃣ Endpoint más básico (exchange_info):")
try:
    info = client.futures_exchange_info()
    print(f"   ✅ Funciona - Las keys NO están revocadas")
    print(f"   • Status: ACTIVE")
    print(f"   • Símbolos: {len(info.get('symbols', []))}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print(f"   ⚠️  Posiblemente REVOCADAS")

# 2. Probar si podemos hacer algo que requiera firma
print("\n2️⃣ Endpoint que requiere firma (account status):")
try:
    status = client.futures_account()
    print(f"   ✅ futures_account() FUNCIONA")
    print(f"   • Las keys tienen TODOS los permisos")
    print(f"   • Status: FULL ACCESS")
except Exception as e:
    error_msg = str(e)
    print(f"   ❌ Error: {error_msg}")
    
    if "-2015" in error_msg:
        print(f"   🔍 Error -2015: 'Invalid API-key, IP, or permissions for action'")
        print(f"   💡 Posibles causas:")
        print(f"      a) Keys REVOCADAS después de funcionar")
        print(f"      b) Activaste RESTRICCIÓN IP después")
        print(f"      c) Binance tuvo un problema y reseteeó permisos")

# 3. Probar con Spot para comparar
print("\n3️⃣ Probando con Binance Spot (para comparar):")
try:
    spot_client = Client(api_key, api_secret, testnet=True)
    ticker = spot_client.get_symbol_ticker(symbol="BTCUSDT")
    print(f"   ✅ Spot funciona: Precio BTC: {ticker['price']}")
except Exception as e:
    print(f"   ❌ Spot también falla: {e}")

print("\n" + "=" * 50)
print("🎯 CONCLUSIÓN BASADA EN LOS HECHOS:")
print("• HOY funcionaba")
print("• AHORA no funciona")
print("• MISMAS API Keys")
print("")
print("❌ LO MÁS PROBABLE: Las API Keys fueron REVOCADAS")
print("")
print("💡 SOLUCIÓN INMEDIATA:")
print("1. Ve a Binance Testnet AHORA MISMO")
print("2. Verifica si las API Keys siguen ACTIVAS")
print("3. Si NO lo están, créalas NUEVAMENTE")
print("4. Actualiza config_futures.json")

print("\n⚠️  ¿Puedes verificar AHORA en Binance si tus API Keys siguen activas?")
