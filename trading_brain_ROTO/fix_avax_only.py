print("🔧 Arreglando SOLO cerebro_avax_futures.py...")

# Leer archivo
with open('cerebros/cerebro_avax_futures.py', 'r') as f:
    lines = f.readlines()

# Encontrar y corregir línea 12 (índice 11)
if len(lines) >= 12:
    print(f"📝 Línea 12 actual: '{lines[11].rstrip()}'")
    
    # La línea 12 debe comenzar con 4 espacios (def __init__ dentro de clase)
    if 'def __init__' in lines[11]:
        # Quitar todos los espacios/tabs iniciales
        cleaned = lines[11].lstrip()
        # Añadir exactamente 4 espacios
        lines[11] = '    ' + cleaned
        print(f"✅ Línea 12 corregida: '{lines[11].rstrip()}'")
    
    # Guardar
    with open('cerebros/cerebro_avax_futures.py', 'w') as f:
        f.writelines(lines)
    
    print("✅ Archivo guardado")
else:
    print("❌ El archivo tiene menos de 12 líneas")

print("\\n🔍 Probando importación...")
try:
    exec(open('cerebros/cerebro_avax_futures.py').read())
    print("✅ Importación exitosa")
except Exception as e:
    print(f"❌ Error: {e}")
