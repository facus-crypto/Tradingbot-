#!/usr/bin/env python3
"""Probar función helper send_signal."""
import sys
sys.path.append('.')

from interfaces.telegram_advanced import send_signal

print("🔍 Probando función send_signal...")

# Probar enviar señal
signal_id = 999
symbol = "BTCUSDT"
side = "COMPRAR"
entry = 89526.70
sl = 91317.23
tp = 85945.63
comment = "Prueba del sistema restaurado"

print(f"📤 Enviando señal #{signal_id}...")
print(f"   Par: {symbol}")
print(f"   Acción: {side}")

success = send_signal(signal_id, symbol, side, entry, sl, tp, comment)

if success:
    print("✅ ✅ ✅ SEÑAL ENVIADA A TELEGRAM ✅ ✅ ✅")
    print("Revisa tu bot de Telegram ahora.")
else:
    print("❌ Error enviando señal")
