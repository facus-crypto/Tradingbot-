import logging
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class TelegramAdvancedBot:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
        logger.info(f"Bot Telegram inicializado para chat: {chat_id}")

    async def start(self):
        """Método dummy para compatibilidad con sistema principal"""
        return True

    def send_message(self, text: str, parse_mode="Markdown"):
        """Envía mensaje simple a Telegram."""
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            response = requests.post(f"{self.base_url}/sendMessage", json=payload)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            return False

    def send_signal(self, signal_id, symbol, side, entry, sl, tp, comment, trailing_info=None):
        """Envía señal de trading con botones."""
        try:
            message = (
                f"🚨 *SEÑAL #{signal_id}*\n\n"
                f"• *Par:* `{symbol}`\n"
                f"• *Acción:* {side}\n"
                f"• *Entrada:* `{entry:.2f}`\n"
                f"• *Stop Loss:* `{sl:.2f}`\n"
                f"• *Take Profit:* `{tp:.2f}`\n"
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

    def send_status(self, cerebros_activos=10, modo="Señales manuales", trailing_configurado=True):
        """Envía estado del sistema (comando /status)."""
        try:
            mercados = ["BTC", "ETH", "SOL", "LINK", "BNB", "ADA", "AVAX", "XRP", "DOT", "ATOM"]
            
            mensaje = "✅ *SISTEMA OPERATIVO*\n\n"
            mensaje += f"• {cerebros_activos}/10 cerebros activos\n"
            mensaje += f"• Modo: {modo}\n"
            mensaje += "• Bot funcionando\n"
            
            if trailing_configurado:
                mensaje += "• Trailing stop configurado\n"
            else:
                mensaje += "• Trailing stop: Desactivado\n"
            
            mensaje += "\n📋 *Mercados monitoreados:*\n"
            for mercado in mercados:
                mensaje += f"• {mercado}\n"
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            mensaje += f"\n_🕐 Actualizado: {timestamp}_"
            
            payload = {
                "chat_id": self.chat_id,
                "text": mensaje,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            
            response = requests.post(f"{self.base_url}/sendMessage", json=payload)
            if response.status_code == 200:
                logger.info("✅ Estado del sistema enviado")
                return True
            else:
                logger.error(f"❌ Error enviando estado: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Error en send_status: {e}")
            return False

    def send_test_buttons(self):
        """Envía mensaje con botones de prueba."""
        try:
            mensaje = "## Mensajes no leídos\n\n### SISTEMA VERIFICADO\n\n"
            mensaje += "El sistema está operativo y funcionando.\n\n"
            mensaje += "- **Estado**: Activo\n"
            mensaje += "- **Cerebros**: 10/10\n"
            mensaje += "- **Botones**: Funcionales\n\n"
            mensaje += "Presiona los botones para probar:"
            
            payload = {
                "chat_id": self.chat_id,
                "text": mensaje,
                "parse_mode": "Markdown",
                "reply_markup": {
                    "inline_keyboard": [[
                        {"text": "**PROBAR**", "callback_data": "test_action"},
                        {"text": "**TEST**", "callback_data": "test_action2"}
                    ]]
                }
            }
            
            response = requests.post(f"{self.base_url}/sendMessage", json=payload)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ Error en send_test_buttons: {e}")
            return False

def send_signal(signal_id, symbol, side, entry, sl, tp, comment, trailing_info=None):
    """Función helper para compatibilidad."""
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
