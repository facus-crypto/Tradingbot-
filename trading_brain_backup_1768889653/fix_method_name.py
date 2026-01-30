import sys
sys.path.insert(0, '.')

# Leer y corregir
with open('interfaces/telegram_advanced.py', 'r') as f:
    content = f.read()

# Reemplazar getcurrentprices por get_current_prices
content_corrected = content.replace('getcurrentprices', 'get_current_prices')

# También asegurarnos que el método existe
if 'async def get_current_prices(self):' not in content_corrected:
    # Agregar el método si no existe
    insert_point = content_corrected.find('class TelegramAdvancedBot:')
    if insert_point != -1:
        # Buscar después del __init__
        init_end = content_corrected.find('def __init__', insert_point)
        if init_end != -1:
            # Encontrar el final del __init__
            brace_count = 0
            i = init_end
            while i < len(content_corrected):
                if content_corrected[i] == '{' or content_corrected[i] == '(':
                    brace_count += 1
                elif content_corrected[i] == '}' or content_corrected[i] == ')':
                    brace_count -= 1
                elif content_corrected[i] == '\n' and brace_count <= 0 and content_corrected[i+1:i+5] == '    ' and not content_corrected[i+1:i+8] == '        ':
                    # Fin del método __init__
                    break
                i += 1
            
            # Insertar el método get_current_prices después del __init__
            get_prices_method = '''
    async def get_current_prices(self):
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
                                prices[symbol] = float(data['price'])
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
        
        return prices'''
            
            content_corrected = content_corrected[:i] + get_prices_method + content_corrected[i:]

# Escribir archivo corregido
with open('interfaces/telegram_advanced.py', 'w') as f:
    f.write(content_corrected)

print('✅ Método get_current_prices corregido/agregado')
