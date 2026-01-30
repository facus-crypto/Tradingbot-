#!/usr/bin/env python3
"""Probar función helper send_signal con recarga."""
import sys
import importlib

# Forzar recarga del módulo
if 'interfaces.telegram_advanced' in sys.modules:
    importlib.reload(sys.modules['interfaces.telegram_advanced'])

from interfaces.telegram_advanced import send_signal

print("🔍 Probando función send_signal (recargado)...")

# Probar enviar señal
signal_id = 1000  # Nuevo ID
symbol = "BTCUSDT"
side = "COMPRAR"
entry = 89526.70
sl = 91317.23
tp = 85945.63
comment = "Prueba del sistema RESTAURADO"

print(f"📤 Enviando señal #{signal_id}...")
print(f"   Par: {symbol}")
print(f"   Acción: {side}")

success = send_signal(signal_id, symbol, side, entry, sl, tp, comment)

if success:
    print("\n" + "="*50)
    print("✅ ✅ ✅ SEÑAL ENVIADA A TELEGRAM ✅ ✅ ✅")
    print("="*50)
    print("Revisa tu bot de Telegram ahora.")
else:
    print("\n❌ Error enviando señal")
