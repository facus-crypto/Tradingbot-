"""
Probar si las keys son de Binance Principal (producción)
"""
import hmac
import hashlib
import time
import requests

API_KEY = "uDLz2UjKBfY6Nhj9Q9paxpFMUmCQkmw71knczVmuelu9v80RwAvwCosOwwScHepL"
API_SECRET = "cx7n5YHG8jDKY10tS1ejsj2wShnNdT3qvsaFClZPpbVIDQZFouxkB1llfzsY34y4"

# Probar CON y SIN testnet
endpoints = [
    ("TESTNET Futures", "https://testnet.binancefuture.com/fapi/v2/balance"),
    ("TESTNET Spot", "https://testnet.binance.vision/api/v3/account"),
    ("PRODUCCIÓN Futures", "https://fapi.binance.com/fapi/v2/balance"),
    ("PRODUCCIÓN Spot", "https://api.binance.com/api/v3/account")
]

def test_all_endpoints():
    print("🔍 Probando TODOS los endpoints posibles...")
    
    headers = {'X-MBX-APIKEY': API_KEY}
    
    for name, endpoint in endpoints:
        print(f"\n📡 Probando: {name}")
        print(f"   URL: {endpoint}")
        
        timestamp = int(time.time() * 1000)
        params = {'timestamp': timestamp, 'recvWindow': 10000}
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            API_SECRET.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        params['signature'] = signature
        
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:100]}")
            
            if response.status_code == 200:
                print(f"   ✅ ¡FUNCIONA CON {name}!")
                if 'availableBalance' in response.text:
                    import json
                    data = json.loads(response.text)
                    if isinstance(data, list):
                        for item in data:
                            if item.get('asset') == 'USDT':
                                print(f"   💰 Balance USDT: {item.get('availableBalance')}")
                return name  # Devolver el endpoint que funciona
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
    
    print("\n❌ Ningún endpoint funcionó.")
    return None

if __name__ == "__main__":
    working_endpoint = test_all_endpoints()
    
    if working_endpoint:
        print(f"\n🎯 CONCLUSIÓN: Las keys funcionan con {working_endpoint}")
        if "TESTNET" in working_endpoint:
            print("   ✅ Configura testnet=True en config.py")
        else:
            print("   ⚠️  Son keys de PRODUCCIÓN - ¡CUIDADO!")
            print("   ⚠️  Configura testnet=False en config.py")
    else:
        print("\n❌ Las API Keys NO funcionan en ningún endpoint.")
        print("   Posibles causas:")
        print("   1. API Keys revocadas/eliminadas")
        print("   2. Permisos incorrectos")
        print("   3. IP bloqueada (poco probable si no hay whitelist)")
        print("   4. Keys creadas en cuenta equivocada")
