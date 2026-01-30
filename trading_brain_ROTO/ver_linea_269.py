#!/usr/bin/env python3
"""
Ver y corregir EXACTAMENTE la línea 269
"""
import sys

print("🔍 VIENDO LÍNEA 269 EXACTA")
print("=" * 50)

archivo = "core/sistema_principal_futures.py"

# Leer el archivo
with open(archivo, 'r') as f:
    lineas = f.readlines()

# Línea 269 es índice 268 (0-indexed)
if len(lineas) > 268:
    linea_269 = lineas[268]
    print(f"📄 Línea 269 actual:")
    print(f"   '{linea_269.rstrip()}'")
    
    print("\n🔍 Contexto (líneas 265-275):")
    for i in range(264, 275):
        if i < len(lineas):
            marcador = ">>>" if i == 268 else "   "
            print(f"{marcador} {i+1:4d}: {lineas[i].rstrip()}")
    
    print("\n🎯 PROBLEMA: binance_manager está DUPLICADO")
    print("   Posiblemente en:")
    print("   1. Parámetros de la clase (CerebroXXX(binance_manager=...))")
    print("   2. Llamada explícita (..., binance_manager=self.binance_manager)")
    
    print("\n🔄 SOLUCIÓN: Remover el duplicado")
    
    # Analizar la línea
    if "binance_manager=self.binance_manager" in linea_269:
        print("\n📝 CORRIGIENDO...")
        
        # Opción 1: Si la clase YA tiene binance_manager en sus parámetros
        if "Cerebro" in linea_269 and "(binance_manager" in linea_269:
            print("   La clase YA tiene binance_manager en constructor")
            print("   Eliminando el explícito...")
            
            nueva_linea = linea_269.replace(", binance_manager=self.binance_manager", "")
            lineas[268] = nueva_linea
            
            print(f"   ANTES: {linea_269.rstrip()}")
            print(f"   DESPUÉS: {nueva_linea.rstrip()}")
            
        # Opción 2: Si NO tiene, mantenerlo
        else:
            print("   La clase NO tiene binance_manager en constructor")
            print("   Manteniéndolo...")
        
        # Guardar corrección
        with open(archivo, 'w') as f:
            f.writelines(lineas)
        
        print(f"\n✅ {archivo} corregido")
        
    else:
        print("\n⚠️  binance_manager no encontrado en línea 269")
        print("   El problema puede ser en otra línea")
        
else:
    print(f"❌ El archivo tiene menos de 269 líneas")

print("\n🔍 Verificando sintaxis después de corrección...")

test_sintaxis = f'''
import sys
try:
    with open("{archivo}", 'r') as f:
        codigo = f.read()
    compile(codigo, "{archivo}", 'exec')
    print("✅ Sintaxis CORRECTA")
    
    # Probar importación
    sys.path.append('.')
    from core.sistema_principal_futures import SistemaPrincipalFutures
    print("✅ Importación EXITOSA")
    
    # Probar instancia
    sistema = SistemaPrincipalFutures()
    print("✅ Instancia creada")
    
    print("🎉 ¡ERROR CORREGIDO!")
    
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {{e}}")
    print(f"   Línea: {{e.lineno}}")
    if hasattr(e, 'text'):
        print(f"   Texto: {{e.text}}")
except Exception as e:
    print(f"❌ Error: {{type(e).__name__}}: {{e}}")
'''

with open("verificar_sintaxis.py", "w") as f:
    f.write(test_sintaxis)

import subprocess
result = subprocess.run(["python", "verificar_sintaxis.py"], capture_output=True, text=True)
print(result.stdout)

if result.stderr:
    print("⚠️  Errores:", result.stderr)

import os
os.remove("verificar_sintaxis.py")

print("\n" + "=" * 50)
if "✅ Sintaxis CORRECTA" in result.stdout and "✅ Importación EXITOSA" in result.stdout:
    print("🚀 ¡LISTO PARA EJECUTAR!")
    print("python iniciar_sistema_futures.py")
else:
    print("⚠️  Aún hay problemas. Mostrando MÁS contexto...")
    
    # Mostrar más líneas alrededor del problema
    print("\n🔍 Mostrando líneas 250-280:")
    with open(archivo, 'r') as f:
        todas_lineas = f.readlines()
    
    for i in range(249, 280):
        if i < len(todas_lineas):
            marcador = ">>>" if i == 268 else "   "
            print(f"{marcador} {i+1:4d}: {todas_lineas[i].rstrip()}")
