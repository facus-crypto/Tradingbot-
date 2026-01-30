import re

# Leer archivo actual
with open('interfaces/telegram_advanced.py', 'r') as f:
    contenido = f.read()

# Buscar dónde agregar la función (después del __init__)
patron = r"logger\.info\(f\"   • Token: \{token\[:10\]\}...\"\)\s*\n\s*\n"

if re.search(patron, contenido, re.DOTALL):
    # Encontrar la posición para insertar
    partes = re.split(patron, contenido)
    
    if len(partes) >= 2:
        # Nueva función a agregar
        nueva_funcion = '''
    # =============== FUNCIÓN SEND_SIGNAL ===============
    def send_signal(self, signal_id, symbol, side, entry, sl, tp, comment, trailing_info=None):
        """
        Envía señal con botones REALES y formato VERTICAL
        """
        try:
            import requests
            import time
            
            # LISTA VERTICAL de mercados
            monitored_symbols = ["BTC", "ETH", "SOL", "LINK", "BNB", "ADA", "AVAX", "XRP", "DOT", "ATOM"]
            symbols_list = "\\n".join([f"• {s}" for s in monitored_symbols])
            
            # Crear mensaje
            message = f"""🟡 **SEÑAL DETECTADA** 🟡

📊 **Par:** {symbol}
📈 **Dirección:** {side}
💰 **Precio Entrada:** ${entry:,.2f}
🛑 **Stop Loss:** ${sl:,.2f}
🎯 **Take Profit:** ${tp:,.2f}

📊 **Trailing Stop:**
{f"• **Fase:** {trailing_info['phase']}" if trailing_info else "• **Fase:** 1 (Inicial)"}
{f"• **SL Dinámico:** ${trailing_info.get('dynamic_sl', sl):,.2f}" if trailing_info else ""}
{f"• **TP Dinámico:** ${trailing_info.get('dynamic_tp', tp):,.2f}" if trailing_info else ""}
{f"• **PnL Actual:** {trailing_info.get('pnl_percent', 0):.2f}%" if trailing_info else ""}

📝 **Nota:** {comment}

📋 **Mercados Monitoreados:**
{symbols_list}

⏰ **Válido por:** 3 minutos"""
            
            # Enviar con botones REALES
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    'chat_id': self.chat_id,
                    'text': message,
                    'parse_mode': 'Markdown',
                    'reply_markup': {
                        'inline_keyboard': [[
                            {'text': '✅ EJECUTAR', 'callback_data': f'execute_{signal_id}'},
                            {'text': '❌ CANCELAR', 'callback_data': f'cancel_{signal_id}'}
                        ]]
                    }
                }
            ).json()
            
            if response.get('ok'):
                logger.info(f"✅ Señal {signal_id} enviada: {symbol} {side}")
                return True
            else:
                logger.error(f"❌ Error enviando señal: {response}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en send_signal: {e}")
            return False
'''
        
        # Reconstruir contenido
        nuevo_contenido = partes[0] + re.search(patron, contenido, re.DOTALL).group() + nueva_funcion + partes[1]
        
        # Guardar archivo actualizado
        with open('interfaces/telegram_advanced.py', 'w') as f:
            f.write(nuevo_contenido)
        
        print("✅ Función send_signal agregada al archivo")
    else:
        print("❌ No se pudo encontrar donde insertar la función")
else:
    print("❌ No se encontró el patrón en el archivo")
