import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

import logging
import asyncio
import json
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SistemaPrincipalFutures:
    def __init__(self):
        self.config = None
        self.binance_manager = None
        self.telegram_bot = None
        self.cerebros = {}
        
    async def inicializar(self):
        logger.info("🚀 Iniciando Sistema de Trading Futures...")
        
        # 1. Cargar configuración
        await self.cargar_configuracion()
        
        # 2. Inicializar Binance
        await self.inicializar_binance()
        
        # 3. Inicializar Telegram
        await self.inicializar_telegram()
        
        # 4. Inicializar cerebros
        await self.inicializar_cerebros()
        
        logger.info("✅ Sistema completamente inicializado")
        return True
    
    async def cargar_configuracion(self):
        try:
            with open('config_futures.json', 'r') as f:
                self.config = json.load(f)
            logger.info("✅ Configuración cargada")
        except Exception as e:
            logger.error(f"❌ Error cargando configuración: {e}")
            raise
    
    async def inicializar_binance(self):
        try:
            from binance_manager_custom import BinanceFuturesManagerCustom
            api_key = self.config['binance']['api_key']
            api_secret = self.config['binance']['api_secret']
            testnet = self.config['binance']['testnet']
            
            self.binance_manager = BinanceFuturesManagerCustom(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet
            )
            logger.info("✅ Binance inicializado")
        except Exception as e:
            logger.warning(f"⚠️  Binance no inicializado: {e}")
            self.binance_manager = None
    
    async def inicializar_telegram(self):
        try:
            from interfaces.telegram_advanced import TelegramAdvancedBot
            token = self.config['telegram']['token']
            chat_id = self.config['telegram']['chat_id']
            
            self.telegram_bot = TelegramAdvancedBot(token=token, chat_id=chat_id)
            await self.telegram_bot.start()
            logger.info("✅ Telegram inicializado")
        except Exception as e:
            logger.warning(f"⚠️  Telegram no inicializado: {e}")
            self.telegram_bot = None
    
    async def inicializar_cerebros(self):
        try:
            cerebros_config = self.config['cerebros']
            
            # Importar todos los cerebros
            from cerebros.cerebro_btc import CerebroBTC
            from cerebros.cerebro_eth import CerebroETH
            from cerebros.cerebro_sol import CerebroSOL
            from cerebros.cerebro_link import CerebroLINK
            from cerebros.cerebro_bnb import CerebroBNB
            from cerebros.cerebro_ada import CerebroADA
            from cerebros.cerebro_avax_futures import CerebroAVAXFutures
            from cerebros.cerebro_xrp import CerebroXRP
            from cerebros.cerebro_dot import CerebroDOT
            from cerebros.cerebro_atom import CerebroATOM
            
            cerebros_clases = {
                'BTCUSDT': CerebroBTC,
                'ETHUSDT': CerebroETH,
                'SOLUSDT': CerebroSOL,
                'LINKUSDT': CerebroLINK,
                'BNBUSDT': CerebroBNB,
                'ADAUSDT': CerebroADA,
                'AVAXUSDT': CerebroAVAXFutures,
                'XRPUSDT': CerebroXRP,
                'DOTUSDT': CerebroDOT,
                'ATOMUSDT': CerebroATOM
            }
            
            for simbolo, ClaseCerebro in cerebros_clases.items():
                if cerebros_config[simbolo]['activo']:
                    cerebro = ClaseCerebro(
                        binance_manager=self.binance_manager,
                        telegram_bot=self.telegram_bot
                    )
                    self.cerebros[simbolo] = cerebro
                    logger.info(f"✅ Cerebro {simbolo} inicializado")
            
            logger.info(f"✅ {len(self.cerebros)} cerebros inicializados")
        except Exception as e:
            logger.error(f"❌ Error inicializando cerebros: {e}")
            raise
    
    async def run(self):
        """Bucle principal del sistema"""
        logger.info("🔁 Iniciando bucle principal...")
        while True:
            try:
                # Aquí iría la lógica de trading
                await asyncio.sleep(60)
            except KeyboardInterrupt:
                logger.info("👋 Deteniendo sistema...")
                break
            except Exception as e:
                logger.error(f"❌ Error en bucle principal: {e}")
                await asyncio.sleep(10)

async def main():
    sistema = SistemaPrincipalFutures()
    try:
        await sistema.inicializar()
        await sistema.run()
    except KeyboardInterrupt:
        logger.info("👋 Sistema detenido por usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    asyncio.run(main())
