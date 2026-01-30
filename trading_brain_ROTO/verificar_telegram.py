#!/usr/bin/env python3
"""
Verificar estado de Telegram
"""
import os
import json

print("🔍 VERIFICANDO ESTADO DE TELEGRAM")
print("=" * 50)

# 1. Verificar archivo de configuración
config_file = "config_futures.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    token = config['telegram']['token']
    chat_id = config['telegram']['chat_id']
    
    print("📋 CONFIGURACIÓN EN config_futures.json:")
    print(f"• Token: {'✅ CONFIGURADO' if token and token != 'TU_BOT_TOKEN_AQUI' else '❌ NO CONFIGURADO'}")
    print(f"• Chat ID: {'✅ CONFIGURADO' if chat_id and chat_id != 'TU_CHAT_ID_AQUI' else '❌ NO CONFIGURADO'}")
    
    if token and token != 'TU_BOT_TOKEN_AQUI':
        print(f"   Token: {token[:15]}...")
    if chat_id and chat_id != 'TU_CHAT_ID_AQUI':
        print(f"   Chat ID: {chat_id}")
else:
    print(f"❌ {config_file} no encontrado")

# 2. Verificar archivo telegram_advanced.py
telegram_file = "telegram_advanced.py"
print(f"\n📄 ARCHIVO {telegram_file}:")
if os.path.exists(telegram_file):
    print(f"✅ EXISTE ({os.path.getsize(telegram_file)} bytes)")
    
    # Verificar contenido básico
    with open(telegram_file, 'r') as f:
        contenido = f.read()
    
    if "class TelegramAdvancedBot" in contenido:
        print("✅ Contiene clase TelegramAdvancedBot")
    else:
        print("❌ NO contiene la clase correcta")
    
    if "async def send_signal" in contenido:
        print("✅ Tiene método send_signal")
    else:
        print("❌ Falta método send_signal")
        
else:
    print("❌ NO EXISTE - Necesita crearse")

# 3. Verificar import en sistema_principal_futures.py
sistema_file = "core/sistema_principal_futures.py"
print(f"\n🔗 IMPORT EN {sistema_file}:")
if os.path.exists(sistema_file):
    with open(sistema_file, 'r') as f:
        contenido = f.read()
    
    if "from telegram_advanced import TelegramAdvancedBot" in contenido:
        print("✅ Importa TelegramAdvancedBot")
    elif "import telegram_advanced" in contenido:
        print("✅ Importa módulo telegram_advanced")
    else:
        print("❌ NO importa telegram_advanced")
        
    # Verificar si usa la clase
    if "TelegramAdvancedBot" in contenido:
        print("✅ Usa clase TelegramAdvancedBot")
    else:
        print("❌ NO usa TelegramAdvancedBot")
else:
    print(f"❌ {sistema_file} no encontrado")

# 4. Probar importación directa
print("\n🧪 PROBANDO IMPORTACIÓN:")
try:
    from telegram_advanced import TelegramAdvancedBot
    print("✅ Importación EXITOSA de TelegramAdvancedBot")
    
    # Probar crear instancia (sin iniciar)
    if token and token != 'TU_BOT_TOKEN_AQUI' and chat_id and chat_id != 'TU_CHAT_ID_AQUI':
        try:
            bot = TelegramAdvancedBot(token, chat_id)
            print("✅ Instancia creada correctamente")
            
            # Verificar métodos
            if hasattr(bot, 'enviar_mensaje'):
                print("✅ Tiene método enviar_mensaje")
            if hasattr(bot, 'send_signal'):
                print("✅ Tiene método send_signal")
            if hasattr(bot, 'iniciar'):
                print("✅ Tiene método iniciar")
                
        except Exception as e:
            print(f"❌ Error creando instancia: {e}")
    else:
        print("⚠️  No se puede probar instancia (falta token/chat_id)")
        
except ImportError as e:
    print(f"❌ Error importando: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")

print("\n" + "=" * 50)
print("🎯 DIAGNÓSTICO:")
print("Si 'telegram_advanced.py' NO existe o tiene error:")
print("1. Crea el archivo con la clase correcta")
print("2. O usa un módulo más simple")
print("3. O desactiva Telegram temporalmente")

print("\n🛠️  SOLUCIÓN RÁPIDA:")
print("Ejecutar: python configurar_telegram.py")
print("(creará telegram_advanced.py si no existe)")
