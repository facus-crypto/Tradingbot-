#!/usr/bin/env python3
"""
Actualizar configuración con nuevas API Keys y probar conexión
"""
import json
import os
import subprocess

print("🔄 ACTUALIZANDO CONFIGURACIÓN Y PROBANDO CONEXIÓN")
print("=" * 50)

# Tus nuevas API Keys
nueva_api = "1JuwHBEThWq06lIHFnnDoHuFS6NDw45a7SMHk64X7uTlrBpkjMAPk5hiur8vLuPD"
nueva_secret = "1RUhGgywkDn4loz2BO59AGr76mEe8BrtUGQ5YI7AfaxYyMjH80r27GG1a56tmfdr"

# Verificar formato de las keys
print("🔍 Verificando nuevas API Keys...")
print(f"• API Key: {nueva_api[:20]}... (longitud: {len(nueva_api)})")
print(f"• API Secret: {nueva_secret[:20]}... (longitud: {len(nueva_secret)})")

if len(nueva_api) < 20 or len(nueva_secret) < 20:
    print("⚠️  Las keys parecen muy cortas. ¿Están completas?")
else:
    print("✅ Formato de keys OK")

# Actualizar configuración
config_file = "config_futures.json"

# 1. Hacer backup
if os.path.exists(config_file):
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"config_futures_backup_{timestamp}.json"
    
    with open(config_file, 'r') as f:
        config_backup = json.load(f)
    
    with open(backup_file, 'w') as f:
        json.dump(config_backup, f, indent=2)
    
    print(f"✅ Backup creado: {backup_file}")

# 2. Actualizar con nuevas keys
print(f"\n🔄 Actualizando {config_file}...")
with open(config_file, 'r') as f:
    config = json.load(f)

# Guardar las keys antiguas por si acaso
old_api = config['binance']['api_key']
old_secret = config['binance']['api_secret']

config['binance']['api_key'] = nueva_api
config['binance']['api_secret'] = nueva_secret
config['binance']['testnet'] = True  # Asegurar testnet

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Config_futures.json actualizado")

# 3. Probar conexión inmediatamente
print("\n🔍 Probando conexión con NUEVAS API Keys...")
print("=" * 30)

try:
    # Prueba rápida de conexión
    from binance.client import Client
    from binance.exceptions import BinanceAPIException
    
    client = Client(nueva_api, nueva_secret, testnet=True)
    
    print("1️⃣ Probando futures_exchange_info()...")
    try:
        info = client.futures_exchange_info()
        print(f"   ✅ Funciona - {len(info.get('symbols', []))} símbolos disponibles")
    except BinanceAPIException as e:
        print(f"   ❌ Error: {e.code} - {e.message}")
    
    print("\n2️⃣ Probando futures_account() (permisos de trading)...")
    try:
        account = client.futures_account()
        print(f"   ✅ ¡ÉXITO! futures_account() funciona")
        print(f"   • Balance USDT: {next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {}).get('walletBalance', 'N/A')}")
        print(f"   • Maker Commission: {account.get('makerCommission', 'N/A')}")
        print(f"   • Taker Commission: {account.get('takerCommission', 'N/A')}")
        
        print("\n🎉 ¡LAS NUEVAS API KEYS FUNCIONAN CORRECTAMENTE!")
        print("📋 Tienen todos los permisos necesarios para trading.")
        
    except BinanceAPIException as e:
        print(f"   ❌ Error: {e.code} - {e.message}")
        if e.code == -2015:
            print(f"   ⚠️  Mismo problema - falta permiso de trading")
            print(f"   💡 Asegúrate de que las nuevas keys tengan:")
            print(f"      • Enable Spot & Margin Trading")
            print(f"      • Enable Futures Trading")
        
except ImportError:
    print("❌ No se pudo importar python-binance")
except Exception as e:
    print(f"❌ Error general: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("📋 RESUMEN:")
print("• Nuevas API Keys configuradas")
print("• Config_futures.json actualizado")
print("• Backup creado con keys antiguas")

print("\n🎯 PRÓXIMO PASO:")
print("Ejecutar: python verificar_conexion_binance.py")
print("para verificación completa")
