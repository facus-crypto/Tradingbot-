import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cerebros.cerebro_btc import CerebroBTC

async def prueba():
    print('🧠 Probando Cerebro BTC...')
    cerebro = CerebroBTC()
    señal = await cerebro.analizar()
    
    if señal:
        print(f'✅ SEÑAL ENCONTRADA:')
        print(f'   Símbolo: {señal["simbolo"]}')
        print(f'   Dirección: {señal["direccion"]}')
        print(f'   Fuerza: {señal["fuerza"]}/10')
        print(f'   Precio: ${señal["precio_entrada"]:.2f}')
        print(f'   Razones: {señal["razones"]}')
    else:
        print('⚠️  No hay señal para BTC en este momento')

if __name__ == "__main__":
    asyncio.run(prueba())
