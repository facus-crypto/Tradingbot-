#!/usr/bin/env python3
"""Configurar apalancamiento 2x para todos los pares."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("🎯 CONFIGURANDO APALANCAMIENTO 2x")

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

print("✅ Binance Manager creado")

# Configurar apalancamiento 2x para todos los pares
print("\n⚙️  Configurando apalancamiento 2x...")
resultados = bm.establecer_apalancamiento_todos(leverage=2)

print("\n📊 RESULTADOS:")
for par, exito in resultados.items():
    estado = "✅" if exito else "❌"
    print(f"   {estado} {par}: {'Configurado 2x' if exito else 'Error'}")

# Verificar configuración actual
print("\n🔍 Verificando configuración actual...")
try:
    endpoint = "/fapi/v2/account"
    response = bm._hacer_solicitud(endpoint, "")
    
    if isinstance(response, dict) and 'positions' in response:
        print("📋 Apalancamiento por par:")
        for pos in response['positions']:
            if float(pos['positionAmt']) != 0 or float(pos['leverage']) != 1:
                print(f"   • {pos['symbol']}: {pos['leverage']}x")
except Exception as e:
    print(f"⚠️  Error verificando: {e}")

print("\n" + "="*50)
print("🎯 APALANCAMIENTO 2x CONFIGURADO")
print("="*50)
print("Ahora todas las operaciones usarán:")
print("• 📈 Entrada: Capital × 2")
print("• ⚠️  Riesgo: Stop Loss más amplio")
print("• 📊 Beneficio: Take Profit mayor")
print("• 🔄 Margen requerido: 50% del normal")
