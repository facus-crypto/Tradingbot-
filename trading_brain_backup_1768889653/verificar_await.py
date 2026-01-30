#!/usr/bin/env python3
"""
Verificar y corregir todos los métodos que usan await pero no son async
"""
import os
import re

print("🔍 BUSCANDO MÉTODOS CON 'await' PERO SIN 'async'")
print("=" * 60)

archivos = [
    "cerebros/cerebro_base_futures.py",
    "cerebros/cerebro_btc_futures.py",
    "cerebros/cerebro_eth_futures.py",
    "cerebros/cerebro_sol_futures.py",
    "cerebros/cerebro_link_futures.py",
    "cerebros/cerebro_bnb_futures.py",
    "core/sistema_principal_futures.py"
]

correcciones_realizadas = []

for archivo in archivos:
    if not os.path.exists(archivo):
        print(f"\n📄 {archivo}: ❌ No existe")
        continue
    
    print(f"\n📄 Analizando: {archivo}")
    
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    cambios = False
    
    # Buscar todas las definiciones de métodos
    for i, linea in enumerate(lineas):
        # Buscar definiciones de métodos (que no sean async)
        if "def " in linea and "async" not in linea and "def __" not in linea:
            metodo_nombre = linea.split("def ")[1].split("(")[0].strip()
            
            # Verificar si este método contiene 'await' en las siguientes líneas
            # Buscar en las próximas 50 líneas o hasta el siguiente método
            busca_hasta = min(i + 50, len(lineas))
            for j in range(i + 1, busca_hasta):
                if "def " in lineas[j] and j > i + 3:  # Nuevo método encontrado
                    break
                
                if "await" in lineas[j] and "def" not in lineas[j]:
                    # ¡Encontramos un método que usa await pero no es async!
                    print(f"   ⚠️  Línea {i+1}: Método '{metodo_nombre}' usa 'await' (línea {j+1}) pero no es async")
                    
                    # Verificar que no sea ya async (por si acaso)
                    if "async def" not in linea:
                        # Corregir
                        lineas[i] = lineas[i].replace("def ", "async def ")
                        cambios = True
                        correcciones_realizadas.append(f"{archivo}: Método '{metodo_nombre}' (línea {i+1})")
                        print(f"   ✅ Corregido: 'def' → 'async def'")
                    break
    
    # Si hubo cambios, guardar el archivo
    if cambios:
        with open(archivo, 'w') as f:
            f.writelines(lineas)
        print(f"   💾 Archivo guardado con correcciones")

print("\n" + "=" * 60)
if correcciones_realizadas:
    print("✅ CORRECCIONES REALIZADAS:")
    for correccion in correcciones_realizadas:
        print(f"   • {correccion}")
else:
    print("✅ No se encontraron métodos con 'await' pero sin 'async'")

# Verificar sintaxis de todos los archivos nuevamente
print("\n🔍 VERIFICACIÓN FINAL DE SINTÁXIS")
print("=" * 60)

todos_correctos = True
for archivo in archivos:
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r') as f:
                codigo = f.read()
            compile(codigo, archivo, 'exec')
            print(f"📄 {archivo}: ✅ Sintaxis correcta")
        except SyntaxError as e:
            print(f"📄 {archivo}: ❌ Error de sintaxis")
            print(f"      Línea {e.lineno}: {e.text.strip()}")
            print(f"      Error: {e}")
            todos_correctos = False
    else:
        print(f"📄 {archivo}: ❌ No existe")
        todos_correctos = False

print("\n" + "=" * 60)
if todos_correctos:
    print("🎉 ¡TODOS los archivos tienen sintaxis correcta!")
    print("\n📋 Puedes probar a ejecutar el sistema:")
    print("   python iniciar_sistema_futures.py")
else:
    print("⚠️  Aún hay errores de sintaxis por corregir")
