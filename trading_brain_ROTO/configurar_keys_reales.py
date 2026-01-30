#!/usr/bin/env python3
"""
Configurar las API Keys REALES de Binance
"""
import json

print("🔑 CONFIGURAR API KEYS REALES DE BINANCE")
print("=" * 50)

print("📋 SITUACIÓN:")
print("• Tienes API Keys de TESTNET configuradas")
print("• Tienes API Keys de REAL (mostraron saldo $233.84)")
print("• Necesitamos usar las REALES")

print("\n🎯 PASO 1: Obtener tus API Keys REALES")
print("1. Ve a: https://www.binance.com/")
print("2. API Management")
print("3. Busca tus API Keys REALES")
print("4. Asegúrate que tengan:")
print("   • Enable Spot & Margin Trading")
print("   • Enable Futures")
print("   • Enable Futures Trading")

print("\n🎯 PASO 2: Ingresar las nuevas claves")
api_real = input("\nAPI Key REAL de Binance: ").strip()
secret_real = input("Secret Key REAL de Binance: ").strip()

if not api_real or not secret_real:
    print("❌ No se ingresaron las claves")
    exit(1)

# Actualizar configuración
config_file = "config_futures.json"

with open(config_file, 'r') as f:
    config = json.load(f)

print(f"\n🔄 Actualizando {config_file}...")
config['binance']['api_key'] = api_real
config['binance']['api_secret'] = secret_real
config['binance']['testnet'] = False
config['sistema']['modo_prueba'] = False

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configuración actualizada")
print(f"• API Key: {api_real[:20]}...")
print(f"• Modo: REAL (testnet: False)")

# Probar conexión REAL
print("\n🔍 Probando conexión REAL...")

try:
    from binance.client import Client
    
    client = Client(api_real, secret_real)  # Binance REAL
    
    print("1️⃣ Conectando a Binance Futures Real...")
    account = client.futures_account()
    
    print(f"✅ ¡CONEXIÓN REAL EXITOSA!")
    print(f"• Balance USDT: {next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {}).get('walletBalance', 'N/A')}")
    
    print("\n🎉 ¡SISTEMA LISTO PARA TRADING REAL!")
    print("💰 Saldo disponible en tu cuenta")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Posibles causas:")
    print("   • API Keys sin permisos de Futures")
    print("   • Restricción de IP")
    print("   • Keys incorrectas")

print("\n" + "=" * 50)
print("📋 RESUMEN FINAL:")
print("1. Sistema configurado para Binance REAL")
print("2. Usa API Keys REALES (no de testnet)")
print("3. Modo prueba: DESACTIVADO")
print("4. Operará con DINERO REAL")

print("\n🚀 EJECUTAR SISTEMA:")
print("python iniciar_sistema_futures.py")
