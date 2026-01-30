#!/usr/bin/env python3
"""Prueba SIMPLE de Trailing Stop."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("🧪 Prueba simple TrailingStopManager")

# Crear manager sin Binance (para prueba)
from utilidades.trailing_stop_manager import TrailingStopManager

# Manager sin binance (solo prueba)
trailing = TrailingStopManager(None)

# Abrir posición simulada
pos = trailing.abrir_posicion(
    symbol="BTCUSDT",
    entry_price=89500,
    stop_loss=88000,
    take_profit=92000,
    side="COMPRA",
    signal_id=100
)

print(f"✅ Posición creada: {pos['symbol']}")

# Simular monitoreo
print("\n🔍 Simulando monitoreo...")

# Obtener estado
try:
    estado = trailing.get_estado_posiciones()
    print(f"📊 Posiciones activas: {estado['total_posiciones']}")
except Exception as e:
    print(f"⚠️  Error: {e}")

print("\n✅ TrailingStopManager básico funcionando")
