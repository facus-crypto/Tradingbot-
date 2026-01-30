#!/usr/bin/env python3
"""
Diagnóstico específico de conexión a Binance Futures
"""
import os
import json
from binance.client import Client
from binance.exceptions import BinanceAPIException

print("🔧 DIAGNÓSTICO ESPECÍFICO DE CONEXIÓN")
print("=" * 50)

# Leer configuración
config_file = "config_futures.json"
if not os.path.exists(config_file):
    print(f"❌ {config_file} no encontrado")
    exit(1)

with open(config_file, 'r') as f:
    config = json.load(f)

api_key = config['binance']['api_key']
api_secret = config['binance']['api_secret']
testnet = config['binance']['testnet']

print(f"📋 CONFIGURACIÓN:")
print(f"• Testnet: {testnet}")
print(f"• API Key: {api_key[:64]}...")

# Intentar conexión con diferentes configuraciones
print("\n🔍 PROBANDO CONEXIONES...")

# Opción 1: Testnet Futures (lo que debería funcionar)
print("\n1️⃣ TESTNET FUTURES (lo esperado):")
try:
    client = Client(api_key, api_secret, testnet=True)
    
    # Probar endpoint específico de futures
    try:
        print("   Probando client.futures_account()...")
        account = client.futures_account()
        print(f"   ✅ ÉXITO! Conectado a Binance Futures Testnet")
        print(f"   • Balance USDT: {next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {}).get('walletBalance', 'N/A')}")
        print(f"   • Posiciones: {len([p for p in account.get('positions', []) if float(p.get('positionAmt', 0)) != 0])}")
    except BinanceAPIException as e:
        print(f"   ❌ Error en futures_account(): {e.code} - {e.message}")
        
        # Probar si al menos podemos hacer una llamada simple
        try:
            print("   Probando client.futures_exchange_info()...")
            info = client.futures_exchange_info()
            print(f"   ✅ futures_exchange_info() funciona")
            print(f"   • Símbolos disponibles: {len(info.get('symbols', []))}")
        except BinanceAPIException as e2:
            print(f"   ❌ Error en futures_exchange_info(): {e2.code} - {e2.message}")
            
except Exception as e:
    print(f"   ❌ Error general: {type(e).__name__}: {e}")

# Opción 2: Spot Testnet (para verificar que las keys funcionan)
print("\n2️⃣ SPOT TESTNET (verificación):")
try:
    client_spot = Client(api_key, api_secret, testnet=True)
    
    try:
        print("   Probando client.get_account()...")
        account = client_spot.get_account()
        print(f"   ✅ ÉXITO! Conectado a Binance Spot Testnet")
        print(f"   • Maker Commission: {account.get('makerCommission', 'N/A')}")
        
        # Verificar balances
        balances = account.get('balances', [])
        usdt_balance = next((b for b in balances if b['asset'] == 'USDT'), None)
        if usdt_balance:
            print(f"   • Balance USDT Spot: {float(usdt_balance['free']):.2f}")
            
    except BinanceAPIException as e:
        print(f"   ❌ Error en get_account(): {e.code} - {e.message}")
        
except Exception as e:
    print(f"   ❌ Error general: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("📋 CONCLUSIÓN:")
print("Si TODO falla, posibles causas:")
print("1. ❌ API Keys REVOCADAS o ELIMINADAS")
print("2. ❌ 'Habilitar Contratos' NO está realmente activado")
print("3. ❌ Problema de red/firewall")
print("4. ❌ Biblioteca python-binance desactualizada")

print("\n🎯 SOLUCIÓN RÁPIDA:")
print("1. Verifica en Binance que las API Keys existen y tienen permisos")
print("2. Si no estás seguro, crea NUEVAS API Keys")
print("3. Actualiza config_futures.json")
print("4. Prueba nuevamente")

print("\n⚠️  ¿Has verificado HOY que las API Keys siguen activas en Binance?")
