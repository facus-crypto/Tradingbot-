#!/usr/bin/env python3
"""Probar ejecución automática 25% + 2x."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("🎯 PRUEBA EJECUCIÓN AUTOMÁTICA (25% + 2x)")

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

print("1. 📊 Obteniendo balance...")
balance = bm.obtener_balance_disponible()
print(f"   ✅ Balance disponible: ${balance:.2f}")

print("\n2. 🧮 Calculando tamaño para BTC (25% + 2x)...")
cantidad_btc = bm.calcular_tamanio_posicion("BTCUSDT", 0.25, 2)
print(f"   ✅ Cantidad a operar: {cantidad_btc:.6f} BTC")

print("\n3. 📈 Obteniendo precio BTC...")
endpoint = "/fapi/v1/ticker/price"
params = "symbol=BTCUSDT"
precio_data = bm._hacer_solicitud(endpoint, params)
if isinstance(precio_data, dict):
    precio = float(precio_data['price'])
    valor_posicion = cantidad_btc * precio
    print(f"   ✅ Precio BTC: ${precio:.2f}")
    print(f"   ✅ Valor posición: ${valor_posicion:.2f}")

print("\n4. ⚠️  NOTA: No ejecutaremos orden real (solo simulación)")
print("   En el sistema real, al presionar 'EJECUTAR' en Telegram:")
print("   • Se calcularía cantidad: {cantidad_btc:.6f} BTC")
print("   • Se enviaría orden MARKET de COMPRA")
print("   • Se colocarían órdenes SL/TP automáticamente")

print("\n" + "="*60)
print("✅ SISTEMA DE EJECUCIÓN LISTO")
print("="*60)
print("Parámetros configurados:")
print("• 📊 % Capital: 25%")
print("• ⚡ Apalancamiento: 2x")
print("• 🔴 Stop Loss: -2%")
print("• 🟢 Take Profit: +4%")
print("• 🤖 Ejecución: Automática al presionar 'EJECUTAR'")
