#!/usr/bin/env python3
"""
Prueba FINAL de Telegram con datos REALES
"""
import requests

# Configuración REAL encontrada en bot.py
TOKEN = "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw"
CHAT_ID = "213736357"

print("🤖 Enviando mensaje de prueba a Telegram...")

# Mensaje como lo quieres
mensaje = """
🔍 <b>PRE-ALERTA DE TENDENCIA - BTCUSDT</b>

📈 <b>Filtro 4H:</b> ALCISTA (EMA 20 > EMA 50)
📊 <b>RSI 4H:</b> 54.2 (Neutral - Espacio para subir)
⚠️ <b>Estado:</b> Esperando retroceso en 1H para entrada óptima.

<i>Nota: No entrar todavía. El bot busca alineación de fuerza.</i>
"""

try:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    
    response = requests.post(url, json=payload, timeout=10)
    
    if response.status_code == 200:
        print("✅ ¡Mensaje enviado! Revisa Telegram.")
        print("🎯 Deberías ver la PRE-ALERTA con formato HTML.")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"❌ Error: {e}")
