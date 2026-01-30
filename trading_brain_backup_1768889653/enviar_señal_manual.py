import asyncio
import requests
import json

async def enviar_señal_con_botones():
    token = "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw"
    chat_id = "213736357"
    
    print("🎯 Creando señal con botones...")
    
    # Mensaje con botones inline
    mensaje = "🔔 *SEÑAL DE PRUEBA - SIMULACIÓN*\n\n" \
              "🎯 *PAR:* BTCUSDT\n" \
              "📈 *ACCIÓN:* COMPRAR\n" \
              "💰 *PRECIO ENTRADA:* $95,500.00\n" \
              "🛑 *STOP LOSS:* $95,000.00 (-0.52%)\n" \
              "🎯 *TAKE PROFIT:* $97,000.00 (+1.57%)\n" \
              "⚖️ *CANTIDAD:* 0.002 BTC (~191 USDT)\n" \
              "📊 *LEVERAGE:* 2X\n" \
              "📉 *RIESGO:* 1.5%\n\n" \
              "📝 *MOTIVO:* PRUEBA SISTEMA - RSI oversold\n" \
              "⏰ *HORA:* 23:50:00\n\n" \
              "⚠️ *MODO SIMULACIÓN - NO SE EJECUTARÁ*"
    
    # Botones inline
    keyboard = {
        "inline_keyboard": [[
            {
                "text": "✅ CONFIRMAR",
                "callback_data": "confirmar_btc_prueba"
            },
            {
                "text": "❌ CANCELAR", 
                "callback_data": "cancelar_btc_prueba"
            }
        ]]
    }
    
    # Enviar a Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(keyboard)
    }
    
    print("📤 Enviando a Telegram...")
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Señal enviada (Message ID: {result['result']['message_id']})")
        print("\n📱 EN TU TELEGRAM:")
        print("• Verás la señal completa")
        print("• Con botones ✅ CONFIRMAR / ❌ CANCELAR")
        print("• Toca ✅ CONFIRMAR para probar")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(enviar_señal_con_botones())
    print("\n🎯 PRUEBA: Toca el botón en Telegram y dime qué pasa")
