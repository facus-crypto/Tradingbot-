import asyncio
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)

def ejecutar_telegram_en_hilo():
    """Ejecuta Telegram en su propio event loop"""
    asyncio.run(iniciar_telegram_solo())

async def iniciar_telegram_solo():
    """Inicia solo Telegram en su propio loop"""
    from interfaces.telegram_advanced import TelegramAdvancedBot
    
    bot = TelegramAdvancedBot(
        bot_token='8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw',
        chat_id='213736357'
    )
    
    await bot.start()
    
    # Mantener activo para siempre
    while True:
        await asyncio.sleep(1)

async def main():
    print("🤖 SISTEMA CON TELEGRAM EN HILO SEPARADO")
    
    # Iniciar Telegram en hilo separado
    print("📱 Iniciando Telegram en hilo separado...")
    telegram_thread = threading.Thread(target=ejecutar_telegram_en_hilo, daemon=True)
    telegram_thread.start()
    
    print("⏳ Esperando 15 segundos para que Telegram se estabilice...")
    await asyncio.sleep(15)
    
    # Iniciar sistema principal SIN Telegram
    from core.sistema_principal_futures import SistemaPrincipalFutures
    
    sistema = SistemaPrincipalFutures()
    
    # Inicializar componentes excepto Telegram
    await sistema.inicializar_binance()
    print("✅ Binance listo")
    
    # Inicializar cerebros
    await sistema.inicializar_cerebros()
    print("✅ 5 cerebros listos")
    
    # Iniciar ciclo
    print("🔄 Iniciando ciclo de análisis...")
    await sistema.iniciar_ciclo_continuo()
    
    # Mantener activo
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
