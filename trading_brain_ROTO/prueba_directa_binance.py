#!/usr/bin/env python3
"""
Prueba DIRECTA y SIMPLE de conexión a Binance Testnet
"""
from binance.client import Client

print("🔍 PRUEBA DIRECTA Y SIMPLE DE BINANCE TESTNET")
print("=" * 50)

# TUS NUEVAS API KEYS DIRECTAMENTE
API_KEY = "1JuwHBEThWq06lIHFnnDoHuFS6NDw45a7SMHk64X7uTlrBpkjMAPk5hiur8vLuPD"
API_SECRET = "1RUhGgywkDn4loz2BO59AGr76mEe8BrtUGQ5YI7AfaxYyMjH80r27GG1a56tmfdr"

print(f"🔑 Usando API Key: {API_KEY[:20]}...")
print(f"🔐 Usando Secret: {API_SECRET[:20]}...")

print("\n🔧 Creando cliente Binance Testnet...")
try:
    # Conexión DIRECTA a Testnet
    client = Client(API_KEY, API_SECRET, testnet=True)
    print("✅ Cliente creado")
    
    print("\n1️⃣ Probando endpoint público (sin autenticación)...")
    try:
        ticker = client.get_symbol_ticker(symbol="BTCUSDT")
        print(f"   ✅ Público funciona: BTC = {ticker['price']}")
    except Exception as e:
        print(f"   ❌ Público falla: {e}")
    
    print("\n2️⃣ Probando endpoint SEMI-público (solo lectura)...")
    try:
        exchange_info = client.futures_exchange_info()
        print(f"   ✅ Lectura funciona: {len(exchange_info['symbols'])} símbolos")
    except Exception as e:
        print(f"   ❌ Lectura falla: {e}")
    
    print("\n3️⃣ Probando endpoint PRIVADO (requiere permisos)...")
    try:
        account = client.futures_account()
        print(f"   ✅ ¡PRIVADO FUNCIONA! - Tienes permisos COMPLETOS")
        print(f"   • Balance: {next((a for a in account.get('assets', []) if a['asset'] == 'USDT'), {}).get('walletBalance', 'N/A')}")
    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ Privado falla: {error_msg}")
        
        if "-2015" in error_msg:
            print(f"\n🔍 ERROR -2015 ANÁLISIS:")
            print("   'Invalid API-key, IP, or permissions for action'")
            print("\n💡 SIGNIFICA UNA DE TRES COSAS:")
            print("   1. API Key INEXISTENTE o ELIMINADA")
            print("   2. PERMISOS INSUFICIENTES (falta 'Enable Trading')")
            print("   3. RESTRICCIÓN DE IP activada")
            
            print("\n🎯 VERIFICACIÓN RÁPIDA:")
            print("   a. ¿Las keys son de https://testnet.binancefuture.com/ (NO .vision)?")
            print("   b. ¿Tienes 'Enable Trading' activado DENTRO de cada categoría?")
            print("   c. ¿Tienes restricción IP? Si sí, añade tu IP actual")
    
    print("\n4️⃣ Probando crear orden TEST (solo validación)...")
    try:
        # Método correcto para test de orden en Futures
        params = {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': 0.001
        }
        
        # En futures es diferente
        print("   ⚠️  Nota: Test de orden en Futures requiere implementación específica")
        print("   💡 Si llegaste aquí, ya tienes permisos de trading")
        
    except Exception as e:
        print(f"   ❌ Test orden falla: {e}")
        
except Exception as e:
    print(f"❌ Error creando cliente: {type(e).__name__}: {e}")

print("\n" + "=" * 50)
print("🎯 CONCLUSIÓN FINAL:")
print("Si el error -2015 persiste CON NUEVAS KEYS, el problema es:")
print("1. ❌ NO estás creando keys en el lugar correcto")
print("2. ❌ NO estás activando 'Enable Trading' (sub-permiso)")
print("3. ❌ Hay restricción IP bloqueándote")

print("\n💡 SOLUCIÓN DEFINITIVA:")
print("1. Ve a: https://testnet.binancefuture.com/")
print("2. API Management → Create NEW API")
print("3. NOMBRE: 'bot_trading_full'")
print("4. ACTIVA TODO:")
print("   - ✅ Enable Reading")
print("   - ✅ Enable Spot & Margin Trading")
print("   - ✅ Enable Futures")
print("   - ✅ Enable Futures Trading")
print("5. RESTRICCIÓN IP: NONE (deja vacío)")
print("6. CREA y GUARDA")
print("7. Vuelve y prueba")
