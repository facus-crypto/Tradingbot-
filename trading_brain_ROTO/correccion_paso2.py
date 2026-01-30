#!/usr/bin/env python3
"""
Corrección paso 2: Corregir error en cerebro_bnb_futures.py línea 381
El error es 'await' outside async function
"""
import sys
import os

# Ruta al archivo con error
archivo = "cerebros/cerebro_bnb_futures.py"

# Leer el archivo
with open(archivo, 'r') as f:
    lineas = f.readlines()

print(f"🔍 Analizando {archivo}...")

# Buscar la línea 381 (índice 380)
error_corregido = False
for i, linea in enumerate(lineas):
    if i == 380:  # Línea 381 (0-indexed)
        print(f"📄 Línea {i+1} (actual): {linea.strip()}")
        
        # Verificar si la línea tiene 'await' sin contexto async
        if "await self.btc_cerebro.obtener_datos_binance" in linea:
            # Necesitamos ver el contexto - probablemente falta async en el método
            # Buscamos el método que contiene esta línea
            print("🔍 Buscando método que contiene esta línea...")
            
            # Buscar hacia arriba para encontrar el inicio del método
            inicio_metodo = -1
            for j in range(i, max(i-50, -1), -1):
                if "def " in lineas[j] and "generar_senal" in lineas[j]:
                    inicio_metodo = j
                    print(f"   Método encontrado en línea {j+1}: {lineas[j].strip()}")
                    break
            
            if inicio_metodo != -1:
                # Verificar si el método tiene 'async'
                if "async" not in lineas[inicio_metodo]:
                    print(f"⚠️  El método no tiene 'async', agregando...")
                    lineas[inicio_metodo] = lineas[inicio_metodo].replace(
                        "def generar_senal",
                        "async def generar_senal"
                    )
                    error_corregido = True
                    print(f"✅ Método corregido en línea {inicio_metodo+1}")
                else:
                    print("✅ El método ya tiene 'async'")
            else:
                print("⚠️  No se pudo encontrar el método 'generar_senal'")
                print("📝 Corrigiendo directamente la línea...")
                # Corregir directamente la línea (esto podría no ser suficiente)
                if "btc_data = await self.btc_cerebro.obtener_datos_binance" in linea:
                    # Verificar si estamos dentro de un contexto try
                    print("   La línea parece estar dentro de un try")
                    print("   Verificando si necesitamos await o no...")
                    
                    # Podría ser que falta marcar el método como async
                    # Pero para corregir rápido, comentamos y verificamos
                    print("   📋 Mostrando contexto (líneas 375-385):")
                    for k in range(375, 385):
                        if k < len(lineas):
                            print(f"   {k+1:4d}: {lineas[k].rstrip()}")

# Si encontramos y corregimos el error
if error_corregido:
    # Guardar el archivo corregido
    with open(archivo, 'w') as f:
        f.writelines(lineas)
    print(f"\n✅ Archivo {archivo} corregido")
else:
    print("\n⚠️  No se pudo corregir automáticamente")
    print("📄 Mostrando el área del error en detalle (líneas 370-390):")
    for i in range(370, 390):
        if i < len(lineas):
            prefix = ">>>" if i == 380 else "   "
            print(f"{prefix} {i+1:4d}: {lineas[i].rstrip()}")

# Verificar sintaxis nuevamente
print("\n🔍 Verificando sintaxis después de corrección...")
try:
    with open(archivo, 'r') as f:
        codigo = f.read()
    compile(codigo, archivo, 'exec')
    print("✅ Sintaxis del archivo verificada correctamente")
except SyntaxError as e:
    print(f"❌ Error de sintaxis: {e}")
    print(f"   Línea: {e.lineno}, Columna: {e.offset}")
    print(f"   Texto: {e.text}")
