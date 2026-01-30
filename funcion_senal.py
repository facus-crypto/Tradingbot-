#!/usr/bin/env python3
"""
Función para SEÑAL DE ENTRADA con botones
"""
from datetime import datetime

def generar_senal_entrada(symbol="BTCUSDT", precio=65200.00):
    """Genera mensaje de señal con botones"""
    hora = datetime.now().strftime("%H:%M:%S")
    
    # Cálculos de TP/SL
    sl = precio * 0.988  # -1.2%
    tp1 = precio * 1.032  # +3.2%
    tp2 = precio * 1.050  # +5.0%
    tp3 = precio * 1.075  # +7.5%
    
    mensaje = f"""
🚀 <b>SEÑAL ACTIVA: LONG {symbol}</b>

📥 <b>ENTRADA:</b> ${precio:,.2f} (Cierre vela 1H)
🛡️ <b>STOP LOSS:</b> ${sl:,.2f} (-1.2%)
💰 <b>TP1:</b> ${tp1:,.2f} (+3.2%) - Cerrar 40%
💰 <b>TP2:</b> ${tp2:,.2f} (+5.0%) - Cerrar 30%
💰 <b>TP3:</b> ${tp3:,.2f} (+7.5%) - Trailing EMA9

📉 <b>Métricas:</b>
• RSI 1H: 42.1 (Rebote en zona)
• Volumen: 2.1x (Fuerza confirmada)
• R/R: 1:2.7
• Riesgo: 3% de la cuenta

⏰ <b>Hora señal:</b> {hora}
"""
    
    # Botones para Telegram
    botones = [
        [("✅ EJECUTAR", "ejecutar"), ("❌ CANCELAR", "cancelar")]
    ]
    
    return mensaje, botones

# Prueba
print("📄 Ejemplo de SEÑAL:")
mensaje, botones = generar_senal_entrada()
print(mensaje)
print("Botones:", botones)
