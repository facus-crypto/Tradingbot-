print("🆘 RESTAURACIÓN DE EMERGENCIA - CREANDO CEREBROS FUNCIONALES")

# Crear cerebro_ada_futures.py funcional BASADO en cerebro_btc.py
with open('cerebros/cerebro_btc.py', 'r') as f:
    btc_content = f.read()

# Reemplazar para ADA
ada_content = btc_content.replace('BTCUSDT', 'ADAUSDT')\
                         .replace('ema_ribbon_rsi', 'canal_tendencia_rsi_div')\
                         .replace('EMA Ribbon + RSI', 'Canal Tendencia + RSI Div')\
                         .replace('CerebroBTC', 'CerebroADAFutures')\
                         .replace('timeframe_analisis": "15m"', 'timeframe_analisis": "1h"')

with open('cerebros/cerebro_ada_futures.py', 'w') as f:
    f.write(ada_content)

print("✅ cerebro_ada_futures.py RESTAURADO usando plantilla funcional")
print("📋 Ahora prueba: python3 iniciar_sistema_futures.py")
