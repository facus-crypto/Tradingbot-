#!/usr/bin/env python3
"""Probar cerebro BTC con datos REALES de Binance."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

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

print("=== PRUEBA BTC CON DATOS REALES ===\n")

# Probar BTC con datos reales
from cerebros.cerebro_btc_futures import CerebroBTCFutures

cerebro_btc = CerebroBTCFutures(config, bm, None)
print(f"🧠 Cerebro: {cerebro_btc.symbol}")
print(f"📊 Estrategia: {cerebro_btc.nombre_estrategia}")

resultado = cerebro_btc.analizar()
if resultado:
    print(f"\n✅ ANÁLISIS COMPLETO:")
    print(f"   • Dirección: {resultado['direccion']}")
    print(f"   • Confianza: {resultado['confianza']}")
    print(f"   • Precio: {resultado['precio_actual']:.2f}")
    print(f"   • RSI: {resultado['indicadores']['rsi']}")
    print(f"   • EMA8: {resultado['indicadores']['ema8']:.2f}")
    print(f"   • EMA55: {resultado['indicadores']['ema55']:.2f}")
    print(f"   • Spread 8-55: {resultado['indicadores']['spread_8_55']}%")
    
    if resultado['direccion'] != "NEUTRAL":
        print(f"\n🎯 NIVELES DE TRADING:")
        print(f"   • Entrada: {resultado['niveles']['entrada']:.2f}")
        print(f"   • Stop Loss: {resultado['niveles']['stop_loss']:.2f}")
        print(f"   • Take Profit: {resultado['niveles']['take_profit']:.2f}")
else:
    print("❌ Sin resultado")
