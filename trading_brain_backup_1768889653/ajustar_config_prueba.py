#!/usr/bin/env python3
"""
Ajustar configuración para modo prueba
"""
import json
import os

archivo_config = "config_futures.json"

if not os.path.exists(archivo_config):
    print(f"❌ {archivo_config} no existe")
    exit(1)

print("🔧 AJUSTANDO CONFIGURACIÓN PARA PRUEBAS")
print("=" * 50)

# Leer configuración actual
with open(archivo_config, 'r') as f:
    config = json.load(f)

# Asegurar que está en modo prueba
config['binance']['testnet'] = True
config['sistema']['modo_prueba'] = True
config['sistema']['intervalo_analisis'] = 120  # 2 minutos para pruebas

# Desactivar Telegram si no hay token (para evitar errores)
if config['telegram']['token'] == "TU_BOT_TOKEN_AQUI":
    config['telegram']['notificar_señales'] = False
    config['telegram']['notificar_errores'] = False
    config['telegram']['notificar_cierre'] = False
    print("⚠️  Token de Telegram no configurado - notificaciones desactivadas")

# Guardar configuración actualizada
with open(archivo_config, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configuración actualizada:")
print(f"   • Testnet: {config['binance']['testnet']}")
print(f"   • Modo prueba: {config['sistema']['modo_prueba']}")
print(f"   • Intervalo análisis: {config['sistema']['intervalo_analisis']} segundos")
print(f"   • Cerebros activos: {sum(1 for c in config['cerebros'].values() if c['activo'])}/5")

# Crear también una versión de solo 1 cerebro para pruebas rápidas
config_rapida = config.copy()
for simbolo in config_rapida['cerebros']:
    if simbolo != "BTCUSDT":  # Solo dejar BTC activo para prueba rápida
        config_rapida['cerebros'][simbolo]['activo'] = False

config_rapida['sistema']['intervalo_analisis'] = 30  # 30 segundos para prueba rápida

with open("config_prueba_rapida.json", 'w') as f:
    json.dump(config_rapida, f, indent=2)

print("\n🎯 Configuración de prueba rápida creada:")
print(f"   • Archivo: config_prueba_rapida.json")
print(f"   • Solo BTCUSDT activo")
print(f"   • Intervalo: 30 segundos")

print("\n📋 OPCIONES DE EJECUCIÓN:")
print("1. Prueba completa:   python iniciar_sistema_futures.py")
print("2. Prueba rápida:     python iniciar_sistema_futures.py config_prueba_rapida.json")
