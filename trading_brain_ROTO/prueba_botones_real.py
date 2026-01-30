import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.getcwd())

async def main():
    print("🔍 Importando módulos...")
    
    try:
        # Importar desde la ubicación correcta
        from interfaces.telegram_advanced import TelegramAdvancedBot
        print("✅ Módulo Telegram cargado")
        
        # Configuración REAL
        BOT_TOKEN = "8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw"
        CHAT_ID = "213736357"  # Tu chat_id
        
        print(f"🔗 Conectando a Telegram (Chat: {CHAT_ID})...")
        
        # Crear bot
        bot = TelegramAdvancedBot(
            bot_token=BOT_TOKEN,
            chat_id=CHAT_ID
        )
        
        # Iniciar
        await bot.start()
        print("✅ Bot iniciado")
        
        # Datos de señal de PRUEBA
        señal_prueba = {
            'symbol': 'BTCUSDT',
            'side': 'COMPRAR',
            'entry_price': 95500.00,
            'stop_loss': 95000.00,
            'take_profit': 97000.00,
            'quantity': 0.002,
            'leverage': 2,
            'reason': '🔧 PRUEBA DEL SISTEMA - No ejecutar',
            'timestamp': '23:45:00',
            'risk_percentage': 1.5,
            'mode': 'SIMULACIÓN'
        }
        
        print("📤 Enviando señal de prueba CON BOTONES...")
        
        # Enviar señal
        msg_id = await bot.send_signal(señal_prueba)
        
        if msg_id:
            print(f"✅ Señal enviada (ID: {msg_id})")
            print("\n📱 EN TU TELEGRAM DEBERÍAS VER:")
            print("• Señal de BTC con precios")
            print("• Botón ✅ CONFIRMAR (verde)")
            print("• Botón ❌ CANCELAR (rojo)")
            print("\n🎯 PRUEBA: Toca ✅ CONFIRMAR")
            print("💡 Deberías recibir: 'SIMULACIÓN: Orden ejecutada'")
            
            # Esperar 3 minutos para que pruebes
            print("\n⏰ Bot activo por 3 minutos...")
            await asyncio.sleep(180)
            
        else:
            print("❌ Error enviando señal")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 PRUEBA BOTONES TELEGRAM")
    print("═" * 50)
    asyncio.run(main())
    print("═" * 50)
    print("✅ Prueba terminada")
