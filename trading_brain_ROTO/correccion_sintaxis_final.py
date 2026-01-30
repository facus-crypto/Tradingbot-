#!/usr/bin/env python3
"""
Corrección de error de sintaxis: binance_manager repetido
"""
import sys

print("🔧 CORRECCIÓN DE ERROR DE SINTAXIS")
print("=" * 50)

archivo = "core/sistema_principal_futures.py"

# Leer el archivo
with open(archivo, 'r') as f:
    lineas = f.readlines()

print("🔍 Buscando línea 269 (índice 268)...")

# Mostrar contexto
for i in range(265, 275):
    if i < len(lineas):
        marcador = ">>>" if i == 268 else "   "
        print(f"{marcador} {i+1:4d}: {lineas[i].rstrip()}")

print("\n🎯 PROBLEMA: binance_manager aparece dos veces")
print("   (una en clase_cerebro y otra explícitamente)")

# Buscar y corregir TODAS las ocurrencias
correcciones = 0
for i, linea in enumerate(lineas):
    if "binance_manager=self.binance_manager" in linea:
        # Verificar si binance_manager ya está en los parámetros de clase_cerebro
        if "clase_cerebro(binance_manager" in linea:
            print(f"\n✅ Línea {i+1}: Ya tiene binance_manager en clase_cerebro")
            print(f"   Eliminando duplicado...")
            
            # Remover el binance_manager explícito duplicado
            nueva_linea = linea.replace(", binance_manager=self.binance_manager", "")
            lineas[i] = nueva_linea
            
            print(f"   ANTES: {linea.strip()}")
            print(f"   DESPUÉS: {nueva_linea.strip()}")
            correcciones += 1
            
        elif "clase_cerebro(" in linea and "binance_manager=" not in linea:
            print(f"\n✅ Línea {i+1}: Añadiendo binance_manager faltante")
            # Ya está bien, tiene binance_manager explícito
            correcciones += 1

# También verificar otras instanciaciones
print("\n🔍 Verificando otras instanciaciones de cerebros...")
for i, linea in enumerate(lineas):
    if "cerebro_btc = CerebroBTC(" in linea or \
       "cerebro_eth = CerebroETH(" in linea or \
       "cerebro_sol = CerebroSOL(" in linea or \
       "cerebro_link = CerebroLINK(" in linea or \
       "cerebro_bnb = CerebroBNB(" in linea:
        
        print(f"Línea {i+1}: {linea.strip()}")
        
        # Verificar que tenga binance_manager
        if "binance_manager=" not in linea:
            print(f"   ⚠️  Falta binance_manager")
            # No corregimos automáticamente porque podría ser intencional

if correcciones > 0:
    # Guardar archivo corregido
    with open(archivo, 'w') as f:
        f.writelines(lineas)
    print(f"\n✅ {archivo} corregido ({correcciones} correcciones)")
    
    # Verificar sintaxis
    print("\n🔍 Verificando sintaxis...")
    try:
        with open(archivo, 'r') as f:
            codigo = f.read()
        compile(codigo, archivo, 'exec')
        print("✅ Sintaxis correcta")
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        print(f"   Línea {e.lineno}: {e.text}")
else:
    print("\n⚠️  No se realizaron correcciones")
    print("   El error puede estar en otra parte")

print("\n" + "=" * 50)
print("🚀 EJECUTAR PRUEBA RÁPIDA:")

test_rapido = '''
import sys
sys.path.append('.')
try:
    from core.sistema_principal_futures import SistemaPrincipalFutures
    print("✅ Importación exitosa")
    
    # Probar crear instancia
    sistema = SistemaPrincipalFutures()
    print("✅ Instancia creada")
    
    print("🎉 ¡ERROR DE SINTAXIS CORREGIDO!")
    
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
    print(f"   Archivo: {e.filename}, Línea: {e.lineno}")
    print(f"   Texto: {e.text}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
'''

with open("test_sintaxis.py", "w") as f:
    f.write(test_rapido)

import subprocess
result = subprocess.run(["python", "test_sintaxis.py"], capture_output=True, text=True)
print(result.stdout)

if result.stderr:
    print("⚠️  Errores:", result.stderr)

import os
os.remove("test_sintaxis.py")

print("\n📋 EJECUTAR SISTEMA:")
print("python iniciar_sistema_futures.py")
