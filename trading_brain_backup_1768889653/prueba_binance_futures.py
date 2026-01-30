"""
Prueba de integración con Binance Futures
"""
import sys
import os
sys.path.append('.')

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_binance_integration():
    """Prueba la conexión con Binance Futures"""
    
    print("🚀 INICIANDO PRUEBA DE BINANCE FUTURES")
    print("=" * 50)
    
    try:
        # 1. Importar configuración
        import config
        print("✅ Configuración importada")
        
        # 2. Verificar que existen las API keys
        api_key = config.BINANCE_CONFIG.get("api_key", "")
        api_secret = config.BINANCE_CONFIG.get("api_secret", "")
        testnet = config.BINANCE_CONFIG.get("testnet", True)  # Por defecto usar testnet
        
        if api_key == "TU_API_KEY" or api_secret == "TU_API_SECRET":
            print("❌ ERROR: Debes configurar tus API keys en config.py")
            print("   Edita config.py y reemplaza:")
            print("   - 'TU_API_KEY' con tu API Key real")
            print("   - 'TU_API_SECRET' con tu API Secret real")
            print("\n💡 Recomendación: Usa TESTNET primero:")
            print("   1. Ve a https://testnet.binancefuture.com")
            print("   2. Crea una cuenta de prueba")
            print("   3. Genera API keys")
            print("   4. Configura testnet=True en config.py")
            return False
        
        print(f"✅ API Key configurada: {'*' * 10}{api_key[-4:]}")
        print(f"✅ Testnet: {testnet}")
        
        # 3. Importar e inicializar Binance Futures Manager
        from binance_futures import initialize_futures_manager
        
        print("\n🔄 Inicializando Binance Futures Manager...")
        manager = initialize_futures_manager(config.BINANCE_CONFIG)
        
        # 4. Probar conexión obteniendo balance
        print("\n📊 Probando conexión con Binance...")
        try:
            balance = manager.get_usdt_balance()
            print(f"✅ Conexión exitosa!")
            print(f"💰 Balance disponible (USDT): {balance:.2f}")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print("\n🔍 Posibles soluciones:")
            print("   - Verifica que las API keys sean correctas")
            print("   - Asegúrate de que la IP esté whitelisted en Binance")
            print("   - Verifica tu conexión a internet")
            return False
        
        # 5. Probar obtención de precios
        print("\n📈 Probando obtención de precios...")
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        for symbol in symbols:
            try:
                price = manager.get_symbol_price(symbol)
                print(f"   ✅ {symbol}: {price:.2f}")
            except Exception as e:
                print(f"   ❌ Error con {symbol}: {e}")
        
        # 6. Probar cálculo de tamaño de posición
        print("\n🧮 Probando cálculo de posición...")
        try:
            btc_price = manager.get_symbol_price("BTCUSDT")
            position_calc = manager.calculate_position_size(
                symbol="BTCUSDT",
                entry_price=btc_price,
                stop_loss=btc_price * 0.95  # SL del 5%
            )
            
            if position_calc:
                print(f"   ✅ Cálculo exitoso para BTCUSDT")
                print(f"     Precio entrada: {position_calc['entry_price']:.2f}")
                print(f"     Capital asignado: {position_calc['capital_allocated']:.2f} USDT")
                print(f"     Cantidad: {position_calc['quantity']:.6f}")
                print(f"     Riesgo por trade: {position_calc['risk_per_trade']:.2f} USDT")
                print(f"     Riesgo porcentual: {position_calc['risk_percent']:.2f}%")
            else:
                print("   ❌ Error en cálculo de posición")
        except Exception as e:
            print(f"   ❌ Error en cálculo: {e}")
        
        # 7. Verificar posiciones abiertas
        print("\n📋 Verificando posiciones abiertas...")
        try:
            positions = manager.get_open_positions()
            open_positions = [p for p in positions if float(p['positionAmt']) != 0]
            
            if open_positions:
                print(f"   ⚠️  Tienes {len(open_positions)} posición(es) abierta(s):")
                for pos in open_positions:
                    amount = float(pos['positionAmt'])
                    side = "LONG" if amount > 0 else "SHORT"
                    print(f"     • {pos['symbol']}: {abs(amount):.4f} ({side})")
            else:
                print("   ✅ No hay posiciones abiertas")
        except Exception as e:
            print(f"   ❌ Error obteniendo posiciones: {e}")
        
        print("\n" + "=" * 50)
        print("🎯 PRUEBA COMPLETADA EXITOSAMENTE")
        print("\n📝 RESUMEN DE CONFIGURACIÓN FUTURES:")
        print(f"   • Leverage: {manager.leverage}X")
        print(f"   • Tipo de margen: {manager.margin_type}")
        print(f"   • Porcentaje por posición: {manager.position_percent*100}%")
        print(f"   • Capital por posición: Balance * {manager.position_percent}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("   Asegúrate de que todos los módulos estén instalados")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_binance_integration()
    
    if success:
        print("\n✅ ¡Binance Futures configurado correctamente!")
        print("🎯 Ahora puedes proceder con las siguientes integraciones:")
        print("   1. Modificar cerebros para usar Futures")
        print("   2. Integrar gestión de órdenes con señales")
        print("   3. Implementar trailing stop")
    else:
        print("\n❌ La prueba falló. Corrige los errores antes de continuar.")
        
    sys.exit(0 if success else 1)
