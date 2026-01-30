"""
Prueba básica de Telegram Bot
"""
import sys
import os
sys.path.append('.')

import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_telegram_bot():
    """Prueba la conexión con Telegram"""
    
    print("🤖 PROBANDO TELEGRAM BOT")
    print("=" * 50)
    
    try:
        # Importar configuración
        from telegram_config import get_bot_token, get_chat_id
        
        bot_token = get_bot_token()
        chat_id = get_chat_id()
        
        print(f"✅ Token obtenido: {'*' * 20}{bot_token[-4:]}")
        print(f"✅ Chat ID: {chat_id}")
        
        # Verificar si está instalado python-telegram-bot
        try:
            import telegram
            from telegram import Bot
            
            print("✅ python-telegram-bot instalado")
            
            # Probar conexión simple
            print("\n🔗 Probando conexión con Telegram API...")
            bot = Bot(token=bot_token)
            
            try:
                # Obtener info del bot
                bot_info = await bot.get_me()
                print(f"✅ Bot conectado: @{bot_info.username}")
                print(f"   Nombre: {bot_info.first_name}")
                
                # Probar envío de mensaje simple
                print("\n📤 Probando envío de mensaje...")
                message = await bot.send_message(
                    chat_id=chat_id,
                    text="🤖 *Bot de Trading conectado correctamente!*\n\n"
                         "Sistema: 5 cerebros + Binance Futures\n"
                         "Prueba de conexión exitosa.",
                    parse_mode='Markdown'
                )
                
                print(f"✅ Mensaje enviado (ID: {message.message_id})")
                
                # Probar botones inline
                print("\n🔄 Probando botones inline...")
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                
                keyboard = [
                    [
                        InlineKeyboardButton("✅ CONFIRMAR", callback_data="test_confirm"),
                        InlineKeyboardButton("❌ CANCELAR", callback_data="test_cancel")
                    ],
                    [
                        InlineKeyboardButton("🔴 CERRAR POSICIÓN", callback_data="test_close"),
                        InlineKeyboardButton("📊 STATUS", callback_data="test_status")
                    ]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                button_message = await bot.send_message(
                    chat_id=chat_id,
                    text="🔔 *PRUEBA DE BOTONES*\n\n"
                         "Estos son los botones que se usarán:\n"
                         "• ✅ Confirmar señales\n"
                         "• ❌ Cancelar\n"
                         "• 🔴 Cerrar posición (NUEVO)\n"
                         "• 📊 Ver status",
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
                
                print(f"✅ Mensaje con botones enviado (ID: {button_message.message_id})")
                
                print("\n" + "=" * 50)
                print("🎯 TELEGRAM BOT CONFIGURADO CORRECTAMENTE")
                print("\n📋 Funcionalidades implementadas:")
                print("   ✅ Botones interactivos")
                print("   ✅ Confirmar/Cancelar señales")
                print("   ✅ 🔴 Cerrar posición (NUEVO)")
                print("   ✅ Comandos: /start, /status, /posiciones")
                print("   ✅ Integración con Binance Futures")
                
                return True
                
            except telegram.error.Unauthorized as e:
                print(f"❌ Error de autorización: {e}")
                print("   Verifica que el Bot Token sea correcto")
                return False
            except telegram.error.BadRequest as e:
                print(f"❌ Error en la petición: {e}")
                print("   Verifica que el Chat ID sea correcto")
                return False
            except Exception as e:
                print(f"❌ Error enviando mensaje: {e}")
                return False
                
        except ImportError:
            print("❌ python-telegram-bot no instalado")
            print("   Ejecuta: pip install python-telegram-bot")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando configuración: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    # Ejecutar prueba asíncrona
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    success = loop.run_until_complete(test_telegram_bot())
    
    if success:
        print("\n✅ ¡Telegram Bot listo para integrar con el sistema!")
    else:
        print("\n❌ La prueba falló. Corrige los errores.")
    
    loop.close()
