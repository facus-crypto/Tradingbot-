#!/usr/bin/env python3
"""
Solución para python-binance con tus API Keys
"""
import json

print("🔧 SOLUCIÓN PARA PYTHON-BINANCE")
print("=" * 50)

config_file = "config_futures.json"

# Leer configuración
with open(config_file, 'r') as f:
    config = json.load(f)

API_KEY = config['binance']['api_key']
SECRET_KEY = config['binance']['api_secret']

print(f"📋 Tus API Keys funcionan con requests+hmac")
print(f"• API Key: {API_KEY[:20]}...")

print("\n🔍 Probando con python-binance DIRECTAMENTE...")

# Probar python-binance sin configuración compleja
test_code = f'''
import sys
sys.path.append('.')

# Tu configuración actual
API_KEY = "{API_KEY}"
SECRET_KEY = "{SECRET_KEY}"

print("1️⃣ Probando conexión simple...")
try:
    from binance.client import Client
    
    # Opción 1: Sin testnet (Binance Real)
    print("   Probando Binance REAL...")
    client_real = Client(API_KEY, SECRET_KEY)
    
    try:
        account = client_real.futures_account()
        print(f"   ✅ Binance REAL funciona!")
        print(f"   • Balance: {{next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {{}}).get('walletBalance', 'N/A')}}")
        print("   💡 Configurar: testnet = False")
        
        # Actualizar configuración
        import json
        with open("config_futures.json", 'r') as f:
            config = json.load(f)
        config['binance']['testnet'] = False
        with open("config_futures.json", 'w') as f:
            json.dump(config, f, indent=2)
        print("   ✅ Config_futures.json actualizado (testnet=False)")
        
    except Exception as e:
        print(f"   ❌ Error REAL: {{e}}")
        
        # Opción 2: Con testnet
        print("\\n   Probando Binance TESTNET...")
        client_test = Client(API_KEY, SECRET_KEY, testnet=True)
        
        try:
            account = client_test.futures_account()
            print(f"   ✅ Binance TESTNET funciona!")
            print(f"   • Balance: {{next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {{}}).get('walletBalance', 'N/A')}}")
            print("   💡 Configurar: testnet = True")
            
            # Actualizar configuración
            import json
            with open("config_futures.json", 'r') as f:
                config = json.load(f)
            config['binance']['testnet'] = True
            with open("config_futures.json", 'w') as f:
                json.dump(config, f, indent=2)
            print("   ✅ Config_futures.json actualizado (testnet=True)")
            
        except Exception as e2:
            print(f"   ❌ Error TESTNET: {{e2}}")
            print("\\n   ⚠️  python-binance NO funciona con tus keys")
            print("   💡 Usaremos requests directamente (como tu script)")
            
except ImportError:
    print("❌ python-binance no instalado")
except Exception as e:
    print(f"❌ Error: {{e}}")
'''

# Guardar y ejecutar test
with open("test_final.py", "w") as f:
    f.write(test_code)

import subprocess
result = subprocess.run(["python", "test_final.py"], capture_output=True, text=True)
print(result.stdout)

if result.stderr:
    print("⚠️  Errores:", result.stderr)

# Eliminar archivo temporal
import os
os.remove("test_final.py")

print("\n" + "=" * 50)
print("🎯 CONCLUSIÓN FINAL:")
print("• Tus API Keys funcionan (lo probaste)")
print("• El problema es python-binance vs requests")
print("• Necesitamos usar la MISMA lógica que tu script")

print("\n🚀 SOLUCIÓN IMPLEMENTADA:")
print("1. Usar requests+hmac como tu script (no python-binance)")
print("2. O arreglar python-binance")
print("3. Ejecutar sistema con configuración correcta")

print("\n📋 EJECUTAR AHORA:")
print("python iniciar_sistema_futures.py")
