#!/usr/bin/env python3
"""Probar comando /status de Telegram."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("🧪 Probando comando /status...")

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

# Crear bot Telegram
from interfaces.telegram_advanced import TelegramAdvancedBot
bot = TelegramAdvancedBot(
    config['telegram']['token'],
    config['telegram']['chat_id']
)

print(f"✅ Bot creado para chat: {config['telegram']['chat_id']}")

# Enviar estado
print("\n📤 Enviando estado del sistema...")
exito = bot.send_status(
    cerebros_activos=10,
    modo="Señales manuales",
    trailing_configurado=True,
    mercados=["BTC", "ETH", "SOL", "LINK", "BNB", "ADA", "AVAX", "XRP", "DOT", "ATOM"]
)

if exito:
    print("✅ ✅ ✅ ESTADO ENVIADO A TELEGRAM ✅ ✅ ✅")
    print("Revisa tu bot (@facusssss_bot) - Deberías ver:")
    print("• ✅ SISTEMA OPERATIVO")
    print("• 10 cerebros activos")
    print("• Modo: Señales manuales")
    print("• Trailing stop configurado")
    print("• Lista de 10 mercados")
else:
    print("❌ Error enviando estado")

# También probar botones de prueba
print("\n🎯 Enviando mensaje con botones de prueba...")
exito_botones = bot.send_test_buttons()
if exito_botones:
    print("✅ Botones de prueba enviados")
