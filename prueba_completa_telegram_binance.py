#!/usr/bin/env python3
"""
PRUEBA COMPLETA: Telegram → Binance Futures
CON CANTIDAD CORREGIDA ($100+ mínimo)
"""
import requests
import json
import time
import os
from binance.client import Client
from dotenv import load_dotenv

print("=" * 60)
print("🤖 PRUEBA COMPLETA: Telegram → Binance Futures")
print("=" * 60)

# ========== CONFIGURACIÓN ==========
TELEGRAM_TOKEN = "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw"
TELEGRAM_CHAT_ID = "213736357"

load_dotenv()
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_SECRET_KEY')
client = Client(api_key, api_secret)

# CONFIGURACIÓN CORREGIDA (mínimo $100)
SYMBOL = "BTCUSDT"
QUANTITY = 0.002  # 0.002 BTC = ~$190 (cumple mínimo $100)
# ===================================

# ========== 1. ENVIAR SEÑAL ==========
print("\n📤 1. Enviando señal a Telegram...")

mensaje_prueba = f"""
🚀 *PRUEBA DE EJECUCIÓN - {SYMBOL}*

📊 *Detalles prueba:*
• Símbolo: {SYMBOL}
• Cantidad: {QUANTITY} BTC (~$190)
• Mínimo requerido: $100 ✓
• Tipo: MARKET ORDER
• Cierre: AUTOMÁTICO después de 5 segundos

⚠️ *ADVERTENCIA:*
Esta es una PRUEBA REAL con dinero real.
Se comprará y venderá {QUANTITY} BTC inmediatamente.

*¿Ejecutar prueba?*
"""

botones = {
    "inline_keyboard": [
        [
            {"text": "✅ EJECUTAR PRUEBA", "callback_data": "ejecutar_test"},
            {"text": "❌ CANCELAR", "callback_data": "cancelar_test"}
        ]
    ]
}

try:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje_prueba,
        "parse_mode": "Markdown",
        "reply_markup": botones
    }
    
    response = requests.post(url, json=payload, timeout=10)
    
    if response.status_code == 200:
        print("✅ Señal enviada a Telegram")
        mensaje_id = response.json()["result"]["message_id"]
    else:
        print(f"❌ Error Telegram: {response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error enviando señal: {e}")
    exit(1)

# ========== 2. ESPERAR RESPUESTA ==========
print("\n⏳ 2. Esperando tu respuesta en Telegram...")
print("   Tienes 30 segundos para presionar el botón")

respuesta_recibida = None
start_time = time.time()
timeout = 30

while time.time() - start_time < timeout:
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        updates = requests.get(url, timeout=5).json()
        
        if updates.get("ok"):
            for update in updates["result"]:
                if "callback_query" in update:
                    callback = update["callback_query"]
                    if str(callback["message"]["chat"]["id"]) == TELEGRAM_CHAT_ID:
                        respuesta_recibida = callback["data"]
                        user = callback["from"].get("first_name", "Usuario")
                        
                        # Responder al callback
                        answer_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery"
                        requests.post(answer_url, json={
                            "callback_query_id": callback["id"],
                            "text": f"Recibido: {respuesta_recibida}"
                        })
                        
                        print(f"\n📱 {user} presionó: {respuesta_recibida}")
                        break
            
            if respuesta_recibida:
                break
    except:
        pass
    
    time.sleep(1)
    print(f"   ...{int(timeout - (time.time() - start_time))}s restantes", end="\r")

# ========== 3. PROCESAR RESPUESTA ==========
print("\n" + "-" * 60)

if not respuesta_recibida:
    print("⏰ Tiempo agotado - Prueba cancelada")
    
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "⏰ *TIEMPO AGOTADO*\nPrueba cancelada por inactividad.",
        "parse_mode": "Markdown"
    })
    exit(0)

if respuesta_recibida == "cancelar_test":
    print("❌ Prueba cancelada por el usuario")
    
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "❌ *PRUEBA CANCELADA*\nNo se ejecutó ninguna operación.",
        "parse_mode": "Markdown"
    })
    exit(0)

# ========== 4. EJECUTAR EN BINANCE ==========
if respuesta_recibida == "ejecutar_test":
    print("🚀 3. Ejecutando en Binance Futures...")
    
    # Mensaje inicio
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "⚡ *EJECUTANDO PRUEBA...*\nComprando 0.002 BTC en Binance Futures.",
        "parse_mode": "Markdown"
    })
    
    try:
        # Obtener precio
        ticker = client.futures_symbol_ticker(symbol=SYMBOL)
        precio_compra = float(ticker['price'])
        print(f"   💰 Precio actual: ${precio_compra:,.2f}")
        print(f"   📊 Notional: ${precio_compra * QUANTITY:,.2f} (cumple mínimo $100)")
        
        # 4.1 COMPRAR
        print(f"   📈 Comprando {QUANTITY} {SYMBOL}...")
        orden_compra = client.futures_create_order(
            symbol=SYMBOL,
            side='BUY',
            type='MARKET',
            quantity=QUANTITY
        )
        print(f"   ✅ Compra ejecutada - Order ID: {orden_compra['orderId']}")
        
        # Mensaje compra
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"✅ *COMPRA EJECUTADA*\n• {QUANTITY} BTC comprado\n• Precio: ${precio_compra:,.2f}\n• Valor: ${precio_compra * QUANTITY:,.2f}\n• Esperando 5 segundos...",
            "parse_mode": "Markdown"
        })
        
        # Esperar 5s
        time.sleep(5)
        
        # 4.2 VENDER
        print(f"   📉 Vendiendo {QUANTITY} {SYMBOL}...")
        orden_venta = client.futures_create_order(
            symbol=SYMBOL,
            side='SELL',
            type='MARKET',
            quantity=QUANTITY,
            reduceOnly='true'
        )
        
        # Precio venta
        ticker = client.futures_symbol_ticker(symbol=SYMBOL)
        precio_venta = float(ticker['price'])
        
        print(f"   ✅ Venta ejecutada - Order ID: {orden_venta['orderId']}")
        print(f"   💰 Precio venta: ${precio_venta:,.2f}")
        
        # Calcular
        resultado = precio_venta - precio_compra
        resultado_pct = (resultado / precio_compra) * 100
        resultado_usd = resultado * QUANTITY
        
        # 4.3 RESULTADO
        print("\n" + "=" * 60)
        print("📊 RESULTADO DE LA PRUEBA:")
        print(f"   Compra: ${precio_compra:,.2f}")
        print(f"   Venta:  ${precio_venta:,.2f}")
        print(f"   Diferencia por BTC: ${resultado:.2f} ({resultado_pct:.4f}%)")
        print(f"   Resultado total: ${resultado_usd:.4f} USD")
        print("=" * 60)
        
        # Mensaje final
        emoji = "🟢" if resultado > 0 else "🔴" if resultado < 0 else "⚪"
        mensaje_final = f"""
{emoji} *PRUEBA COMPLETADA - {SYMBOL}*

📊 *Resultados:*
• Compra: ${precio_compra:,.2f}
• Venta: ${precio_venta:,.2f}
• Diferencia/BTC: ${resultado:.2f} ({resultado_pct:.4f}%)
• Resultado total: ${resultado_usd:.4f}

✅ *Sistema funcionando correctamente:*
1. Telegram → Señal con botones ✓
2. Confirmación manual ✓
3. Ejecución Binance Futures ✓
4. Cierre automático ✓

🎯 *Prueba exitosa. Sistema listo para operar.*
"""
        
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": mensaje_final,
            "parse_mode": "Markdown"
        })
        
        print("\n✅ PRUEBA COMPLETADA CON ÉXITO")
        print("📱 Revisa Telegram para ver los resultados")
        
    except Exception as e:
        error_msg = f"❌ Error en Binance: {str(e)}"
        print(error_msg)
        
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"❌ *ERROR EN PRUEBA*\n{error_msg}\n\nPosible causa:\n• Saldo insuficiente\n• Mínimo no alcanzado\n• Problema de conexión",
            "parse_mode": "Markdown"
        })
