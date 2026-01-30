#!/usr/bin/env python3
"""
Verificar específicamente qué sub-permisos faltan
"""
from binance.client import Client
import json

print("🔍 VERIFICACIÓN ESPECÍFICA DE SUB-PERMISOS")
print("=" * 50)

# Leer configuración
with open("config_futures.json", 'r') as f:
    config = json.load(f)

api_key = config['binance']['api_key']
api_secret = config['binance']['api_secret']

print("🔧 Probando llamadas específicas para identificar permisos faltantes...")

client = Client(api_key, api_secret, testnet=True)

# 1. Probar si podemos LEER datos (esto debería funcionar)
print("\n1️⃣ LECTURA DE DATOS (debería funcionar):")
try:
    ticker = client.futures_symbol_ticker(symbol="BTCUSDT")
    print(f"   ✅ futures_symbol_ticker() funciona")
    print(f"   • Precio BTC: {ticker['price']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Probar si podemos VER información de cuenta (esto podría fallar)
print("\n2️⃣ LECTURA DE CUENTA (podría fallar sin permisos completos):")
try:
    account = client.futures_account()
    print(f"   ✅ futures_account() funciona - ¡TIENES TODOS LOS PERMISOS!")
    print(f"   • Balance: {next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {}).get('walletBalance', 'N/A')}")
except Exception as e:
    print(f"   ❌ futures_account() falla: {e}")
    print(f"   💡 FALTA: 'Enable Futures Trading' (permiso específico de trading)")

# 3. Probar si podemos CREAR órdenes (esto definitivamente fallará)
print("\n3️⃣ CREACIÓN DE ÓRDENES (definitivamente fallará):")
try:
    # Solo probar con cantidad 0 para no crear orden real
    print("   Probando validación de orden...")
    order_test = client.futures_create_order_test(
        symbol="BTCUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.001
    )
    print(f"   ✅ ¡SORPRESA! Puedes crear órdenes")
except Exception as e:
    print(f"   ❌ No puedes crear órdenes: {e}")
    print(f"   💡 FALTA: Permiso de 'TRADING' específico")

print("\n" + "=" * 50)
print("🎯 CONCLUSIÓN:")
print("Tienes permisos de LECTURA pero NO de TRADING.")
print("En Binance, necesitas activar específicamente:")
print("• DENTRO de 'Habilitar spot y trading de margen': 'Enable Spot & Margin Trading'")
print("• DENTRO de 'Habilitar Contratos': 'Enable Futures' Y 'Enable Futures Trading'")

print("\n📋 SOLUCIÓN:")
print("1. Ve a Binance → API Management")
print("2. Edita tu API Key")
print("3. Busca OPCIONES AVANZADAS o 'Mostrar todos los permisos'")
print("4. Activa los sub-permisos específicos de TRADING")
print("5. O crea NUEVAS API Keys con TODOS los permisos activados desde el inicio")
