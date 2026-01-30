#!/usr/bin/env python3
"""Probar sistema COMPLETO con validador integrado."""
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)

print("="*60)
print("🧠 SISTEMA COMPLETO CON VALIDADOR HISTÓRICO")
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

# Crear Telegram Bot
from interfaces.telegram_advanced import TelegramAdvancedBot
telegram_bot = TelegramAdvancedBot(
    config['telegram']['token'],
    config['telegram']['chat_id']
)

print("✅ Componentes inicializados")

# Probar BTC con validador
print("\n🔍 Probando BTC con validador histórico...")
from cerebros.cerebro_btc_futures import CerebroBTCFutures

cerebro_btc = CerebroBTCFutures(bm, telegram_bot)
senal_btc = cerebro_btc.analizar()

if senal_btc and senal_btc['direccion'] != "NEUTRAL":
    print(f"✅ BTC generó señal: {senal_btc['direccion']} (conf: {senal_btc['confianza']})")
    
    # Validar señal
    validacion = cerebro_btc.validar_senal_con_historico(senal_btc)
    
    print(f"\n📊 VALIDACIÓN HISTÓRICA:")
    print(f"   • Válida: {'✅' if validacion['valida'] else '❌'}")
    print(f"   • Confianza combinada: {validacion['confianza_combinada']:.2f}")
    print(f"   • Razón: {validacion['razon']}")
    
    if validacion['valida']:
        print(f"\n📤 Enviando señal validada a Telegram...")
        enviado = cerebro_btc.enviar_senal_con_validacion(senal_btc)
        
        if enviado:
            print("✅ ✅ ✅ SEÑAL ENVIADA A TELEGRAM CON VALIDACIÓN ✅ ✅ ✅")
            print("Revisa tu bot de Telegram (@facusssss_bot)")
        else:
            print("❌ Error enviando señal")
    else:
        print("⏹️  Señal no enviada (no pasó validación)")
else:
    print("⚠️  BTC no genera señal ahora")

print("\n" + "="*60)
print("🎯 SISTEMA COMPLETO CON VALIDADOR - LISTO")
print("="*60)
print("Cada cerebro ahora:")
print("1. ✅ Analiza datos REALES de Binance")
print("2. ✅ Valida con histórico (backtesting)")
print("3. ✅ Envía solo señales validadas a Telegram")
print("4. ✅ Muestra métricas de confianza combinada")
