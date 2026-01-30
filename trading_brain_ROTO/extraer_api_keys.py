#!/usr/bin/env python3
"""
Extraer API Keys del archivo config.py y actualizar config_futures.json
"""
import os
import json
import re

print("🔑 EXTRACCIÓN DE API KEYS DE config.py")
print("=" * 50)

# 1. Leer config.py
config_py_file = "config.py"
if not os.path.exists(config_py_file):
    print(f"❌ {config_py_file} no encontrado")
    exit(1)

print(f"📄 Leyendo {config_py_file}...")
with open(config_py_file, 'r') as f:
    config_py_content = f.read()

# 2. Buscar API Keys usando expresiones regulares
print("\n🔍 Buscando API Keys en el contenido...")

# Patrones comunes para API Keys
patterns = {
    'api_key': [
        r'api_key\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
        r'API_KEY\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
        r'apikey\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
        r'BINANCE_API_KEY\s*[:=]\s*[\'"]([^\'"]+)[\'"]'
    ],
    'api_secret': [
        r'api_secret\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
        r'API_SECRET\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
        r'secret_key\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
        r'BINANCE_API_SECRET\s*[:=]\s*[\'"]([^\'"]+)[\'"]'
    ]
}

found_keys = {'api_key': None, 'api_secret': None}

for key_type, pattern_list in patterns.items():
    for pattern in pattern_list:
        match = re.search(pattern, config_py_content, re.IGNORECASE)
        if match:
            found_keys[key_type] = match.group(1)
            print(f"✅ {key_type.upper()} encontrada: {match.group(1)[:10]}...{match.group(1)[-4:] if len(match.group(1)) > 14 else ''}")
            break

# 3. Si no encontramos con regex, buscar líneas específicas
if not found_keys['api_key'] or not found_keys['api_secret']:
    print("\n🔍 Buscando manualmente en líneas...")
    lines = config_py_content.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        if 'api' in line_lower and 'key' in line_lower and ('=' in line or ':' in line):
            print(f"   Línea {i+1}: {line.strip()}")
        if 'secret' in line_lower and ('=' in line or ':' in line):
            print(f"   Línea {i+1}: {line.strip()}")

# 4. Si tenemos las keys, actualizar config_futures.json
config_json_file = "config_futures.json"

if os.path.exists(config_json_file):
    if found_keys['api_key'] and found_keys['api_secret']:
        print(f"\n🔄 Actualizando {config_json_file}...")
        
        with open(config_json_file, 'r') as f:
            config = json.load(f)
        
        # Guardar copia original
        with open("config_futures.json.backup", 'w') as f:
            json.dump(config, f, indent=2)
        print("   ✅ Copia de seguridad creada: config_futures.json.backup")
        
        # Actualizar con las nuevas keys
        config['binance']['api_key'] = found_keys['api_key']
        config['binance']['api_secret'] = found_keys['api_secret']
        
        with open(config_json_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("   ✅ config_futures.json actualizado con las API Keys")
        print(f"   • API Key: {found_keys['api_key'][:10]}...")
        print(f"   • API Secret: {found_keys['api_secret'][:10]}...")
        
        # Verificar que no sean los valores por defecto
        if found_keys['api_key'] == 'TU_API_KEY_AQUI' or found_keys['api_secret'] == 'TU_API_SECRET_AQUI':
            print("\n⚠️  ADVERTENCIA: Las keys parecen ser valores por defecto")
            print("   Debes usar tus API Keys reales de Binance")
    else:
        print(f"\n❌ No se pudieron extraer ambas API Keys automáticamente")
        print("📝 Por favor, actualiza config_futures.json manualmente:")
        print("   1. Abre config_futures.json")
        print("   2. Reemplaza 'TU_API_KEY_AQUI' con tu API Key real")
        print("   3. Reemplaza 'TU_API_SECRET_AQUI' con tu API Secret real")
        print("   4. Guarda el archivo")
        
        # Mostrar contenido de config.py para referencia
        print(f"\n📋 Contenido de {config_py_file} (primeras 20 líneas):")
        lines = config_py_content.split('\n')
        for i, line in enumerate(lines[:20]):
            print(f"{i+1:3d}: {line}")
else:
    print(f"\n❌ {config_json_file} no encontrado")

print("\n" + "=" * 50)
print("🎯 PRÓXIMO PASO:")
print("Ejecutar: python verificar_conexion_binance.py")
print("para verificar que la conexión funciona")
