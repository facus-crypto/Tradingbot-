"""
Script para ayudar a configurar API Keys de Binance
"""
import sys
import os

def mostrar_instrucciones():
    print("🔧 CONFIGURACIÓN DE API KEYS PARA BINANCE FUTURES")
    print("=" * 60)
    
    print("\n🎯 PASO 1: Crear cuenta en Binance Testnet (RECOMENDADO)")
    print("   1. Ve a: https://testnet.binancefuture.com")
    print("   2. Haz clic en 'Register' o 'Login with Binance'")
    print("   3. Crea una cuenta de prueba")
    
    print("\n🎯 PASO 2: Generar API Keys en Testnet")
    print("   1. Una vez logueado, ve a 'API Management'")
    print("   2. Crea un nuevo API Key")
    print("   3. Marca las opciones:")
    print("      - ✅ Enable Reading")
    print("      - ✅ Enable Spot & Margin Trading")
    print("      - ✅ Enable Futures")
    print("   4. Guarda la API Key y Secret (¡cópialas ahora!)")
    
    print("\n🎯 PASO 3: Configurar en tu archivo config.py")
    print("   1. Abre config.py con:")
    print("      nano config.py")
    print("   2. Busca la sección BINANCE_CONFIG")
    print("   3. Reemplaza:")
    print("      'TU_API_KEY' → tu API Key real")
    print("      'TU_API_SECRET' → tu API Secret real")
    print("   4. Asegúrate que testnet sea True:")
    print("      'testnet': True")
    
    print("\n🎯 PASO 4: Whitelist de IP (OPCIONAL pero recomendado)")
    print("   1. En API Management, habilita 'Restrict access to trusted IPs only'")
    print("   2. Añade tu IP pública (puedes verla en: https://whatismyipaddress.com/)")
    
    print("\n⚠️  IMPORTANTE: PARA TESTNET SOLAMENTE")
    print("   • Usa solo fondos de prueba (no reales)")
    print("   • Los precios y mercados son simulados")
    print("   • Ideal para desarrollo y pruebas")
    
    print("\n🔗 Enlaces útiles:")
    print("   • Testnet: https://testnet.binancefuture.com")
    print("   • Documentación API: https://binance-docs.github.io/apidocs/futures/en/")
    print("   • GitHub: https://github.com/binance/binance-futures-connector-python")
    
    print("\n" + "=" * 60)
    
    respuesta = input("\n¿Ya tienes tus API Keys configuradas en config.py? (s/n): ")
    
    if respuesta.lower() == 's':
        print("\n✅ Perfecto! Ahora podemos probar la integración.")
        print("   Ejecuta: python3 prueba_binance_futures.py")
    else:
        print("\n⚠️  Configura tus API Keys primero.")
        print("   Sigue los pasos arriba y luego ejecuta:")
        print("   python3 prueba_binance_futures.py")

if __name__ == "__main__":
    mostrar_instrucciones()
