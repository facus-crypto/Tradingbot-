#!/usr/bin/env python3
"""
Verificar conexión a Binance con las API Keys existentes
"""
import sys
import os

# Añadir directorio actual al path
sys.path.append('.')

print("🔍 VERIFICANDO CONEXIÓN A BINANCE")
print("=" * 50)

try:
    # Intentar importar la biblioteca de Binance
    print("1️⃣ Probando importación de bibliotecas...")
    from binance.client import Client
    from binance.exceptions import BinanceAPIException
    print("   ✅ python-binance instalado")
    
    # Verificar si tenemos módulo propio
    try:
        from binance_manager import BinanceFuturesManager
        print("   ✅ binance_manager encontrado")
        tiene_binance_manager = True
    except ImportError:
        print("   ⚠️  binance_manager no encontrado, usando python-binance directamente")
        tiene_binance_manager = False
    
except ImportError as e:
    print(f"   ❌ Error de importación: {e}")
    print("\n💡 INSTALACIÓN NECESARIA:")
    print("   pip install python-binance")
    exit(1)

# Verificar credenciales en configuración
config_file = "config_futures.json"
if os.path.exists(config_file):
    import json
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    api_key = config['binance']['api_key']
    api_secret = config['binance']['api_secret']
    testnet = config['binance']['testnet']
    
    print(f"\n2️⃣ Credenciales encontradas:")
    print(f"   • API Key: {'✅ CONFIGURADA' if api_key and api_key != 'TU_API_KEY_AQUI' else '❌ NO CONFIGURADA'}")
    print(f"   • API Secret: {'✅ CONFIGURADA' if api_secret and api_secret != 'TU_API_SECRET_AQUI' else '❌ NO CONFIGURADA'}")
    print(f"   • Testnet: {'✅ ACTIVADO' if testnet else '❌ DESACTIVADO (modo real)'}")
    
    if api_key and api_key != 'TU_API_KEY_AQUI' and api_secret and api_secret != 'TU_API_SECRET_AQUI':
        print("\n3️⃣ Probando conexión a Binance...")
        try:
            # Probar conexión con python-binance directamente
            if testnet:
                print("   Conectando a Binance Testnet...")
                client = Client(api_key, api_secret, testnet=True)
                endpoint = "https://testnet.binancefuture.com"
            else:
                print("   Conectando a Binance Real...")
                client = Client(api_key, api_secret)
                endpoint = "https://fapi.binance.com"
            
            # Hacer una llamada simple
            try:
                account_info = client.futures_account()
                print(f"   ✅ Conexión exitosa!")
                print(f"   • Endpoint: {endpoint}")
                print(f"   • Maker Commission: {account_info.get('makerCommission', 'N/A')}")
                print(f"   • Taker Commission: {account_info.get('takerCommission', 'N/A')}")
                
                # Verificar balance
                assets = account_info.get('assets', [])
                usdt_balance = next((a for a in assets if a['asset'] == 'USDT'), None)
                if usdt_balance:
                    print(f"   • Balance USDT: {float(usdt_balance['walletBalance']):.2f}")
                else:
                    print("   • Balance USDT: No encontrado")
                
            except BinanceAPIException as e:
                print(f"   ❌ Error de API: {e.code} - {e.message}")
                print("   💡 Posibles causas:")
                print("      - API Keys inválidas")
                print("      - Permisos insuficientes (necesita Futures habilitado)")
                print("      - IP no autorizada")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
    else:
        print("\n⚠️  Configura primero las API Keys en config_futures.json")
        
else:
    print(f"❌ {config_file} no encontrado")

print("\n" + "=" * 50)
print("📋 Siguiente paso: Si la conexión funciona, podemos")
print("   ejecutar el sistema con conexión real a Binance")
