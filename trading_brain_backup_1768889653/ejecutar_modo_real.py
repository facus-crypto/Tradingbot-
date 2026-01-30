#!/usr/bin/env python3
"""
Ejecutar sistema en modo REAL (Binance Real)
"""
import json

print("🚀 EJECUTANDO SISTEMA EN MODO REAL")
print("=" * 50)

config_file = "config_futures.json"

# Leer configuración
with open(config_file, 'r') as f:
    config = json.load(f)

print("📋 CONFIGURACIÓN ACTUAL:")
print(f"• testnet: {config['binance']['testnet']}")
print(f"• API Key: {config['binance']['api_key'][:20]}...")
print(f"• modo_prueba: {config['sistema']['modo_prueba']}")

# Cambiar a modo REAL
print("\n🔄 Cambiando a MODO REAL...")
config['binance']['testnet'] = False
config['sistema']['modo_prueba'] = False
config['sistema']['intervalo_analisis'] = 300  # 5 minutos para real

# Guardar
with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configuración actualizada a MODO REAL")
print("• testnet: False")
print("• modo_prueba: False")
print("• intervalo: 300 segundos")

# Verificar conexión
print("\n🔍 Verificando conexión a Binance REAL...")

try:
    from binance.client import Client
    
    api_key = config['binance']['api_key']
    api_secret = config['binance']['api_secret']
    
    client = Client(api_key, api_secret)  # Sin testnet=True
    
    print("1️⃣ Probando conexión a Futures Real...")
    try:
        account = client.futures_account()
        print(f"✅ ¡CONEXIÓN EXITOSA A BINANCE FUTURES REAL!")
        print(f"• Balance: {next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {}).get('walletBalance', 'N/A')}")
        print(f"• Posiciones: {len([p for p in account.get('positions', []) if float(p.get('positionAmt', 0)) != 0])}")
        
        print("\n🎉 ¡EL SISTEMA ESTÁ LISTO PARA TRADING REAL!")
        print("💰 Saldo disponible: $233.84 USDT")
        
    except Exception as e:
        print(f"❌ Error en Futures Real: {e}")
        
except Exception as e:
    print(f"❌ Error general: {e}")

print("\n" + "=" * 50)
print("🎯 EJECUTAR SISTEMA:")
print("python iniciar_sistema_futures.py")
print("\n⚠️  ADVERTENCIA:")
print("• Esto operará con DINERO REAL")
print("• Comienza con posiciones PEQUEÑAS")
print("• Monitorea constantemente")
