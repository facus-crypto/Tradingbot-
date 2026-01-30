#!/usr/bin/env python3
"""
Crear nuevas API Keys para solucionar el problema
"""
import json
import os

print("🔄 CREANDO NUEVAS API KEYS PARA SOLUCIONAR")
print("=" * 50)

print("📋 PASOS:")
print("1. Ve a: https://testnet.binancefuture.com/")
print("2. API Management → Create API")
print("3. Nombre: 'trading_bot_fixed'")
print("4. PERMISOS (MARCAR):")
print("   ✅ Enable Reading")
print("   ✅ Enable Spot & Margin Trading")
print("   ✅ Enable Futures")
print("   ✅ Enable Futures Trading")
print("5. IP Restriction: None")
print("6. Crea y GUARDA AMBAS CLAVES")

print("\n📝 Cuando tengas las nuevas claves, escribe:")
nueva_api = input("Nueva API Key: ").strip()
nueva_secret = input("Nueva Secret Key: ").strip()

if nueva_api and nueva_secret:
    # Actualizar configuración
    config_file = "config_futures.json"
    
    # Hacer backup
    backup = "config_futures_backup.json"
    os.system(f"cp {config_file} {backup}")
    print(f"✅ Backup creado: {backup}")
    
    # Actualizar
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    config['binance']['api_key'] = nueva_api
    config['binance']['api_secret'] = nueva_secret
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Config_futures.json actualizado")
    print(f"• Nueva API Key: {nueva_api[:20]}...")
    
    # Probar conexión inmediatamente
    print("\n🔍 Probando conexión con nuevas keys...")
    os.system("python verificar_conexion_binance.py")
    
else:
    print("\n⚠️  No se proporcionaron nuevas claves")

print("\n" + "=" * 50)
print("🎯 ESTO DEBERÍA SOLUCIONARLO.")
print("Binance a veces tiene bugs con keys viejas.")
print("Nuevas keys = problema resuelto.")
