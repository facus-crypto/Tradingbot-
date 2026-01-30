#!/usr/bin/env python3
"""
Prueba con BOTONES REALES de Telegram
"""
import requests
import json

TOKEN = "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw"
CHAT_ID = "213736357"

print("🤖 Enviando SEÑAL con botones...")

# SEÑAL completa como la quieres
mensaje = """
🚀 *SEÑAL ACTIVA: LONG BTCUSDT*

📥 *ENTRADA:* $65,200.00 (Cierre vela 1H)
🛡️ *STOP LOSS:* $64,417.60 (-1.2%)
💰 *TP1:* $67,286.40 (+3.2%) - Cerrar 40%
💰 *TP2:* $68,460.00 (+5.0%) - Cerrar 30%
💰 *TP3:* $70,090.00 (+7.5%) - Trailing EMA9

📉 *Métricas:*
• RSI 1H: 42.1 (Rebote en zona)
• Volumen: 2.1x (Fuerza confirmada)
• R/R: 1:2.7
• Riesgo: 3% de la cuenta

⏰ *Confirmar ejecución:*
"""

# Botones INLINE (aparecen debajo del mensaje)
botones = {
    "inline_keyboard": [
        [
            {"text": "✅ EJECUTAR", "callback_data": "ejecutar_senal"},
            {"text": "❌ CANCELAR", "callback_data": "cancelar_senal"}
        ]
    ]
}

try:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown",  # Usar Markdown en vez de HTML
        "reply_markup": botones
    }
    
    print("📤 Enviando...")
    response = requests.post(url, json=payload, timeout=10)
    
    if response.status_code == 200:
        print("✅ ¡Señal con botones enviada! Revisa Telegram.")
        print("🎯 Deberías ver los botones [✅ EJECUTAR] [❌ CANCELAR]")
    else:
        print(f"❌ Error: {response.status_code}")
        print("Respuesta:", response.json())
        
except Exception as e:
    print(f"❌ Error: {e}")
