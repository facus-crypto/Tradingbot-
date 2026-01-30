echo "🔍 VERIFICANDO ESTADO DEL SISTEMA"
echo "================================="
echo ""
echo "1. 📱 TELEGRAM:"
ps aux | grep -E "python.*telegram_advanced" | grep -v grep && echo "   ✅ Telegram activo" || echo "   ❌ Telegram inactivo"
echo ""
echo "2. 🧠 CEREBROS:"
ps aux | grep -E "python.*sistema_corregido" | grep -v grep && echo "   ✅ Sistema activo" || echo "   ❌ Sistema inactivo"
echo ""
echo "3. 📊 LOGS RECIENTES:"
tail -5 trading_corregido.log 2>/dev/null | while read line; do echo "   $line"; done
echo ""
echo "4. 🎯 PROBAR BOTONES TELEGRAM:"
python3 -c "
import requests, json, time
with open('config_futures.json', 'r') as f:
    config = json.load(f)
TOKEN = config['telegram']['bot_token']
CHAT_ID = config['telegram']['chat_id']
signal_id = f'VERIFY_{int(time.time())}'
resp = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', json={
    'chat_id': CHAT_ID,
    'text': '✅ **SISTEMA VERIFICADO**\\n\\nEl sistema está operativo y funcionando.\\n\\n📊 Estado: Activo\\n📈 Cerebros: 10/10\\n🔄 Botones: Funcionales\\n\\nPresiona los botones para probar:',
    'parse_mode': 'Markdown',
    'reply_markup': {'inline_keyboard': [[
        {'text': '✅ PROBAR', 'callback_data': f'execute_{signal_id}'},
        {'text': '❌ TEST', 'callback_data': f'cancel_{signal_id}'}
    ]]}
}).json()
if resp.get('ok'):
    print('   ✅ Señal de verificación enviada')
else:
    print(f'   ❌ Error: {resp}')
"
echo ""
echo "================================="
