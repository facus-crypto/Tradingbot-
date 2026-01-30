print("🔧 Corrigiendo sistema...")
import os

# 1. Crear cerebro base simple
base_code = '''
import logging
logger = logging.getLogger(__name__)

class CerebroFuturesBase:
    def __init__(self, symbol: str, binance_manager=None, telegram_bot=None):
        self.symbol = symbol
        self.binance = binance_manager
        self.telegram = telegram_bot
        self.estado = "ACTIVO"
        logger.info(f"Cerebro {symbol} listo")
    
    def calcular_trailing_directo(self, entrada, actual, ganancia=None):
        if ganancia is None or ganancia <= 0.01:
            return entrada * 0.98, entrada * 1.03, 1
        elif ganancia <= 0.07:
            return actual * 0.995, actual * 1.02, 2
        else:
            return actual * 0.9975, actual * 1.01, 3
    
    def get_estado(self):
        return {"simbolo": self.symbol, "estado": self.estado}
'''

with open('cerebros/cerebro_base_futures.py', 'w') as f:
    f.write(base_code)
print("✅ cerebro_base_futures.py creado")

# 2. Probar importación
try:
    from cerebros.cerebro_base_futures import CerebroFuturesBase
    test = CerebroFuturesBase('TEST')
    print(f"✅ Importación funciona: {test.get_estado()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("🎯 Sistema corregido. Ahora ejecuta: python3 iniciar_sistema_futures.py")
