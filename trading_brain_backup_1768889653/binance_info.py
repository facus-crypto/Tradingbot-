import requests
import time
import hashlib
import hmac
import json

API_KEY = "1JuwHBEThWq06lIHFnnDoHuFS6NDw45a7SMHk64X7uTlrBpkjMAPk5hiur8vLuPD"
SECRET_KEY = "1RUhGgywkDn4loz2BO59AGr76mEe8BrtUGQ5YI7AfaxYyMjH80r27GG1a56tmfdr"

def crear_firma(params=""):
    timestamp = int(time.time() * 1000)
    query = f"{params}&timestamp={timestamp}" if params else f"timestamp={timestamp}"
    signature = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    return timestamp, f"{query}&signature={signature}"

def hacer_solicitud(endpoint, params=""):
    timestamp, query_firmada = crear_firma(params)
    headers = {"X-MBX-APIKEY": API_KEY}
    url = f"https://api.binance.com{endpoint}?{query_firmada}"
    return requests.get(url, headers=headers, timeout=10)

print("=" * 60)
print("INFORMACIÓN COMPLETA DE TU CUENTA BINANCE")
print("=" * 60)

# 1. INFORMACIÓN DE LA CUENTA
print("\n1. 📋 INFORMACIÓN DE CUENTA:")
print("-" * 40)
try:
    respuesta = hacer_solicitud("/api/v3/account")
    datos = respuesta.json()
    
    print(f"   • Permisos API: {', '.join(datos.get('permissions', []))}")
    print(f"   • Nivel de comisión: {datos.get('commissionLevel', 'N/A')}")
    print(f"   • Cuenta puede comerciar: {datos.get('canTrade', 'N/A')}")
    print(f"   • Cuenta puede retirar: {datos.get('canWithdraw', 'N/A')}")
    print(f"   • Cuenta puede depositar: {datos.get('canDeposit', 'N/A')}")
    print(f"   • Maker Commission: {datos.get('makerCommission', 'N/A')}%")
    print(f"   • Taker Commission: {datos.get('takerCommission', 'N/A')}%")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. SALDOS DE WALLET
print("\n2. 💰 SALDOS DE WALLET (SPOT):")
print("-" * 40)
try:
    saldos = [b for b in datos.get('balances', []) if float(b['free']) > 0 or float(b['locked']) > 0]
    
    if saldos:
        print(f"   Monedas con saldo ({len(saldos)}):")
        for balance in saldos[:10]:  # Mostrar primeras 10
            libre = float(balance['free'])
            bloqueado = float(balance['locked'])
            total = libre + bloqueado
            if total > 0:
                print(f"   • {balance['asset']}: Libre={libre:.8f}, Bloqueado={bloqueado:.8f}, Total={total:.8f}")
        if len(saldos) > 10:
            print(f"   ... y {len(saldos) - 10} monedas más")
    else:
        print("   Sin saldo en spot")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 3. VERIFICAR FUTUROS
print("\n3. 📈 VERIFICANDO FUTUROS:")
print("-" * 40)
try:
    # Probar si tiene acceso a futuros
    t, q = crear_firma()
    headers = {"X-MBX-APIKEY": API_KEY}
    url_futuros = f"https://fapi.binance.com/fapi/v2/account?{q}"
    respuesta_f = requests.get(url_futuros, headers=headers, timeout=10)
    
    if respuesta_f.status_code == 200:
        datos_f = respuesta_f.json()
        print("   ✅ FUTUROS HABILITADOS")
        print(f"   • Total Margin Balance: ${float(datos_f.get('totalMarginBalance', 0)):.2f}")
        print(f"   • Available Balance: ${float(datos_f.get('availableBalance', 0)):.2f}")
        print(f"   • Unrealized P&L: ${float(datos_f.get('totalUnrealizedProfit', 0)):.2f}")
        print(f"   • Posiciones abiertas: {len([p for p in datos_f.get('positions', []) if float(p['positionAmt']) != 0])}")
    elif respuesta_f.status_code == 401:
        print("   ❌ FUTUROS NO HABILITADOS (API sin permisos)")
    else:
        print(f"   ⚠️  Código: {respuesta_f.status_code} - Revisar permisos")
except Exception as e:
    print(f"   ⚠️  Error futuros: {e}")

# 4. VERIFICAR MARGIN (CROSS)
print("\n4. 📊 VERIFICANDO MARGIN:")
print("-" * 40)
try:
    # Probar margin cross
    respuesta_m = hacer_solicitud("/sapi/v1/margin/account")
    if respuesta_m.status_code == 200:
        datos_m = respuesta_m.json()
        print("   ✅ MARGIN HABILITADO")
        print(f"   • Margin Level: {float(datos_m.get('marginLevel', 0)):.2f}")
        print(f"   • Total Asset: ${float(datos_m.get('totalAssetOfBtc', 0)):.8f} BTC")
    elif respuesta_m.status_code == 401:
        print("   ❌ MARGIN NO HABILITADO")
    else:
        print(f"   ⚠️  Código: {respuesta_m.status_code}")
except Exception as e:
    print(f"   ⚠️  Error margin: {e}")

# 5. RESUMEN FINAL
print("\n5. 📝 RESUMEN:")
print("-" * 40)

# Calcular saldo total aproximado en BTC
try:
    saldo_total_btc = 0
    for balance in datos.get('balances', []):
        libre = float(balance['free'])
        bloqueado = float(balance['locked'])
        if libre + bloqueado > 0:
            # Para simplificar, asumimos 1 BTC = 1 BTC (obvio)
            # En realidad deberías obtener precios reales
            if balance['asset'] == 'BTC':
                saldo_total_btc += (libre + bloqueado)
            elif balance['asset'] == 'USDT':
                saldo_total_btc += (libre + bloqueado) / 45000  # Aproximado
            elif balance['asset'] == 'ETH':
                saldo_total_btc += (libre + bloqueado) / 15  # Aproximado
    
    print(f"   • Saldo aproximado en BTC: {saldo_total_btc:.8f}")
    print(f"   • Saldo aproximado en USD: ${saldo_total_btc * 45000:.2f}")
    
    # Verificar permisos
    permisos = datos.get('permissions', [])
    print(f"   • Spot Trading: {'✅' if 'SPOT' in permisos else '❌'}")
    print(f"   • Margin Trading: {'✅' if 'MARGIN' in permisos else '❌'}")
    print(f"   • Futures Trading: {'✅' if 'LEVERAGED' in permisos or 'FUTURES' in permisos else '❌'}")
    
except Exception as e:
    print(f"   ❌ Error cálculo: {e}")

print("\n" + "=" * 60)
print("✨ Análisis completado")
print("=" * 60)
