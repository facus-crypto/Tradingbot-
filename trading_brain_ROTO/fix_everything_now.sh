#!/bin/bash
echo "🔄 RESTAURANDO SISTEMA COMPLETO..."

# 1. Crear cerebro_base_futures.py CORRECTO
cat > cerebros/cerebro_base_futures.py << 'END'
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
END
echo "✅ cerebro_base_futures.py creado"

# 2. Corregir cerebro_link_futures.py
sed -i '26s/^[[:space:]]*//' cerebros/cerebro_link_futures.py 2>/dev/null || echo "⚠️  No se pudo corregir línea 26"

# 3. Probar
echo "🔍 Probando sistema..."
python3 -c "
try:
    from cerebros.cerebro_base_futures import CerebroFuturesBase
    from cerebros.cerebro_link_futures import CerebroLINK
    print('✅ Importaciones funcionan')
    print('🚀 Ejecuta: python3 iniciar_sistema_futures.py')
except Exception as e:
    print(f'❌ Error: {e}')
"
