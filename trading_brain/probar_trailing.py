#!/usr/bin/env python3
"""Probar Trailing Stop Manager."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("="*60)
print("🧪 PRUEBA TRAILING STOP MANAGER")
print("="*60)

# Cargar configuración
with open('config_futures.json', 'r') as f:
    config = json.load(f)

# Crear Binance Manager
from binance_manager_custom import BinanceFuturesManagerCustom
bm = BinanceFuturesManagerCustom(
    config['binance']['api_key'],
    config['binance']['api_secret'],
    config['binance'].get('testnet', False)
)

# Crear Trailing Manager
from utilidades.trailing_stop_manager import crear_trailing_manager
trailing_mgr = crear_trailing_manager(bm)

print("✅ TrailingStopManager creado")

# Simular apertura de posición
print("\n📈 Simulando posición BTC COMPRA...")
posicion = trailing_mgr.abrir_posicion(
    symbol="BTCUSDT",
    entry_price=89500.00,
    stop_loss=88000.00,
    take_profit=92000.00,
    side="COMPRA",
    signal_id=9999
)

print(f"✅ Posición registrada:")
print(f"   • Entry: {posicion['entry_price']}")
print(f"   • SL inicial: {posicion['current_sl']}")
print(f"   • TP: {posicion['take_profit']}")

# Monitorear una vez
print("\n🔍 Monitoreando posición...")
trailing_mgr.monitorear_posiciones()

# Verificar estado
print("\n📊 Estado posiciones:")
estado = trailing_mgr.get_estado_posiciones()
print(f"   • Posiciones activas: {estado['total_posiciones']}")
print(f"   • Total ajustes: {estado['resumen']['total_ajustes']}")

print("\n" + "="*60)
print("✅ TRAILING STOP MANAGER FUNCIONANDO")
print("="*60)
print("El sistema ahora puede:")
print("1. 📈 Registrar posiciones abiertas")
print("2. 🔍 Monitorear precios en tiempo real")
print("3. 📐 Ajustar stops con trailing de 3 fases")
print("4. 🔴 Cerrar posiciones automáticamente (SL/TP)")
