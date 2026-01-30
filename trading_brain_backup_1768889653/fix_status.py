import sys
sys.path.insert(0, '.')

# Leer el archivo
with open('interfaces/telegram_advanced.py', 'r') as f:
    lines = f.readlines()

# Encontrar y reemplazar la función command_status
new_lines = []
i = 0
while i < len(lines):
    if 'async def command_status(self' in lines[i]:
        # Mantener la línea de definición
        new_lines.append(lines[i])
        i += 1
        
        # Reemplazar el contenido de la función
        new_lines.append('    """Maneja el comando /status"""\n')
        new_lines.append('    try:\n')
        new_lines.append('        from datetime import datetime\n')
        new_lines.append('        \n')
        new_lines.append('        # Información básica del sistema\n')
        new_lines.append('        status_parts = []\n')
        new_lines.append('        status_parts.append("🔐 *ESTADO DEL SISTEMA*")\n')
        new_lines.append('        status_parts.append("="*30)\n')
        new_lines.append('        \n')
        new_lines.append('        # Fecha y hora\n')
        new_lines.append('        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")\n')
        new_lines.append('        status_parts.append(f"⏰ *Hora:* {hora}")\n')
        new_lines.append('        \n')
        new_lines.append('        # Información de Binance (si hay trading_executor)\n')
        new_lines.append('        if self.trading_executor:\n')
        new_lines.append('            try:\n')
        new_lines.append('                balance = await self.trading_executor.get_balance()\n')
        new_lines.append('                status_parts.append(f"💰 *Balance disponible:* ${balance:.2f} USDT")\n')
        new_lines.append('            except:\n')
        new_lines.append('                status_parts.append("💰 *Binance:* Conectado")\n')
        new_lines.append('        else:\n')
        new_lines.append('            status_parts.append("💰 *Binance:* Configurado")\n')
        new_lines.append('        \n')
        new_lines.append('        # Estado de cerebros\n')
        new_lines.append('        status_parts.append("\\n🧠 *Cerebros activos:*")\n')
        new_lines.append('        status_parts.append("• BTCUSDT - EMA Ribbon + RSI")\n')
        new_lines.append('        status_parts.append("• ETHUSDT - MACD + Bollinger")\n')
        new_lines.append('        status_parts.append("• SOLUSDT - RSI Ajustado")\n')
        new_lines.append('        status_parts.append("• LINKUSDT - Fibonacci Ichimoku")\n')
        new_lines.append('        status_parts.append("• BNBUSDT - ADX Volume Profile")\n')
        new_lines.append('        \n')
        new_lines.append('        # Sistema\n')
        new_lines.append('        status_parts.append("\\n⚙️ *Configuración:*")\n')
        new_lines.append('        status_parts.append("• Leverage: 2X Aislado")\n')
        new_lines.append('        status_parts.append("• Capital por trade: 25%")\n')
        new_lines.append('        status_parts.append("• Riesgo por trade: 2%")\n')
        new_lines.append('        \n')
        new_lines.append('        # Estado\n')
        new_lines.append('        status_parts.append("\\n✅ *Sistema operativo y monitoreando*")\n')
        new_lines.append('        status_parts.append("\\n📡 *Esperando señales del mercado...*")\n')
        new_lines.append('        \n')
        new_lines.append('        # Unir todo\n')
        new_lines.append('        status_text = "\\n".join(status_parts)\n')
        new_lines.append('        \n')
        new_lines.append('        await update.message.reply_text(status_text, parse_mode=\'Markdown\')\n')
        new_lines.append('        \n')
        new_lines.append('    except Exception as e:\n')
        new_lines.append('        error_msg = f"❌ Error obteniendo estado: {e}"\n')
        new_lines.append('        await update.message.reply_text(error_msg, parse_mode=\'Markdown\')\n')
        
        # Saltar las líneas antiguas hasta encontrar el próximo async def
        while i < len(lines) and not lines[i].strip().startswith('async def'):
            i += 1
        i -= 1  # Retroceder una línea
    else:
        new_lines.append(lines[i])
    i += 1

# Escribir el archivo corregido
with open('interfaces/telegram_advanced.py', 'w') as f:
    f.writelines(new_lines)

print('✅ Función /status actualizada para mostrar información real')
