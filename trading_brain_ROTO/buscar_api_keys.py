#!/usr/bin/env python3
"""
Buscar API Keys de Binance en diferentes ubicaciones
"""
import os
import sys

print("🔍 BUSCANDO API KEYS DE BINANCE")
print("=" * 50)

# 1. Verificar variables de entorno
print("\n1️⃣ Variables de entorno:")
env_vars = ['BINANCE_API_KEY', 'BINANCE_API_SECRET', 'BINANCE_TESTNET']
for var in env_vars:
    value = os.environ.get(var)
    if value:
        print(f"   ✅ {var}: {'*' * 10}{value[-4:] if len(value) > 4 else '***'}")
    else:
        print(f"   ❌ {var}: No definida")

# 2. Verificar archivos comunes de configuración
print("\n2️⃣ Archivos de configuración comunes:")
config_files = [
    'config.py',
    'config.json', 
    'config_binance.py',
    'binance_config.py',
    '.env',
    'secrets.py'
]

for file in config_files:
    if os.path.exists(file):
        print(f"   ✅ {file}: Existe")
        # Mostrar primeras líneas si es pequeño
        if os.path.getsize(file) < 10000:  # Menos de 10KB
            with open(file, 'r') as f:
                content = f.read()
                if 'API' in content or 'KEY' in content or 'SECRET' in content:
                    print(f"      → Contiene términos relacionados con API")
    else:
        print(f"   ❌ {file}: No existe")

# 3. Verificar directorio actual por archivos .py que puedan contener config
print("\n3️⃣ Buscando en archivos Python locales...")
import glob
py_files = glob.glob("*.py")
for py_file in py_files:
    if os.path.getsize(py_file) < 5000:  # Archivos pequeños
        with open(py_file, 'r') as f:
            content = f.read().lower()
            if 'binance' in content and ('api_key' in content or 'api_secret' in content):
                print(f"   🔍 {py_file}: Posible configuración de Binance")

# 4. Verificar config_futures.json específicamente
print("\n4️⃣ Archivo config_futures.json:")
if os.path.exists("config_futures.json"):
    import json
    try:
        with open("config_futures.json", 'r') as f:
            config = json.load(f)
        
        api_key = config['binance']['api_key']
        api_secret = config['binance']['api_secret']
        
        if api_key and api_key != 'TU_API_KEY_AQUI':
            print(f"   ✅ API Key: Configurada")
            print(f"      → {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
        else:
            print(f"   ❌ API Key: NO configurada (usa valor por defecto)")
            
        if api_secret and api_secret != 'TU_API_SECRET_AQUI':
            print(f"   ✅ API Secret: Configurada")
            print(f"      → {api_secret[:10]}...{api_secret[-4:] if len(api_secret) > 14 else ''}")
        else:
            print(f"   ❌ API Secret: NO configurada (usa valor por defecto)")
            
    except Exception as e:
        print(f"   ❌ Error leyendo config_futures.json: {e}")
else:
    print(f"   ❌ config_futures.json no existe")

print("\n" + "=" * 50)
print("📝 INSTRUCCIONES:")
print("1. Si tienes las API Keys en otro archivo, cópialas a config_futures.json")
print("2. Si están en variables de entorno, podemos leerlas desde ahí")
print("3. Si no las tienes, créalas en Binance Testnet")

print("\n🛠️  SOLUCIÓN RÁPIDA:")
print("Edita config_futures.json y reemplaza:")
print('  "api_key": "TU_API_KEY_AQUI",')
print('  "api_secret": "TU_API_SECRET_AQUI",')
print("con tus claves reales")
