import requests
import json

def get_binance_prices(symbols):
    """Obtiene precios actuales de Binance"""
    prices = {}
    
    for symbol in symbols:
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                prices[symbol] = float(data['price'])
            else:
                prices[symbol] = 0.0
        except:
            prices[symbol] = 0.0
    
    return prices

# Probar
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT", "BNBUSDT"]
prices = get_binance_prices(symbols)

print("💰 Precios actuales Binance:")
for symbol, price in prices.items():
    print(f"  {symbol}: ${price:,.2f}")
