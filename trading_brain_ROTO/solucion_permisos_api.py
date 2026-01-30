#!/usr/bin/env python3
"""
Solución para permisos de API Keys
"""
import os
import json

print("🔧 SOLUCIÓN PARA PERMISOS DE API KEYS")
print("=" * 50)

print("📋 DIAGNÓSTICO CONFIRMADO:")
print("✅ Las API Keys SON VÁLIDAS (futures_exchange_info() funciona)")
print("❌ Pero NO tienen permisos de TRADING (futures_account() falla)")
print("❌ Tampoco tienen permisos de SPOT TRADING (get_account() falla)")

print("\n🎯 EL PROBLEMA:")
print("Falta el permiso: 'Enable Trading' (Habilitar Trading)")
print("En Binance, necesitas ACTIVAR:")
print("1. ✅ Habilitar lectura (ya está)")
print("2. ✅ Habilitar spot y trading de margen (ya está)")
print("3. ✅ Habilitar Contratos (ya está)")
print("4. ❌ **PERO FALTA: 'Enable Trading' dentro de cada categoría**")

print("\n💡 SOLUCIÓN PASO A PASO:")

print("\n1️⃣ IR A BINANCE:")
print("   • https://www.binance.com/ (o testnet.binancefuture.com para testnet)")
print("   • API Management")

print("\n2️⃣ EDITAR API KEY EXISTENTE:")
print("   • Busca tu API Key: uDLz2UjKBfY6Nhj9Q9paxpFMUmCQkmw71knczVm...")
print("   • Haz clic en 'Edit restrictions'")

print("\n3️⃣ VERIFICAR PERMISOS EXACTOS:")
print("   Debe tener TODOS estos:")
print("   [✅] Habilitar lectura")
print("   [✅] Habilitar spot y trading de margen")
print("   [✅] **DENTRO de esto: 'Enable Spot & Margin Trading'**")
print("   [✅] Habilitar Contratos")
print("   [✅] **DENTRO de esto: 'Enable Futures' Y 'Enable Futures Trading'**")

print("\n4️⃣ SI NO SE PUEDE EDITAR:")
print("   • Crea NUEVAS API Keys")
print("   • Nombre: 'trading_bot_full_access'")
print("   • Activa TODOS los permisos de trading")
print("   • Sin restricción IP (o añade tu IP)")
print("   • Guarda nuevas claves")

print("\n5️⃣ ACTUALIZAR CONFIGURACIÓN:")
print("   • Si editaste: no necesitas cambiar nada")
print("   • Si creaste nuevas: actualiza config_futures.json")

print("\n" + "=" * 50)
print("❓ PREGUNTA CRÍTICA:")
print("¿Puedes entrar AHORA a Binance y verificar/editar los permisos?")
print("¿O prefieres crear nuevas API Keys directamente?")

print("\n📋 PRÓXIMO PASO SEGÚN TU RESPUESTA:")
print("Opción A: Verificar/editar API Keys existentes")
print("Opción B: Crear nuevas API Keys")

# Preguntar al usuario
respuesta = input("\n¿Qué prefieres? (A/B): ").strip().upper()

if respuesta == 'A':
    print("\n🎯 INSTRUCCIONES DETALLADAS PARA OPCIÓN A:")
    print("1. Ve a: https://testnet.binancefuture.com/")
    print("2. API Management → Busca tu API Key")
    print("3. 'Edit restrictions'")
    print("4. Asegúrate de que TENGA:")
    print("   • Enable Spot & Margin Trading")
    print("   • Enable Futures")
    print("   • Enable Futures Trading")
    print("5. Guarda cambios")
    print("6. Regresa y ejecuta: python verificar_conexion_binance.py")
    
elif respuesta == 'B':
    print("\n🎯 INSTRUCCIONES DETALLADAS PARA OPCIÓN B:")
    print("1. Ve a: https://testnet.binancefuture.com/")
    print("2. API Management → Create API")
    print("3. Nombre: 'trading_bot_full'")
    print("4. PERMISOS (MARCAR TODOS):")
    print("   ✅ Enable Reading")
    print("   ✅ Enable Spot & Margin Trading")
    print("   ✅ Enable Futures")
    print("   ✅ Enable Futures Trading")
    print("5. IP Restriction: None (o tu IP)")
    print("6. Crea y GUARDA AMBAS CLAVES")
    
    nueva_api = input("\nNueva API Key: ").strip()
    nueva_secret = input("Nueva Secret Key: ").strip()
    
    if nueva_api and nueva_secret:
        # Actualizar configuración
        config_file = "config_futures.json"
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        config['binance']['api_key'] = nueva_api
        config['binance']['api_secret'] = nueva_secret
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n✅ Config_futures.json actualizado")
        print(f"• Nueva API Key: {nueva_api[:20]}...")
        print("\n🎯 Prueba ahora: python verificar_conexion_binance.py")
    else:
        print("\n⚠️  No se proporcionaron nuevas claves")
        
else:
    print("\n⚠️  Respuesta no válida. Continuaremos después de que verifiques.")

print("\n" + "=" * 50)
print("📌 RESUMEN:")
print("• Las keys existen pero falta permiso de TRADING")
print("• Necesitas 'Enable Trading' específicamente")
print("• Sin eso, el bot no podrá ejecutar órdenes")
