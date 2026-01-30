"""
Probar con Binance Spot Testnet (alternativa)
"""
import hmac
import hashlib
import time
import requests

API_KEY = "uDLz2UjKBfY6Nhj9Q9paxpFMUmCQkmw71knczVmuelu9v80RwAvwCosOwwScHepL"
API_SECRET = "cx7n5YHG8jDKY10tS1ejsj2wShnNdT3qvsaFClZPpbVIDQZFouxkB1llfzsY34y4"

BASE_URL = "https://testnet.binance.vision"  # Spot Testnet diferente

def test_spot_api():
    print("🔍 Probando Binance Spot Testnet...")
    
    headers = {'X-MBX-APIKEY': API_KEY}
    timestamp = int(time.time() * 1000)
    
    # Probar endpoint de spot
    params = {
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    
    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        query_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    params['signature'] = signature
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v3/account",
            headers=headers,
            params=params
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ ¡Binance Spot Testnet funciona!")
        else:
            print(f"❌ Error {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_spot_api()
