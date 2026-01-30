#!/usr/bin/env python3
"""
PRUEBA DE SEÑAL CON BOTONES Y FORMATO VERTICAL
"""

import sys
import os
import time
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 PRUEBA DE SEÑAL CON BOTONES")
print("="*50)

try:
    # Importar la función send_signal
    from interfaces.telegram_advanced import send_signal
    print("✅ Módulo telegram_advanced cargado")
    
except Exception as e:
    print(f"❌ Error importando: {e}")
    sys.exit(1)

# Crear ID único para la señal
signal_id = f"BTC_{int(time.time())}"
print(f"📋 Signal ID: {signal_id}")

# Información de trailing stop
trailing_info = {
    'phase': 1,
    'dynamic_sl': 67053.07,
    'dynamic_tp': 70474.15,
    'pnl_percent': 0.45
}

print("📤 Enviando señal con botones...")

# Enviar señal con botones
success = send_signal(
    signal_id=signal_id,
    symbol="BTCUSDT",
    side="LONG",
    entry=68421.50,
    sl=67053.07,
    tp=70474.15,
    comment="🔴 SEÑAL DE PRUEBA - EMA Ribbon + RSI divergence detectada",
    trailing_info=trailing_info
)

if success:
    print("\n✅ SEÑAL ENVIADA EXITOSAMENTE")
    print("📱 Ahora revisa Telegram. Deberías ver:")
    print("   • Lista VERTICAL de mercados (con puntos)")
    print("   • Botones '✅ EJECUTAR' y '❌ CANCELAR'")
    print("   • Información completa de Trailing Stop")
    print("   • Precios de entrada, SL y TP")
    print("\n🖱️ Prueba los botones haciendo clic en ellos")
else:
    print("\n❌ Error al enviar la señal")
    print("   Revisando logs...")
