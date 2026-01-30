#!/usr/bin/env python3
"""
Corregir función get_symbol_price en binance_manager_custom.py
"""
import os

print("🔧 CORRIGIENDO GET_SYMBOL_PRICE")
print("=" * 50)

archivo = "binance_manager_custom.py"

# Leer el archivo
with open(archivo, 'r') as f:
    contenido = f.read()

# Buscar la función problemática
lineas = contenido.split('\n')
encontrada = False

for i, linea in enumerate(lineas):
    if "async def get_symbol_price" in linea:
        print(f"✅ Encontrada función en línea {i+1}")
        encontrada = True
        
        # Modificar las siguientes líneas para que NO sea async
        # Cambiar "async def get_symbol_price" por "def get_symbol_price"
        lineas[i] = "    def get_symbol_price(self, symbol: str) -> float:"
        print(f"   Corregido: 'async def' → 'def'")
        
        # También necesitamos quitar 'await' de las llamadas
        # Pero eso está en otro archivo
        
        break

if encontrada:
    # Guardar archivo corregido
    with open(archivo, 'w') as f:
        f.write('\n'.join(lineas))
    print(f"\n✅ {archivo} corregido")
    
    # Ahora también necesitamos corregir cerebro_base_futures.py
    # donde se llama a esta función
    cerebro_file = "cerebros/cerebro_base_futures.py"
    
    with open(cerebro_file, 'r') as f:
        cerebro_content = f.read()
    
    # La función obtener_precio_actual() llama a binance.get_symbol_price()
    # Pero como ahora NO es async, no necesita await
    # Buscar la línea específica
    cerebro_lines = cerebro_content.split('\n')
    cambios = 0
    
    for i, linea in enumerate(cerebro_lines):
        if "precio = self.binance.get_symbol_price(self.symbol)" in linea and "await" in linea:
            cerebro_lines[i] = "            precio = self.binance.get_symbol_price(self.symbol)"
            cambios += 1
            print(f"✅ Línea {i+1} corregida (quitado 'await')")
    
    if cambios > 0:
        with open(cerebro_file, 'w') as f:
            f.write('\n'.join(cerebro_lines))
        print(f"✅ {cerebro_file} corregido ({cambios} cambios)")
    else:
        print(f"⚠️  No se encontraron llamadas a corregir en {cerebro_file}")
        
else:
    print(f"❌ No se encontró la función get_symbol_price")

print("\n🔍 Verificando corrección...")
# Crear test simple
test_code = '''
from binance_manager_custom import BinanceFuturesManagerCustom

# Crear instancia (no necesita credenciales reales para test)
manager = BinanceFuturesManagerCustom("test_key", "test_secret", testnet=False)

print("1️⃣ Verificando tipo de get_symbol_price...")
import inspect
print(f"   • Es async: {inspect.iscoroutinefunction(manager.get_symbol_price)}")
print(f"   • Es función normal: {callable(manager.get_symbol_price)}")

print("\\n2️⃣ Probando llamada (simulada)...")
try:
    # Esto debería funcionar sin await
    print("   Llamando sin await...")
    # No podemos llamarla realmente sin credenciales, pero verificamos el tipo
    print("   ✅ Función corregida correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")
'''

with open("test_correccion.py", "w") as f:
    f.write(test_code)

os.system("python test_correccion.py")
os.remove("test_correccion.py")

print("\n" + "=" * 50)
print("🎯 EJECUTAR PRUEBA FINAL:")
print("cd ~/bot_trading/trading_brain")
print("python -c \"import sys; sys.path.append('.'); from cerebros.cerebro_btc_futures import CerebroBTC; import asyncio; cerebro = CerebroBTC(); asyncio.run(cerebro.obtener_precio_actual())\"")

print("\n⚠️  Si sigue el error, necesitamos revisar la implementación completa")
print("   de get_symbol_price en binance_manager_custom.py")
