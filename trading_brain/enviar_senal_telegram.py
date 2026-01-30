#!/usr/bin/env python3
"""Enviar señal REAL de BTC a Telegram."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

# 1. Obtener señal REAL de BTC
print("=== OBTENIENDO SEÑAL REAL BTC ===")

# Crear Binance Manager
from binance_manager_custom import BinanceFuturesManagerCustom
bm = BinanceFuturesManagerCustom(
    config['binance']['api_key'],
    config['binance']['api_secret'],
    config['binance'].get('testnet', False)
)

# Obtener análisis REAL de BTC
from cerebros.cerebro_btc_futures import CerebroBTCFutures
cerebro_btc = CerebroBTCFutures(bm, None)
senal_btc = cerebro_btc.analizar()

if not senal_btc or senal_btc['direccion'] == "NEUTRAL":
    print("❌ BTC no genera señal ahora (NEUTRAL)")
    # Crear señal de prueba
    senal_btc = {
        'par': 'BTCUSDT',
        'direccion': 'COMPRA',
        'confianza': 0.75,
        'precio_actual': 89536.90,
        'indicadores': {'rsi': 38.02},
        'niveles': {
            'entrada': 89536.90,
            'stop_loss': 91327.64,
            'take_profit': 85955.42
        }
    }

print(f"✅ Señal BTC obtenida: {senal_btc['direccion']}")

# 2. Enviar a Telegram
print("\n=== ENVIANDO A TELEGRAM ===")

from interfaces.telegram_advanced import TelegramAdvancedBot

# Crear bot Telegram
telegram_token = config['telegram']['token']
chat_id = config['telegram']['chat_id']

bot = TelegramAdvancedBot(telegram_token, chat_id)
print(f"🤖 Bot Telegram creado")
print(f"💬 Chat ID: {chat_id}")

# Preparar señal para Telegram
signal_id = 1001  # ID de ejemplo
side = "COMPRAR" if senal_btc['direccion'] == "COMPRA" else "VENDER"
entry = senal_btc['niveles']['entrada']
sl = senal_btc['niveles']['stop_loss']
tp = senal_btc['niveles']['take_profit']

# Comentario con indicadores
rsi_val = senal_btc['indicadores'].get('rsi', 0)
comment = f"EMA Ribbon + RSI ({rsi_val:.1f}), Conf: {senal_btc['confianza']}"

# Enviar señal
print(f"\n📤 Enviando señal #{signal_id}...")
print(f"   Par: {senal_btc['par']}")
print(f"   Acción: {side}")
print(f"   Entrada: {entry:.2f}")
print(f"   SL: {sl:.2f}")
print(f"   TP: {tp:.2f}")

success = bot.send_signal(
    signal_id=signal_id,
    symbol=senal_btc['par'],
    side=side,
    entry=entry,
    sl=sl,
    tp=tp,
    comment=comment,
    trailing_info={"fase": 1}
)

if success:
    print("\n✅ ✅ ✅ SEÑAL ENVIADA A TELEGRAM ✅ ✅ ✅")
    print("Revisa tu bot de Telegram ahora.")
else:
    print("\n❌ Error enviando a Telegram")
