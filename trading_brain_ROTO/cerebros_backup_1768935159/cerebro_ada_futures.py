import logging
from datetime import datetime
from cerebros.cerebro_base_futures import CerebroFuturesBase

logger = logging.getLogger(__name__)

class CerebroADAFutures(CerebroFuturesBase):
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("ADAUSDT", binance_manager, telegram_bot)
        self.config = {
            "combinacion": "canal_tendencia_rsi_div",
            "timeframe_analisis": "1h"
        }
        self.estrategia = "Canal Tendencia + RSI Div"
        logger.info(f"🧠 Cerebro BTC inicializado - {self.estrategia}")
    
    async def analizar(self):
        try:
            logger.info(f"🔍 Analizando {self.symbol}...")
            # Simulación de análisis
            self.ultima_senal = {
                "timestamp": datetime.now(),
                "direccion": "NEUTRAL",
                "confianza": 0.5
            }
            self.estado = "ANALIZANDO"
            return self.ultima_senal
        except Exception as e:
            logger.error(f"❌ Error analizando BTC: {e}")
            return None
    
    def get_estado(self):
        estado_base = super().get_estado()
        estado_base.update({
            "estrategia": self.estrategia,
            "config": self.config,
            "ultimo_analisis": self.ultima_senal
        })
        return estado_base
