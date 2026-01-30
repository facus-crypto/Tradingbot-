#!/usr/bin/env python3
"""
Corrección paso 1: Añadir 'def' al método obtener_posiciones_activas
"""
import sys
import os

# Ruta al archivo con error
archivo = "core/sistema_principal_futures.py"

# Leer el archivo
with open(archivo, 'r') as f:
    lineas = f.readlines()

# Buscar y corregir la línea 411 (índice 410)
linea_corregida = False
for i, linea in enumerate(lineas):
    if i == 410:  # Línea 411 (0-indexed)
        if "async obtener_posiciones_activas(self)" in linea:
            lineas[i] = "    async def obtener_posiciones_activas(self) -> List[Dict]:\n"
            linea_corregida = True
            print(f"✅ Línea {i+1} corregida:")
            print(f"   ANTES: {linea.strip()}")
            print(f"   DESPUÉS: {lineas[i].strip()}")
            break

if not linea_corregida:
    # Buscar el método en todo el archivo
    for i, linea in enumerate(lineas):
        if "obtener_posiciones_activas(self)" in linea and "async" in linea and "def" not in linea:
            lineas[i] = linea.replace("async obtener_posiciones_activas", "async def obtener_posiciones_activas")
            linea_corregida = True
            print(f"✅ Método corregido en línea {i+1}:")
            print(f"   ANTES: {linea.strip()}")
            print(f"   DESPUÉS: {lineas[i].strip()}")
            break

if linea_corregida:
    # Guardar el archivo corregido
    with open(archivo, 'w') as f:
        f.writelines(lineas)
    print(f"✅ Archivo {archivo} corregido exitosamente")
else:
    print("⚠️  No se encontró el método a corregir")
    print("📄 Mostrando líneas alrededor de la 411:")
    for i in range(405, 415):
        if i < len(lineas):
            print(f"{i+1:4d}: {lineas[i].rstrip()}")

# Verificar sintaxis del archivo corregido
print("\n🔍 Verificando sintaxis...")
try:
    with open(archivo, 'r') as f:
        codigo = f.read()
    compile(codigo, archivo, 'exec')
    print("✅ Sintaxis del archivo verificada correctamente")
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
    print(f"   Línea: {e.lineno}, Columna: {e.offset}")
