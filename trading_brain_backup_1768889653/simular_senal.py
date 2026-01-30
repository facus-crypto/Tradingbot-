import requests
import json
from datetime import datetime

# Configuración
TOKEN = "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw"
CHAT_ID = "213736357"

# Crear mensaje de señal
def enviar_senal(tipo="COMPRA", simbolo="BTCUSDT", precio=45000, stop_loss=44500, take_profit=46000):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if tipo == "COMPRA":
        emoji = "🟢"
        titulo = "🚨 SEÑAL DE COMPRA"
    else:
        emoji = "🔴"
        titulo = "🚨 SEÑAL DE VENTA"
    
    mensaje = f"""
{titulo} {emoji}

📊 **Par:** {simbolo}
💰 **Precio Actual:** ${precio:,.2f}
🎯 **Stop Loss:** ${stop_loss:,.2f}
🎯 **Take Profit:** ${take_profit:,.2f}
📈 **Risk/Reward:** 1:2
⚡ **Leverage:** 2x

🛡️ **Protección:**
- Stop Loss: -1.0%
- Take Profit 1: +1.5%
- Take Profit 2: +2.2%

📊 **Indicadores:**
• RSI: 32 (Oversold)
• MACD: Bullish crossover
• EMA Ribbon: Alineación alcista
• Volumen: Alto

⏰ **Hora:** {timestamp}
🔐 **Estado:** CONFIRMADA

#️⃣ #{simbolo.replace('USDT', '')} #{tipo}
    """
    
    # Enviar a Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown",
        "disable_notification": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Señal {tipo} enviada a Telegram")
            print(f"   Par: {simbolo}")
            print(f"   Precio: ${precio}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error enviando: {e}")

# Simular diferentes señales
print("📡 Enviando señales de prueba a Telegram...")
print("-" * 50)

# Señal 1: COMPRA BTC
enviar_senal(
    tipo="COMPRA",
    simbolo="BTCUSDT",
    precio=45234.56,
    stop_loss=44500,
    take_profit=46500
)

print("-" * 50)

# Señal 2: VENTA ETH
enviar_senal(
    tipo="VENTA",
    simbolo="ETHUSDT",
    precio=2456.78,
    stop_loss=2500,
    take_profit=2400
)

print("-" * 50)
print("🎯 Simulación completada")
print("📱 Revisa tu Telegram para ver las señales")
