#!/usr/bin/env python3
"""
Corregir duplicado de binance_manager en línea 269
"""
archivo = "core/sistema_principal_futures.py"

print("🔧 CORRIGIENDO DUPLICADO EN LÍNEA 269")
print("=" * 50)

# Leer el archivo
with open(archivo, 'r') as f:
    lineas = f.readlines()

# Mostrar el problema
print("📋 PROBLEMA ENCONTRADO:")
print("Línea 268: cerebro = clase_cerebro(binance_manager=self.binance_manager,")
print("Línea 269:     binance_manager=self.binance_manager,  ← ¡DUPLICADO!")
print("Línea 270:     telegram_bot=self.telegram_bot")

print("\n🔄 CORRIGIENDO...")

# Línea 268 (índice 267) ya tiene binance_manager
# Línea 269 (índice 268) es el duplicado - ELIMINARLA
if len(lineas) > 268:
    print(f"\nEliminando línea 269 duplicada...")
    print(f"ANTES - Línea 269: '{lineas[268].rstrip()}'")
    
    # Eliminar la línea 269 completamente (el duplicado)
    lineas.pop(268)
    
    print("DESPUÉS - Línea 269 eliminada")
    
    # También necesitamos ajustar la línea 268 para que termine correctamente
    if len(lineas) > 267:
        linea_268 = lineas[267]
        if linea_268.strip().endswith(','):
            # Ya termina con coma, está bien
            pass
        else:
            # Añadir coma si no la tiene
            lineas[267] = linea_268.rstrip() + ",\n"
            print("Añadida coma al final de línea 268")
    
    # Guardar corrección
    with open(archivo, 'w') as f:
        f.writelines(lineas)
    
    print("\n✅ Archivo corregido")
    
    # Mostrar resultado
    print("\n📄 LÍNEAS CORREGIDAS (268-270):")
    for i in range(266, 271):
        if i < len(lineas):
            print(f"{i+1:4d}: {lineas[i].rstrip()}")
            
else:
    print("❌ El archivo no tiene suficientes líneas")

print("\n🔍 VERIFICANDO SINTAXIS...")

# Verificar sintaxis
try:
    with open(archivo, 'r') as f:
        codigo = f.read()
    compile(codigo, archivo, 'exec')
    print("✅ Sintaxis CORRECTA")
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
    print(f"   Línea: {e.lineno}")
    if hasattr(e, 'text'):
        print(f"   Texto: {e.text}")

print("\n🎯 PROBAR IMPORTACIÓN...")

test_import = '''
import sys
sys.path.append('.')

try:
    from core.sistema_principal_futures import SistemaPrincipalFutures
    print("✅ Importación EXITOSA")
    
    # Probar crear instancia
    sistema = SistemaPrincipalFutures()
    print("✅ Instancia creada")
    
    print("🎉 ¡CORRECCIÓN EXITOSA!")
    
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
    print(f"   En línea: {e.lineno}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
'''

with open("test_import.py", "w") as f:
    f.write(test_import)

import subprocess
result = subprocess.run(["python", "test_import.py"], capture_output=True, text=True)
print(result.stdout)

if result.stderr:
    print("⚠️  Errores:", result.stderr)

import os
os.remove("test_import.py")

print("\n" + "=" * 50)
if "✅ Importación EXITOSA" in result.stdout:
    print("🚀 ¡CORRECCIÓN COMPLETADA!")
    print("📋 EJECUTAR SISTEMA:")
    print("python iniciar_sistema_futures.py")
else:
    print("⚠️  Aún hay problemas")
