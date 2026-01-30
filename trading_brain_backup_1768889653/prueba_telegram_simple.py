import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    print("🤖 INICIANDO SOLO TELEGRAM PARA PRUEBA")
    
    from interfaces.telegram_advanced import TelegramAdvancedBot
    
    # Iniciar solo Telegram
    bot = TelegramAdvancedBot(
        bot_token='8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw',
        chat_id='213736357'
    )
    
    print("📱 Iniciando Telegram...")
    await bot.start()
    
    print("✅ Telegram activo")
    print("📝 Envía /start o /status en Telegram")
    print("⏳ Manteniendo activo por 5 minutos...")
    
    # Mantener activo
    await asyncio.sleep(300)
    
    print("🏁 Prueba terminada")

if __name__ == "__main__":
    asyncio.run(main())
