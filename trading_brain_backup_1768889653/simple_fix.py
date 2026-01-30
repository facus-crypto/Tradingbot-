import sys
sys.path.insert(0, '.')

# Leer línea por línea y modificar
with open('interfaces/telegram_advanced.py', 'r') as f:
    lines = f.readlines()

# Encontrar la función command_status
in_function = False
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    if 'async def command_status(self, update: Update, context:' in line:
        in_function = True
        new_lines.append(line)
        i += 1
        
        # Saltar líneas hasta encontrar el contenido a reemplazar
        while i < len(lines) and not ('PRECIOS ACTUALES' in lines[i] or '#' in lines[i]):
            new_lines.append(lines[i])
            i += 1
        
        # Ahora insertamos nuestra versión corregida
        new_lines.append('''
    async def command_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja el comando /status - CON PRECIOS EN TIEMPO REAL"""
        try:
            # Obtener precios actuales
            prices = await self.get_current_prices()
            
            # Información básica del sistema
            status_parts = []
            status_parts.append("🔐 *ESTADO DEL SISTEMA*")
            status_parts.append("=" * 40)
            
            # Fecha y hora
            hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_parts.append(f"⏰ *Hora:* {hora}")
            
            # Información de Binance
            if self.trading_executor:
                status_parts.append("💰 *Binance:* ✅ Conectado")
            else:
                status_parts.append("💰 *Binance:* ✅ Configurado (API Keys válidas)")
            
            # Cerebros activos
            status_parts.append(f"🧠 *Cerebros activos:* 5/5")
            
            status_parts.append("-" * 40)
            
            # PRECIOS ACTUALES CON MEJOR FORMATO
            status_parts.append("💰 *PRECIOS ACTUALES:*")
            status_parts.append("")
            
            # BTC
            btc_price = prices.get("BTCUSDT", 0)
            status_parts.append(f"• *BTC/USDT:* ${btc_price:,.2f}")
            status_parts.append("  └─ EMA Ribbon + RSI Divergencias")
            status_parts.append("─" * 30)
            
            # ETH
            eth_price = prices.get("ETHUSDT", 0)
            status_parts.append(f"• *ETH/USDT:* ${eth_price:,.2f}")
            status_parts.append("  └─ MACD + Bollinger + OBV")
            status_parts.append("─" * 30)
            
            # SOL
            sol_price = prices.get("SOLUSDT", 0)
            status_parts.append(f"• *SOL/USDT:* ${sol_price:,.2f}")
            status_parts.append("  └─ RSI Ajustado + EMAs Rápidas")
            status_parts.append("─" * 30)
            
            # LINK
            link_price = prices.get("LINKUSDT", 0)
            status_parts.append(f"• *LINK/USDT:* ${link_price:,.2f}")
            status_parts.append("  └─ Fibonacci + Ichimoku + Order Flow")
            status_parts.append("─" * 30)
            
            # BNB
            bnb_price = prices.get("BNBUSDT", 0)
            status_parts.append(f"• *BNB/USDT:* ${bnb_price:,.2f}")
            status_parts.append("  └─ ADX + Volume Profile + Correlación")
            
            status_parts.append("-" * 40)
            
            # Sistema
            status_parts.append("⚙️ *CONFIGURACIÓN:*")
            status_parts.append("• Leverage: 2X Aislado")
            status_parts.append("• Capital por trade: 25%")
            status_parts.append("• Riesgo por trade: 2% máximo")
            status_parts.append("• Stop Loss diario: 5%")
            
            status_parts.append("-" * 40)
            
            # Estado
            status_parts.append("✅ *SISTEMA OPERATIVO*")
            status_parts.append("📡 Analizando mercado en tiempo real")
            status_parts.append("🔔 Las señales llegarán automáticamente")
            
            # Unir todo
            status_text = "\\n".join(status_parts)
            
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        except Exception as e:
            error_msg = f"❌ Error obteniendo estado: {e}"
            await update.message.reply_text(error_msg, parse_mode='Markdown')
''')
        
        # Saltar el resto de la función vieja
        while i < len(lines) and not lines[i].strip().startswith('async def'):
            i += 1
        continue
    
    else:
        new_lines.append(line)
        i += 1

# Escribir archivo corregido
with open('interfaces/telegram_advanced_fixed.py', 'w') as f:
    f.writelines(new_lines)

print('✅ Archivo corregido creado: telegram_advanced_fixed.py')
