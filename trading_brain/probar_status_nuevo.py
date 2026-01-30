#!/usr/bin/env python3
"""Probar comando /status con recarga."""
import sys
import importlib

# Forzar recarga del módulo
if 'interfaces.telegram_advanced' in sys.modules:
    importlib.reload(sys.modules['interfaces.telegram_advanced'])

import json
import logging

logging.basicConfig(level=logging.INFO)

print("🧪 Probando comando /status (recargado)...")

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

# Importar después de recargar
from interfaces.telegram_advanced import TelegramAdvancedBot
bot = TelegramAdvancedBot(
    config['telegram']['token'],
    config['telegram']['chat_id']
)

print(f"✅ Bot creado para chat: {config['telegram']['chat_id']}")

# Enviar estado
print("\n📤 Enviando estado del sistema...")
try:
    exito = bot.send_status(
        cerebros_activos=10,
        modo="Señales manuales",
        trailing_configurado=True
    )
    
    if exito:
        print("✅ ✅ ✅ ESTADO ENVIADO A TELEGRAM ✅ ✅ ✅")
        print("Revisa @facusssss_bot ahora")
    else:
        print("❌ Error enviando estado")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ Prueba completada")
