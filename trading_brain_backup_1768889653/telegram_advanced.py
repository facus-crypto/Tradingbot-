
"""
Módulo avanzado de Telegram para el sistema de trading
Versión SIMPLIFICADA - Solo funcionalidades básicas
"""
import logging
from typing import Dict, Optional
import aiohttp
import asyncio

logger = logging.getLogger(__name__)

class TelegramAdvancedBot:
    """Bot simplificado de Telegram (sin botones complejos)"""
    
    def __init__(self, token: str, chat_id: str, binance_manager=None):
        self.token = token
        self.chat_id = chat_id
        self.binance_manager = binance_manager
        self.base_url = f"https://api.telegram.org/bot{token}"
        
        logger.info(f"🤖 Telegram Bot inicializado para chat: {chat_id}")
        logger.info(f"   • Token: {token[:10]}...")
    
    async def iniciar(self):
        """Iniciar el bot (versión simplificada)"""
        try:
            # Probar conexión
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/getMe"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        bot_name = data.get('result', {}).get('first_name', 'Bot')
                        logger.info(f"✅ Bot '{bot_name}' conectado a Telegram")
                        
                        # Enviar mensaje de inicio
                        await self.enviar_mensaje(
                            "🚀 *SISTEMA DE TRADING INICIADO*\n"
                            "Bot de Telegram configurado correctamente\n"
                            "• 5 cerebros activos\n"
                            "• Modo: Binance Real\n"
                            "• Señales automáticas activadas"
                        )
                        return True
                    else:
                        logger.error(f"❌ Error conectando a Telegram: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error iniciando Telegram: {e}")
            return False
    
    async def enviar_mensaje(self, texto: str, parse_mode: str = "Markdown"):
        """Enviar mensaje simple al chat"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/sendMessage"
                payload = {
                    "chat_id": self.chat_id,
                    "text": texto,
                    "parse_mode": parse_mode
                }
                
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        logger.debug(f"📨 Mensaje enviado a Telegram")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Error enviando mensaje: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error en enviar_mensaje: {e}")
            return False
    
    async def send_signal(self, signal_data: Dict) -> Optional[int]:
        """Enviar señal de trading (versión simplificada)"""
        try:
            symbol = signal_data.get('symbol', '')
            action = signal_data.get('action', '')
            confidence = signal_data.get('confidence', 0)
            entry_price = signal_data.get('entry_price', 0)
            stop_loss = signal_data.get('stop_loss', 0)
            take_profit = signal_data.get('take_profit', 0)
            
            # Crear mensaje simple
            message = (
                f"📈 *SEÑAL DE TRADING*\n"
                f"• Símbolo: {symbol}\n"
                f"• Acción: {action}\n"
                f"• Confianza: {confidence:.0%}\n"
                f"• Entrada: {entry_price:.2f}\n"
                f"• Stop Loss: {stop_loss:.2f}\n"
                f"• Take Profit: {take_profit:.2f}"
            )
            
            # Añadir razones si existen
            razones = signal_data.get('razones', [])
            if razones:
                message += f"\n• Razones: {', '.join(razones[:3])}"  # Máximo 3 razones
            
            # Enviar mensaje
            success = await self.enviar_mensaje(message)
            
            if success:
                logger.info(f"📤 Señal enviada a Telegram: {symbol} {action}")
                return 1  # Simulamos message_id
            else:
                return None
                
        except Exception as e:
            logger.error(f"❌ Error en send_signal: {e}")
            return None
    
    async def detener(self):
        """Detener el bot (nada que hacer en versión simple)"""
        logger.info("🤖 Telegram Bot detenido")

# Instancia global
telegram_bot_instance = None

def get_telegram_bot(token: str, chat_id: str, binance_manager=None):
    """Obtener instancia del bot de Telegram"""
    global telegram_bot_instance
    if telegram_bot_instance is None:
        telegram_bot_instance = TelegramAdvancedBot(token, chat_id, binance_manager)
    return telegram_bot_instance
