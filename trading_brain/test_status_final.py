#!/usr/bin/env python3
"""Prueba FINAL del comando /status."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("🎯 Prueba FINAL comando /status")

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

# Importar NUEVO
from interfaces.telegram_advanced import TelegramAdvancedBot

bot = TelegramAdvancedBot(
    config['telegram']['token'],
    config['telegram']['chat_id']
)

print("1. Enviando estado del sistema...")
if bot.send_status():
    print("   ✅ Estado enviado")
else:
    print("   ❌ Error")

print("\n2. Enviando mensaje con botones de prueba...")
if bot.send_test_buttons():
    print("   ✅ Botones enviados")
else:
    print("   ❌ Error")

print("\n3. Enviando señal de prueba...")
if bot.send_signal(
    signal_id=9999,
    symbol="BTCUSDT",
    side="COMPRAR",
    entry=89500.50,
    sl=88000.00,
    tp=92000.00,
    comment="Prueba del sistema completo"
):
    print("   ✅ Señal enviada")
else:
    print("   ❌ Error")

print("\n" + "="*50)
print("🎉 Todos los comandos probados")
print("Revisa tu Telegram (@facusssss_bot)")
print("Deberías ver 3 mensajes:")
print("1. ✅ Estado del sistema")
print("2. 📋 Mensaje con botones PROBAR/TEST")
print("3. 🚨 Señal de trading con botones")
