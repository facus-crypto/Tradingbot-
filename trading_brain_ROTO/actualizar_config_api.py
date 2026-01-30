#!/usr/bin/env python3
"""
Actualizar config_futures.json con API Keys reales de config.py
"""
import json
import os

print("🔑 ACTUALIZANDO CONFIG_FUTURES.JSON CON API KEYS REALES")
print("=" * 50)

# Leer config.py para extraer API Keys
config_py_file = "config.py"
if not os.path.exists(config_py_file):
    print(f"❌ {config_py_file} no encontrado")
    exit(1)

with open(config_py_file, 'r') as f:
    lines = f.readlines()

api_key = None
api_secret = None

# Buscar las líneas específicas que vimos
for line in lines:
    if '"api_key":' in line and 'TU_API_KEY_AQUI' not in line:
        # Extraer el valor entre comillas
        parts = line.split('"')
        for i, part in enumerate(parts):
            if 'api_key' in part and i + 3 < len(parts):
                api_key = parts[i + 2]
                break
    elif '"api_secret":' in line and 'TU_API_SECRET_AQUI' not in line:
        parts = line.split('"')
        for i, part in enumerate(parts):
            if 'api_secret' in part and i + 3 < len(parts):
                api_secret = parts[i + 2]
                break

print(f"📄 API Key encontrada: {api_key[:20]}..." if api_key else "❌ API Key no encontrada")
print(f"📄 API Secret encontrada: {api_secret[:20]}..." if api_secret else "❌ API Secret no encontrada")

if not api_key or not api_secret:
    print("\n⚠️  No se pudieron extraer las API Keys")
    print("📋 Líneas relevantes de config.py:")
    for i, line in enumerate(lines[100:110], start=101):
        print(f"{i:3d}: {line.rstrip()}")
    exit(1)

# Leer y actualizar config_futures.json
config_json_file = "config_futures.json"
if not os.path.exists(config_json_file):
    print(f"❌ {config_json_file} no encontrado")
    exit(1)

print(f"\n🔄 Actualizando {config_json_file}...")

# Crear backup
backup_file = "config_futures.json.backup_" + os.popen('date +%Y%m%d_%H%M%S').read().strip()
with open(config_json_file, 'r') as f:
    config = json.load(f)

with open(backup_file, 'w') as f:
    json.dump(config, f, indent=2)
print(f"✅ Backup creado: {backup_file}")

# Actualizar con las nuevas keys
config['binance']['api_key'] = api_key
config['binance']['api_secret'] = api_secret

# Asegurar que esté en testnet para pruebas
config['binance']['testnet'] = True
print("✅ Modo Testnet activado (para pruebas seguras)")

# Guardar el archivo actualizado
with open(config_json_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ config_futures.json actualizado exitosamente")

# Verificar la actualización
print("\n🔍 VERIFICACIÓN DE LA ACTUALIZACIÓN:")
print(f"• API Key actualizada: {api_key[:15]}...{api_key[-5:]}")
print(f"• API Secret actualizada: {api_secret[:15]}...{api_secret[-5:]}")
print(f"• Testnet: {config['binance']['testnet']}")
print(f"• Modo prueba: {config['sistema']['modo_prueba']}")

print("\n" + "=" * 50)
print("🎯 PRÓXIMO PASO:")
print("Ejecutar: python verificar_conexion_binance.py")
print("para verificar que la conexión a Binance Testnet funciona")
print("\n⚠️  IMPORTANTE:")
print("1. Estas API Keys son de TESTNET (sin fondos reales)")
print("2. Para producción, necesitarás API Keys de Binance Real")
print("3. Nunca compartas tus API Keys Secret")
