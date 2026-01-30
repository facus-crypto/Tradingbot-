import sys
sys.path.append('.')
import asyncio

async def prueba_correcta():
    from binance_manager_custom import get_binance_manager
    from cerebros.cerebro_btc_futures import CerebroBTC
    
    # Leer configuración
    import json
    with open("config_futures.json", 'r') as f:
        config = json.load(f)
    
    api_key = config["binance"]["api_key"]
    api_secret = config["binance"]["api_secret"]
    testnet = config["binance"]["testnet"]
    
    print(f"🔑 API Key: {api_key[:20]}...")
    print(f"🌐 Testnet: {testnet}")
    
    # Crear manager
    manager = get_binance_manager(api_key, api_secret, testnet)
    print(f"✅ Manager creado")
    
    # Crear cerebro CON manager
    cerebro = CerebroBTC(binance_manager=manager)
    print(f"✅ Cerebro BTC creado con manager")
    
    # Obtener precio
    try:
        precio = await cerebro.obtener_precio_actual()
        print(f"💰 Precio BTC: {precio}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

resultado = asyncio.run(prueba_correcta())
print(f"\n🎯 Resultado: {'✅ ÉXITO' if resultado else '❌ FALLO'}")
