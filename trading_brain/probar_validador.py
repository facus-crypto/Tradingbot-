#!/usr/bin/env python3
"""Probar validador histórico."""
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

print("=== PRUEBA VALIDADOR HISTÓRICO ===\n")

# Crear validador
from utilidades.validador_historico import ValidadorHistorico
validador = ValidadorHistorico(bm)

# Crear señal de prueba
senal_prueba = {
    'par': 'BTCUSDT',
    'direccion': 'COMPRA',
    'confianza': 0.75,
    'precio_actual': 89526.70
}

print(f"🔍 Validando señal {senal_prueba['par']}...")
resultado = validador.validar_senal(senal_prueba['par'], senal_prueba, dias_backtest=30)

print(f"\n📊 RESULTADO DE VALIDACIÓN:")
print(f"   • Válida: {'✅' if resultado['valida'] else '❌'}")
print(f"   • Confianza histórica: {resultado['confianza_historica']}")
print(f"   • Profit Factor: {resultado['profit_factor_simulado']}")
print(f"   • Win Rate: {resultado['win_rate']}%")
print(f"   • Trades simulados: {resultado['trades_simulados']}")
print(f"   • Razón: {resultado['razon']}")
print(f"   • Muestras: {resultado['datos_muestras']} velas")
print(f"   • Precio medio: {resultado['precio_medio']}")
print(f"   • Volatilidad: {resultado['volatilidad']}%")

print("\n" + "="*50)
print("✅ VALIDADOR HISTÓRICO FUNCIONANDO")
print("="*50)
