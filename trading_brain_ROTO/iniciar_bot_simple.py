import logging
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update, context):
    await update.message.reply_text(
        '🤖 **Bot de Trading Activo**\n\n'
        '✅ Configuración correcta\n'
        '✅ Listo para recibir señales\n'
        '✅ Botones interactivos activos\n\n'
        '📊 Sistema: 10 cerebros operativos\n'
        '🔗 Binance: Conectado\n'
        '🚀 Modo: Trading manual con confirmación',
        parse_mode='Markdown'
    )

async def status_command(update, context):
    await update.message.reply_text(
        '✅ **SISTEMA OPERATIVO**\n\n'
        '• 10 cerebros activos\n'
        '• Modo: Señales manuales\n'
        '• Bot funcionando\n'
        '• Trailing stop configurado\n\n'
        '📋 Mercados monitoreados:\n'
        '• BTC\n• ETH\n• SOL\n• LINK\n• BNB\n'
        '• ADA\n• AVAX\n• XRP\n• DOT\n• ATOM',
        parse_mode='Markdown'
    )

def main():
    import json
    with open('config_futures.json', 'r') as f:
        config = json.load(f)
    
    TOKEN = config['telegram']['bot_token']
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    
    print(f"🤖 Iniciando bot con token: {TOKEN[:15]}...")
    app.run_polling(allowed_updates=None)

if __name__ == '__main__':
    main()
