import logging
import requests

logger = logging.getLogger(__name__)

class TelegramAdvancedBot:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
        logging.info(f"Bot Telegram inicializado para chat: {chat_id}")

    async def start(self):
        """Método dummy para compatibilidad con sistema principal"""
        return True

    def send_message(self, text: str):
        """Método dummy para compatibilidad"""
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }
            response = requests.post(f"{self.base_url}/sendMessage", json=payload)
            return response.status_code == 200
        except:
            return False

    def send_signal(self, signal_id, symbol, side, entry, sl, tp, comment, trailing_info=None):
        try:
            message = (
                f"🚨 *SEÑAL #{signal_id}*\n\n"
                f"• *Par:* `{symbol}`\n"
                f"• *Acción:* {side}\n"
                f"• *Entrada:* `{entry:.8f}`\n"
                f"• *Stop Loss:* `{sl:.8f}`\n"
                f"• *Take Profit:* `{tp:.8f}`\n"
                f"• *Comentario:* {comment}\n"
            )
            if trailing_info:
                message += f"• *Trailing Stop:* Fase {trailing_info['fase']}\n"
            
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "reply_markup": {
                    "inline_keyboard": [[
                        {"text": "✅ EJECUTAR", "callback_data": f"execute_{signal_id}"},
                        {"text": "❌ CANCELAR", "callback_data": f"cancel_{signal_id}"}
                    ]]
                }
            }
            
            response = requests.post(f"{self.base_url}/sendMessage", json=payload)
            if response.status_code == 200:
                logger.info(f"✅ Señal {signal_id} enviada a Telegram")
                return True
            else:
                logger.error(f"❌ Error enviando señal: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Error enviando señal: {e}")
            return False

def send_signal(signal_id, symbol, side, entry, sl, tp, comment, trailing_info=None):
    """Función helper para compatibilidad"""
    try:
        import json
        with open('config_futures.json', 'r') as f:
            config = json.load(f)
        token = config['telegram']['token']
        chat_id = config['telegram']['chat_id']
        bot = TelegramAdvancedBot(token, chat_id)
        return bot.send_signal(signal_id, symbol, side, entry, sl, tp, comment, trailing_info)
    except Exception as e:
        logging.error(f"Error: {e}")
        return False
