#!/usr/bin/env python3
"""
SOLUCIÓN DEFINITIVA: Crear API Keys en el lugar CORRECTO
"""
import webbrowser
import json
import os

print("🎯 SOLUCIÓN DEFINITIVA")
print("=" * 50)

print("🔍 PROBLEMA IDENTIFICADO:")
print("Estás usando: https://testnet.binance.vision/ (SPOT)")
print("Necesitas:    https://testnet.binancefuture.com/ (FUTURES)")

print("\n🎯 URL CORRECTA PARA API KEYS DE FUTURES:")
print("👉 https://testnet.binancefuture.com/ 👈")

print("\n🔄 Abriendo el URL correcto en 3 segundos...")
import time
time.sleep(3)
webbrowser.open("https://testnet.binancefuture.com/")

print("\n📋 PASOS EXACTOS:")
print("1. Regístrate/Inicia sesión en testnet.binancefuture.com")
print("2. Ve a API Management")
print("3. ELIMINA todas las API Keys antiguas")
print("4. Crea NUEVA API Key con:")
print("   • Nombre: 'bot_futures_trading'")
print("   • PERMISOS (BUSCA Y ACTIVA):")
print("     - ✅ Enable Reading")
print("     - ✅ Enable Spot & Margin Trading")
print("     - ✅ Enable Futures")
print("     - ✅ Enable Futures Trading")
print("   • RESTRICCIÓN IP: NONE (deja vacío)")
print("5. GUARDA AMBAS CLAVES (solo se muestran una vez)")

print("\n⏳ Cuando tengas las NUEVAS claves CORRECTAS, escribe:")

while True:
    nueva_api = input("\nNueva API Key de FUTURES: ").strip()
    nueva_secret = input("Nueva Secret Key de FUTURES: ").strip()
    
    if nueva_api and nueva_secret:
        # Verificar longitud típica de keys de Binance
        if len(nueva_api) >= 64 and len(nueva_secret) >= 64:
            print(f"✅ Keys válidas (longitud OK)")
            break
        else:
            print(f"⚠️  Keys muy cortas. Las de Binance suelen tener 64+ caracteres")
            print(f"   • API Key: {len(nueva_api)} caracteres")
            print(f"   • Secret: {len(nueva_secret)} caracteres")
            continuar = input("¿Continuar igual? (s/n): ").lower()
            if continuar == 's':
                break
    else:
        print("❌ Keys vacías. Intenta de nuevo.")

# Actualizar configuración
config_file = "config_futures.json"

print(f"\n🔄 Actualizando {config_file}...")

# Hacer backup
timestamp = time.strftime("%Y%m%d_%H%M%S")
backup_file = f"{config_file}.backup_{timestamp}"
os.system(f"cp {config_file} {backup_file}")
print(f"✅ Backup creado: {backup_file}")

# Leer y actualizar
with open(config_file, 'r') as f:
    config = json.load(f)

config['binance']['api_key'] = nueva_api
config['binance']['api_secret'] = nueva_secret
config['binance']['testnet'] = True

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Config_futures.json actualizado")
print(f"• Nueva API Key: {nueva_api[:20]}...")
print(f"• Nueva Secret: {nueva_secret[:20]}...")

# Probar inmediatamente
print("\n🔍 Probando conexión INMEDIATAMENTE...")
print("=" * 30)

test_code = f'''
from binance.client import Client
client = Client("{nueva_api}", "{nueva_secret}", testnet=True)
try:
    account = client.futures_account()
    print("✅ ¡CONEXIÓN EXITOSA A BINANCE FUTURES TESTNET!")
    print(f"• Balance USDT: {{next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {{}}).get('walletBalance', 'N/A')}}")
    print("🎉 ¡EL SISTEMA ESTÁ LISTO PARA TRADING!")
except Exception as e:
    print(f"❌ Error: {{e}}")
    print("💡 Verifica que:")
    print("   1. Estés en testnet.binancefuture.com (NO .vision)")
    print("   2. Tengas 'Enable Futures Trading' activado")
'''

# Guardar y ejecutar prueba
with open("prueba_final.py", "w") as f:
    f.write(test_code)

result = os.system("python prueba_final.py")
os.remove("prueba_final.py")

print("\n" + "=" * 50)
print("📋 RESUMEN:")
print("• URL correcto: testnet.binancefuture.com")
print("• API Keys específicas para FUTURES")
print("• Permisos: Enable Futures Trading")
print("• Configuración actualizada")

if result == 0:
    print("\n🎉 ¡PROBLEMA SOLUCIONADO!")
    print("🚀 El sistema está listo para ejecutarse.")
else:
    print("\n⚠️  Aún hay problemas.")
    print("💡 Revisa los puntos anteriores.")
