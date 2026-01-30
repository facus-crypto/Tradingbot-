import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cerebros.cerebro_sol import CerebroSOL

async def prueba():
    print('🧠 Probando Cerebro SOL...')
    cerebro = CerebroSOL()
    señal = await cerebro.analizar()
    
    if señal:
        print(f'✅ SEÑAL ENCONTRADA:')
        print(f'   Símbolo: {señal["simbolo"]}')
        print(f'   Dirección: {señal["direccion"]} ({señal["tipo_entrada"]})')
        print(f'   Fuerza: {señal["fuerza"]}/10')
        print(f'   Precio: ${señal["precio_entrada"]:.2f}')
    else:
        print('⚠️ No hay señal para SOL en este momento')

if __name__ == "__main__":
    asyncio.run(prueba())
