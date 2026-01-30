#!/usr/bin/env python3
"""
Verificar estructura de inicialización y corregir
"""
import sys
sys.path.append('.')

print("🔍 VERIFICANDO ESTRUCTURA DE INICIALIZACIÓN")
print("=" * 50)

# Probar cómo se inicializa en el sistema principal
print("1️⃣ Probando inicialización del sistema...")

try:
    from core.sistema_principal_futures import SistemaPrincipalFutures
    import asyncio
    
    async def test():
        sistema = SistemaPrincipalFutures()
        
        # Inicializar binance
        print("  Inicializando Binance...")
        binance_ok = await sistema.inicializar_binance()
        print(f"  Binance: {'✅' if binance_ok else '❌'}")
        
        if binance_ok and sistema.binance_manager:
            print(f"  Manager creado: {type(sistema.binance_manager).__name__}")
            
            # Inicializar cerebros
            print("  Inicializando cerebros...")
            cerebros_ok = await sistema.inicializar_cerebros()
            print(f"  Cerebros: {'✅' if cerebros_ok else '❌'}")
            
            if cerebros_ok and sistema.cerebros:
                print(f"  Cerebros creados: {len(sistema.cerebros)}")
                
                # Probar un cerebro
                cerebro_btc = sistema.cerebros.get('BTCUSDT')
                if cerebro_btc:
                    print(f"  Cerebro BTC tiene binance: {'✅' if cerebro_btc.binance else '❌'}")
                    
                    # Probar obtener precio
                    print("  Probando obtener precio...")
                    try:
                        precio = await cerebro_btc.obtener_precio_actual()
                        print(f"  Precio BTC: {precio}")
                    except Exception as e:
                        print(f"  ❌ Error precio: {e}")
    
    asyncio.run(test())
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n2️⃣ Verificando problema específico...")
print("   Los cerebros necesitan binance_manager para funcionar")
print("   En sistema_principal_futures.py se pasa durante inicialización")

print("\n3️⃣ Solución probar directamente con manager:")
print("   from binance_manager_custom import get_binance_manager")
print("   from cerebros.cerebro_btc_futures import CerebroBTC")
print("   ")
print("   manager = get_binance_manager(api_key, api_secret, testnet=False)")
print("   cerebro = CerebroBTC(binance_manager=manager)")
print("   precio = await cerebro.obtener_precio_actual()")

print("\n" + "=" * 50)
print("🎯 EJECUTAR PRUEBA CORRECTA:")

test_code = '''
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
print(f"\\n🎯 Resultado: {'✅ ÉXITO' if resultado else '❌ FALLO'}")
'''

with open("prueba_correcta.py", "w") as f:
    f.write(test_code)

print("python prueba_correcta.py")
