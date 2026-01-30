#!/usr/bin/env python3
"""
Diagnosticar problema con API Keys de Binance
"""
import os
import json
from binance.client import Client
from binance.exceptions import BinanceAPIException

print("🔧 DIAGNÓSTICO DE API KEYS DE BINANCE")
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

print(f"📋 INFORMACIÓN DE CONFIGURACIÓN:")
print(f"• API Key: {api_key[:15]}...{api_key[-5:]}")
print(f"• API Secret: {api_key[:15]}...{api_secret[-5:]}")
print(f"• Testnet: {'✅ ACTIVADO' if testnet else '❌ DESACTIVADO'}")

print("\n🔍 PROBANDO DIFERENTES ENDPOINTS...")

# Probar diferentes combinaciones
endpoints = [
    ("Binance Spot Testnet", "https://testnet.binance.vision", False),
    ("Binance Futures Testnet", "https://testnet.binancefuture.com", True),
    ("Binance Spot Real", "https://api.binance.com", False),
    ("Binance Futures Real", "https://fapi.binance.com", True)
]

for endpoint_name, endpoint_url, is_futures in endpoints:
    print(f"\n🔄 Probando: {endpoint_name}")
    print(f"   URL: {endpoint_url}")
    
    try:
        if testnet and 'testnet' in endpoint_name.lower():
            client = Client(api_key, api_secret, testnet=is_futures)
        elif not testnet and 'testnet' not in endpoint_name.lower():
            client = Client(api_key, api_secret)
        else:
            print("   ⏭️  Saltando (no coincide con modo testnet)")
            continue
        
        # Probar endpoint específico
        if is_futures:
            try:
                account = client.futures_account()
                print(f"   ✅ CONEXIÓN EXITOSA A FUTURES!")
                print(f"   • Maker Commission: {account.get('makerCommission', 'N/A')}")
                print(f"   • Taker Commission: {account.get('takerCommission', 'N/A')}")
                
                # Verificar balance
                assets = account.get('assets', [])
                usdt_balance = next((a for a in assets if a['asset'] == 'USDT'), None)
                if usdt_balance:
                    print(f"   • Balance USDT: {float(usdt_balance['walletBalance']):.2f}")
                
                # Verificar posiciones
                positions = account.get('positions', [])
                active_positions = [p for p in positions if float(p['positionAmt']) != 0]
                print(f"   • Posiciones activas: {len(active_positions)}")
                
                return
                
            except BinanceAPIException as e:
                print(f"   ❌ Error Futures API: {e.code} - {e.message}")
                if e.code == -2015:
                    print(f"   💡 Las API Keys no tienen acceso a FUTURES")
                continue
                
        else:
            try:
                account = client.get_account()
                print(f"   ✅ CONEXIÓN EXITOSA A SPOT!")
                print(f"   • Maker Commission: {account.get('makerCommission', 'N/A')}")
                print(f"   • Taker Commission: account.get('takerCommission', 'N/A')}")
                
                # Verificar balances
                balances = account.get('balances', [])
                usdt_balance = next((b for b in balances if b['asset'] == 'USDT'), None)
                if usdt_balance:
                    print(f"   • Balance USDT Spot: {float(usdt_balance['free']):.2f}")
                
                return
                
            except BinanceAPIException as e:
                print(f"   ❌ Error Spot API: {e.code} - {e.message}")
                continue
                
    except Exception as e:
        print(f"   ❌ Error general: {e}")

print("\n" + "=" * 50)
print("📋 RESUMEN Y SOLUCIONES:")
print("\n❌ PROBLEMA: Las API Keys no funcionan con Binance Futures")
print("\n💡 SOLUCIONES:")
print("1. CREAR NUEVAS API KEYS EN BINANCE TESTNET FUTURES:")
print("   a. Ve a: https://testnet.binancefuture.com/")
print("   b. Regístrate/Inicia sesión")
print("   c. Ve a: API Management")
print("   d. Crea nueva API Key con:")
print("      - Permisos: Enable Trading")
print("      - Restricción IP: Ninguna (o añade tu IP)")
print("      - Guarda las nuevas claves")

print("\n2. VERIFICAR QUE LAS API KEYS SON PARA FUTURES:")
print("   • Las API Keys de Binance Spot NO funcionan con Futures")
print("   • Necesitas API Keys específicas de Binance Futures")

print("\n3. VERIFICAR RESTRICCIONES DE IP:")
print("   • Si configuraste restricción IP, añade tu IP actual")
print("   • O crea nuevas API Keys sin restricción IP")

print("\n🛠️  PRÓXIMOS PASOS:")
print("1. Crea nuevas API Keys en Binance Futures Testnet")
print("2. Actualiza config_futures.json con las nuevas claves")
print("3. Ejecuta python verificar_conexion_binance.py nuevamente")
