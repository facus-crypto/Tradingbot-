import requests
import time
import hashlib
import hmac

API_KEY = "1JuwHBEThWq06lIHFnnDoHuFS6NDw45a7SMHk64X7uTlrBpkjMAPk5hiur8vLuPD"
SECRET_KEY = "1RUhGgywkDn4loz2BO59AGr76mEe8BrtUGQ5YI7AfaxYyMjH80r27GG1a56tmfdr"

print("=== PRUEBA CONEXIÓN BINANCE ===")
print(f"API: {API_KEY[:15]}...")
print(f"SECRET: {SECRET_KEY[:15]}...")

# 1. Probar conexión básica
print("\n[1/3] Probando conexión...")
try:
    r = requests.get("https://api.binance.com/api/v3/ping", timeout=5)
    print(f"✓ Binance responde (Status: {r.status_code})")
except Exception as e:
    print(f"✗ Error conexión: {e}")
    exit()

# 2. Crear firma
print("\n[2/3] Generando firma...")
timestamp = int(time.time() * 1000)
query = f"timestamp={timestamp}"
signature = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()

headers = {"X-MBX-APIKEY": API_KEY}
url = f"https://api.binance.com/api/v3/account?{query}&signature={signature}"

# 3. Probar autenticación
print("\n[3/3] Probando autenticación...")
try:
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"\nRESULTADO:")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ ✅ ✅ ¡CONEXIÓN EXITOSA!")
        print("Tus llaves de Binance son VÁLIDAS")
    elif response.status_code == 401:
        print("❌ ERROR 401: API Key inválida o expirada")
        print("Ve a Binance > API Management y verifica:")
        print("1. Que la API Key esté activa")
        print("2. Que no haya expirado")
        print("3. URL: https://www.binance.com/es/my/settings/api-management")
    elif response.status_code == 403:
        print("❌ ERROR 403: IP no autorizada")
        print("Tu IP actual no está en la whitelist de Binance")
        print("Agrega tu IP en Binance API Management")
    else:
        print(f"⚠️  Código: {response.status_code}")
        print(f"Respuesta: {response.text[:100]}")
        
except Exception as e:
    print(f"❌ Error en solicitud: {e}")

print("\n" + "="*40)
