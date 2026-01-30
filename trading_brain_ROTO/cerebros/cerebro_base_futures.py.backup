import logging
logger = logging.getLogger(__name__)


class CerebroFuturesBase:
    def __init__(self, symbol, binance=None, telegram=None):
        self.symbol = symbol
        self.binance = binance
        self.telegram = telegram
        logger.info(f"Cerebro base creado para {symbol}")

    def calcular_trailing_directo(self, entrada, actual, ganancia=None):
        if ganancia is None or ganancia <= 0.01:
            return entrada * 0.98, entrada * 1.03, 1
        elif ganancia <= 0.07:
            return actual * 0.995, actual * 1.02, 2
        else:
            return actual * 0.9975, actual * 1.01, 3
