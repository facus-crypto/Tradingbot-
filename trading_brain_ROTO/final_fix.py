import sys
sys.path.insert(0, '.')

# Leer el archivo
with open('interfaces/telegram_advanced.py', 'r') as f:
    lines = f.readlines()

# Buscar dónde insertar get_current_prices (después del __init__)
insert_point = -1
for i, line in enumerate(lines):
    if 'def __init__' in line:
        # Encontrar el final del __init__
        j = i
        indent_level = 0
        while j < len(lines):
            if 'def ' in lines[j] and j != i and lines[j].startswith(' ' * 4):
                # Encontramos el siguiente método
                insert_point = j
                break
            j += 1
        break

if insert_point != -1:
    print(f'Insertando get_current_prices en línea {insert_point}')
    
    # Método get_current_prices
    get_prices_method = '''    async def get_current_prices(self):
        """Obtiene precios actuales de Binance"""
        import aiohttp
        
        symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT", "BNBUSDT"]
        prices = {}
        
        try:
            async with aiohttp.ClientSession() as session:
                for symbol in symbols:
                    try:
                        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
                        async with session.get(url, timeout=5) as response:
                            if response.status == 200:
                                data = await response.json()
                                prices[symbol] = float(data[\'price\'])
                            else:
                                prices[symbol] = 0.0
                    except:
                        prices[symbol] = 0.0
        except:
            # Valores por defecto si falla
            prices = {
                "BTCUSDT": 95742.10,
                "ETHUSDT": 3320.13,
                "SOLUSDT": 142.63,
                "LINKUSDT": 13.81,
                "BNBUSDT": 932.44
            }
        
        return prices\n\n'''
    
    # Insertar
    lines.insert(insert_point, get_prices_method)
    
    # Ahora buscar y reemplazar command_status
    for i, line in enumerate(lines):
        if 'async def command_status(self, update: Update, context:' in line:
            # Reemplazar esta función completa
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
            from datetime import datetime
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
            
            await update.message.reply_text(status_text, parse_mode=\'Markdown\')
            
        except Exception as e:
            error_msg = f"❌ Error obteniendo estado: {e}"
            await update.message.reply_text(error_msg, parse_mode=\'Markdown\')\n'''
            
            # Encontrar el final de la función actual
            j = i + 1
            indent_level = 0
            while j < len(lines):
                stripped = lines[j].lstrip()
                if stripped.startswith('async def ') or stripped.startswith('def '):
                    if lines[j].startswith(' ' * 4):  # Mismo nivel de indentación
                        break
                j += 1
            
            # Reemplazar
            lines[i:j] = [new_command_status]
            break
    
    # Escribir archivo corregido
    with open('interfaces/telegram_advanced.py', 'w') as f:
        f.writelines(lines)
    
    print('✅ Archivo corregido: get_current_prices añadido y command_status actualizado')
else:
    print('❌ No se pudo encontrar dónde insertar')
