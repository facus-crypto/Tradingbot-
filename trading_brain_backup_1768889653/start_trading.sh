#!/bin/bash
echo "🚀 INICIANDO SISTEMA DE TRADING COMPLETO"
echo "========================================"

# Matar procesos previos
pkill -f "python.*iniciar" 2>/dev/null
sleep 2

# Iniciar sistema
cd /data/data/com.termux/files/home/bot_trading/trading_brain
echo "📊 1. Verificando configuración..."
python3 -c "
import json
try:
    with open('config_futures.json') as f:
        config = json.load(f)
    print('✅ Configuración OK')
    print(f'   • API Key: {config[\"binance\"][\"api_key\"][:15]}...')
    print(f'   • Telegram: {config[\"telegram\"][\"token\"][:15]}...')
except Exception as e:
    print(f'❌ Error config: {e}')
"

echo -e "\n🤖 2. Iniciando Telegram..."
python3 -c "
import sys
sys.path.insert(0, '.')
import asyncio

async def iniciar_telegram():
    try:
        from interfaces.telegram_advanced import TelegramAdvancedBot
        import json
        
        with open('config_futures.json') as f:
            config = json.load(f)
        
        bot = TelegramAdvancedBot(
            bot_token=config['telegram']['token'],
            chat_id=config['telegram']['chat_id'],
            trading_executor=None
        )
        
        await bot.start()
        print('✅ Telegram INICIADO y escuchando')
        print('📱 Envía /status en Telegram para verificar')
        
        # Mantener activo
        await asyncio.sleep(10)
        
        # No llamar a stop() - dejar corriendo
        return True
        
    except Exception as e:
        print(f'❌ Error Telegram: {e}')
        return False

asyncio.run(iniciar_telegram())
"

echo -e "\n🧠 3. Iniciando sistema completo..."
echo "   El sistema ahora está analizando mercado"
echo "   Cuando detecte señales, te llegarán a Telegram"
echo "   Presiona Ctrl+C para detener"

# Iniciar sistema principal
python3 iniciar_sistema_futures.py
