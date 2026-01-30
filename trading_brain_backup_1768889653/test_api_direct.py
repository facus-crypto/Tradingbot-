"""
Prueba directa de API Keys con requests
"""
import hmac
import hashlib
import time
import requests
import json

# Tus API Keys (ya configuradas)
API_KEY = "FqiAcido53B0N0MVfirLnvKrufoCwqzDyPs5M8IvqEuMbBOwsy2L9vS6tfxSTI1o"
API_SECRET = "zA0CCDqgQXsQDpduqPn04CSasuiNmO3Si9gsFYYMnAcyOhbwZeGgNQtEmcxnel1U"

BASE_URL = "https://testnet.binancefuture.com"

def test_api_key():
    print("🔍 Probando API Key directamente...")
    
    # 1. Probar endpoint que NO requiere firma (solo API Key)
    print("\n1. Probando endpoint sin firma (solo API Key)...")
    headers = {'X-MBX-APIKEY': API_KEY}
    
    try:
        response = requests.get(f"{BASE_URL}/fapi/v1/ping", headers=headers)
        print(f"   ✅ Ping con API Key: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Probar endpoint que SÍ requiere firma
    print("\n2. Probando endpoint con firma (balance)...")
    
    # Crear parámetros
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    
    # Crear query string y firma
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    params['signature'] = signature
    
    # Hacer la petición
    try:
        response = requests.get(
            f"{BASE_URL}/fapi/v2/balance",
            headers=headers,
            params=params
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("   ✅ ¡API Keys funcionan correctamente!")
            data = response.json()
            for balance in data:
                if balance['asset'] == 'USDT':
                    print(f"   💰 Balance USDT: {balance['availableBalance']}")
        else:
            print(f"   ❌ Error {response.status_code}")
            
            # Intentar diagnóstico
            if "Invalid API-key" in response.text:
                print("   ⚠️  API Key inválida o revocada")
            elif "Signature" in response.text:
                print("   ⚠️  Error en la firma (API Secret incorrecta)")
            elif "timestamp" in response.text.lower():
                print("   ⚠️  Problema de timestamp (verifica la hora del sistema)")
            elif "IP" in response.text:
                print("   ⚠️  IP no whitelisted")
    
    except Exception as e:
        print(f"   ❌ Error en la petición: {e}")

if __name__ == "__main__":
    test_api_key()
