import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    print("🔄 Iniciando sistema LIMPIO...")
    
    # Importar componentes directamente
    from interfaces.telegram_advanced import TelegramAdvancedBot
    from binance_manager_custom import get_binance_manager
    from cerebros.cerebro_btc_futures import CerebroBTC
    from cerebros.cerebro_eth_futures import CerebroETH
    from cerebros.cerebro_sol_futures import CerebroSOL
    from cerebros.cerebro_link_futures import CerebroLINK
    
    # 1. Iniciar Telegram SOLO
    print("📱 Iniciando Telegram...")
    telegram_bot = TelegramAdvancedBot(
        bot_token='8336783544:AAFsyl628ALE9RKTInE60HnOjLHMe6mlbtw',
        chat_id='213736357'
    )
    await telegram_bot.start()
    print("✅ Telegram listo - Responde a /status")
    
    # 2. Iniciar Binance
    print("💰 Iniciando Binance...")
    binance_manager = get_binance_manager()
    balance = await binance_manager.get_balance()
    print(f"✅ Binance listo - Balance: {balance} USDT")
    
    # 3. Iniciar 4 cerebros (sin BNB por ahora)
    print("🧠 Iniciando cerebros...")
    cerebros = {
        'BTC': CerebroBTC(binance_manager=binance_manager, telegram_bot=telegram_bot),
        'ETH': CerebroETH(binance_manager=binance_manager, telegram_bot=telegram_bot),
        'SOL': CerebroSOL(binance_manager=binance_manager, telegram_bot=telegram_bot),
        'LINK': CerebroLINK(binance_manager=binance_manager, telegram_bot=telegram_bot)
    }
    
    print("✅ 4 cerebros listos (BTC, ETH, SOL, LINK)")
    print("\n🎯 SISTEMA LISTO PARA OPERAR")
    print("📱 Escribe /status en Telegram")
    
    # Mantener activo
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
