#!/usr/bin/env python3
"""
ESTRUCTURA CEREBRO CUÁNTICO - Base
"""
import requests
import time
import json
from datetime import datetime
from telegram import Bot

print("🧠 Estructura cerebro creada")

# ========== CONFIGURACIÓN ==========
TELEGRAM_TOKEN = "PON_TU_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "PON_TU_CHAT_ID_AQUI"
# ===================================

# Lista de monedas
MONEDAS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "LINKUSDT"]

print("Monedas configuradas:", MONEDAS)

# ========== FUNCIONES BÁSICAS ==========
def enviar_telegram(mensaje):
    """Envía mensaje a Telegram"""
    print(f"📤 Telegram: {mensaje[:50]}...")

def obtener_precio(symbol):
    """Obtiene precio actual de Binance"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=5)
        precio = float(response.json()['price'])
        return precio
    except:
        return 0

def obtener_velas(symbol, intervalo="1h", limite=100):
    """Obtiene velas históricas para análisis"""
    try:
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": intervalo,
            "limit": limite
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except:
        return []
# =======================================

# ========== NIVEL 1: FILTROS DE MERCADO ==========
def verificar_tendencia_btc():
    """Verifica tendencia general del mercado (BTC)"""
    try:
        velas = obtener_velas("BTCUSDT", "4h", 50)
        if len(velas) < 20:
            return "INDETERMINADA"
        
        # Calcular EMA 20 y 50
        precios = [float(v[4]) for v in velas]  # Precios de cierre
        
        # EMA simple (para ejemplo)
        if len(precios) >= 20:
            ema_20 = sum(precios[-20:]) / 20
            ema_50 = sum(precios[-50:]) / 50 if len(precios) >= 50 else ema_20
            
            if precios[-1] > ema_20 > ema_50:
                return "ALCISTA_FUERTE"
            elif precios[-1] < ema_20 < ema_50:
                return "BAJISTA_FUERTE"
            elif precios[-1] > ema_20:
                return "ALCISTA_LEVE"
            else:
                return "BAJISTA_LEVE"
    except:
        pass
    
    return "NEUTRAL"

def obtener_miedo_codicia():
    """Obtiene índice Fear & Greed (simulado)"""
    try:
        # En realidad usarías una API, pero simulamos
        return 65  # 65 = Greed (apetito por riesgo)
    except:
        return 50

def filtro_mercado():
    """Filtro general del mercado"""
    print("\n🔍 NIVEL 1: Filtros de Mercado")
    
    # 1. Tendencia BTC
    tendencia = verificar_tendencia_btc()
    print(f"   📈 Tendencia BTC: {tendencia}")
    
    # 2. Fear & Greed
    fg = obtener_miedo_codicia()
    print(f"   😨 Fear & Greed: {fg}/100")
    
    # 3. Reglas
    mercado_ok = True
    razones = []
    
    if "BAJISTA_FUERTE" in tendencia:
        razones.append("Tendencia BTC muy bajista")
        mercado_ok = False
    
    if fg < 25:  # Extreme Fear
        razones.append("Miedo extremo en mercado")
        mercado_ok = False
    
    if fg > 85:  # Extreme Greed
        razones.append("Codicia extrema (posible corrección)")
        mercado_ok = False
    
    return mercado_ok, razones, {"tendencia": tendencia, "fear_greed": fg}
# =================================================

# ========== EJECUCIÓN ==========
print("\n" + "="*60)
print("🤖 CEREBRO CUÁNTICO - INICIANDO ANÁLISIS")
print("="*60)

# Prueba funciones básicas
for moneda in MONEDAS[:2]:
    precio = obtener_precio(moneda)
    print(f"   {moneda}: ${precio:,.2f}")

# Aplicar filtros de mercado
mercado_ok, razones, datos = filtro_mercado()

if mercado_ok:
    print("\n✅ MERCADO: CONDICIONES ACEPTABLES")
    enviar_telegram("✅ Mercado: Condiciones aceptables para trading")
else:
    print(f"\n⚠️ MERCADO: NO OPERAR - {', '.join(razones)}")
    enviar_telegram(f"⚠️ Mercado: No operar - {', '.join(razones)}")

print("\n🧠 Nivel 1 completado. Listo para Nivel 2 (indicadores específicos).")
