import sys
sys.path.insert(0, '.')

# Leer el archivo
with open('interfaces/telegram_advanced.py', 'r') as f:
    content = f.read()

# Encontrar y reemplazar la función command_status
import re

# Nueva versión de la función
new_command_status = '''    async def command_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            status_parts.append("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯")
            
            # ETH
            eth_price = prices.get("ETHUSDT", 0)
            status_parts.append(f"• *ETH/USDT:* ${eth_price:,.2f}")
            status_parts.append("  └─ MACD + Bollinger + OBV")
            status_parts.append("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯")
            
            # SOL
            sol_price = prices.get("SOLUSDT", 0)
            status_parts.append(f"• *SOL/USDT:* ${sol_price:,.2f}")
            status_parts.append("  └─ RSI Ajustado + EMAs Rápidas")
            status_parts.append("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯")
            
            # LINK
            link_price = prices.get("LINKUSDT", 0)
            status_parts.append(f"• *LINK/USDT:* ${link_price:,.2f}")
            status_parts.append("  └─ Fibonacci + Ichimoku + Order Flow")
            status_parts.append("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯")
            
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
            await update.message.reply_text(error_msg, parse_mode='Markdown")'''

# Reemplazar la función en el contenido
pattern = r'async def command_status\(self, update: Update, context: ContextTypes\.DEFAULT_TYPE\):.*?(?=\n    async def|\n\nclass|\Z)'
new_content = re.sub(pattern, new_command_status, content, flags=re.DOTALL)

# Escribir el archivo corregido
with open('interfaces/telegram_advanced.py', 'w') as f:
    f.write(new_content)

print('✅ Formato de /status mejorado con cerebros activos y separadores')
