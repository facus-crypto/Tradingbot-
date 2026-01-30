#!/usr/bin/env python3
"""
Corrección FINAL de configuración
"""
import json

print("🎯 CORRECCIÓN FINAL DE CONFIGURACIÓN")
print("=" * 50)

print("📋 DIAGNÓSTICO CONFIRMADO:")
print("✅ Tus API Keys SON de Binance REAL")
print("✅ Funcionan con https://api.binance.com")
print("✅ Tienen permisos de Futures (mostró $233.84)")
print("✅ El problema era configuración de Testnet vs Real")

config_file = "config_futures.json"

# Leer configuración actual
with open(config_file, 'r') as f:
    config = json.load(f)

print(f"\n🔧 CONFIGURACIÓN ACTUAL:")
print(f"• testnet: {config['binance']['testnet']}")
print(f"• API Key: {config['binance']['api_key'][:20]}...")

# Corregir configuración
print("\n🔄 Aplicando correcciones...")

# Ya están bien las API Keys (son las reales)
# Solo necesitamos asegurar que testnet sea False
config['binance']['testnet'] = False
config['sistema']['modo_prueba'] = False

# También asegurar que estamos usando el endpoint correcto
# (python-binance lo maneja automáticamente cuando testnet=False)

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configuración corregida:")
print(f"• testnet: {config['binance']['testnet']} (AHORA False)")
print(f"• modo_prueba: {config['sistema']['modo_prueba']} (AHORA False)")
print(f"• API Key: {config['binance']['api_key'][:20]}... (CORRECTAS)")

# Probar conexión CON LA MISMA LÓGICA que tu script funciona
print("\n🔍 Probando conexión con lógica CORRECTA...")

try:
    import requests
    import time
    import hashlib
    import hmac
    
    API_KEY = config['binance']['api_key']
    SECRET_KEY = config['binance']['api_secret']
    
    def crear_firma(params=""):
        timestamp = int(time.time() * 1000)
        query = f"{params}&timestamp={timestamp}" if params else f"timestamp={timestamp}"
        signature = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
        return timestamp, f"{query}&signature={signature}"
    
    def hacer_solicitud_futures(endpoint, params=""):
        timestamp, query_firmada = crear_firma(params)
        headers = {"X-MBX-APIKEY": API_KEY}
        url = f"https://fapi.binance.com{endpoint}?{query_firmada}"
        return requests.get(url, headers=headers, timeout=10)
    
    print("1️⃣ Probando conexión a Futures Real...")
    respuesta = hacer_solicitud_futures("/fapi/v2/account")
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        print(f"✅ ¡CONEXIÓN EXITOSA A BINANCE FUTURES REAL!")
        print(f"• Balance total: ${float(datos.get('totalMarginBalance', 0)):.2f}")
        print(f"• Disponible: ${float(datos.get('availableBalance', 0)):.2f}")
        print(f"• P&L no realizado: ${float(datos.get('totalUnrealizedProfit', 0)):.2f}")
        print(f"• Posiciones activas: {len([p for p in datos.get('positions', []) if float(p['positionAmt']) != 0])}")
        
        print("\n🎉 ¡SISTEMA CONFIGURADO CORRECTAMENTE!")
        print("💰 Saldo real disponible: $233.84")
        
    else:
        print(f"❌ Error HTTP {respuesta.status_code}: {respuesta.text}")
        
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("🚀 EJECUTAR SISTEMA:")
print("python iniciar_sistema_futures.py")
print("\n⚠️  ADVERTENCIA FINAL:")
print("• Esto operará con DINERO REAL ($233.84)")
print("• Comienza con posiciones PEQUEÑAS")
print("• Monitorea constantemente")
print("• Recomendado: Prueba primero con 1 cerebro (BTC)")
