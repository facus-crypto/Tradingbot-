import requests
import json
import time

with open('config_futures.json', 'r') as f:
    config = json.load(f)

TOKEN = config['telegram']['bot_token']
CHAT_ID = config['telegram']['chat_id']

signal_id = f'BOTON_{int(time.time())}'

response = requests.post(
    f'https://api.telegram.org/bot{TOKEN}/sendMessage',
    json={
        'chat_id': CHAT_ID,
        'text': '🎯 **PRUEBA DE BOTONES INTERACTIVOS**\n\nEste mensaje tiene botones REALES que puedes hacer clic.\n\n📊 Par: BTCUSDT\n📈 Dirección: LONG\n💰 Precio: $68,500.00\n\n🔄 **Botones funcionales:**',
        'parse_mode': 'Markdown',
        'reply_markup': {
            'inline_keyboard': [[
                {'text': '✅ EJECUTAR ORDEN', 'callback_data': f'execute_{signal_id}'},
                {'text': '❌ CANCELAR', 'callback_data': f'cancel_{signal_id}'}
            ]]
        }
    }
).json()

if response.get('ok'):
    print(f'✅ Botones inline enviados. Message ID: {response["result"]["message_id"]}')
    print('📱 Ahora en Telegram deberías ver botones REALES que puedes hacer clic.')
else:
    print(f'❌ Error: {response}')
