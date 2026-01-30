#!/usr/bin/env python3
"""
Función para enviar PRE-ALERTA a Telegram
"""
from datetime import datetime

def generar_prealerta(symbol="BTCUSDT"):
    """Genera mensaje de pre-alerta"""
    hora = datetime.now().strftime("%H:%M:%S")
    
    mensaje = f"""
🔍 <b>PRE-ALERTA DE TENDENCIA - {symbol}</b>

📈 <b>Filtro 4H:</b> ALCISTA (EMA 20 > EMA 50)
📊 <b>RSI 4H:</b> 54.2 (Neutral - Espacio para subir)
⚠️ <b>Estado:</b> Esperando retroceso en 1H para entrada óptima.

<i>Nota: No entrar todavía. El bot busca alineación de fuerza.</i>
⏰ <b>Hora:</b> {hora}
"""
    return mensaje

# Prueba
print("📄 Ejemplo de PRE-ALERTA:")
print(generar_prealerta())
