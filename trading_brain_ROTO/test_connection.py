import requests

API_KEY = "1JuwHBEThWq06lIHFnnDoHuFS6NDw45a7SMHk64X7uTlrBpkjMAPk5hiur8vLuPD"
SECRET_KEY = "1RUhGgywkDn4loz2BO59AGr76mEe8BrtUGQ5YI7AfaxYyMjH80r27GG1a56tmfdr"

print("Probando conexión con Bunace API...")
print(f"API Key: {API_KEY[:20]}...")
print(f"Secret Key: {SECRET_KEY[:20]}...")
print("-" * 50)

url = "https://api.bunace.com/api/v1/account"
headers = {
    "X-Bunace-API-Key": API_KEY,
    "X-Bunace-Signature": SECRET_KEY
}

try:
    print("Enviando solicitud a Bunace...")
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"✅ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ CONEXIÓN EXITOSA - Las keys son válidas")
    elif response.status_code == 401:
        print("❌ ERROR 401 - Las keys NO son válidas o están mal configuradas")
    elif response.status_code == 403:
        print("❌ ERROR 403 - Acceso prohibido con estas credenciales")
    else:
        print(f"⚠️  Código de estado inesperado: {response.status_code}")
    
    print(f"Respuesta completa: {response.text[:200]}...")
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se puede conectar al servidor de Bunace")
except requests.exceptions.Timeout:
    print("❌ ERROR: Tiempo de espera agotado")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
