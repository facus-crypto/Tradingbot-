# Leer archivo
with open('cerebros/cerebro_base_futures.py', 'r') as f:
    lineas = f.readlines()

print('🔍 Analizando estructura del archivo...')

# Encontrar dónde termina __init__ y comienzan otros métodos
en_init = False
lineas_corregidas = []

for i, linea in enumerate(lineas):
    # Detectar inicio de __init__
    if 'def __init__' in linea:
        en_init = True
        lineas_corregidas.append(linea)
        print(f'✅ Inicio __init__ en línea {i+1}')
    
    # Detectar fin de __init__ (cuando encontramos otro método)
    elif en_init and linea.strip().startswith('async def') or linea.strip().startswith('def '):
        # Esta línea debería estar fuera de __init__
        print(f'⚠️  Método encontrado dentro de __init__ en línea {i+1}: {linea[:50]}...')
        
        # Corregir: quitar 4 espacios para sacarlo de __init__
        linea_corregida = linea[4:] if linea.startswith('    ') else linea
        lineas_corregidas.append(linea_corregida)
        en_init = False
    
    # Si estamos en __init__, mantener indentación
    elif en_init:
        if linea.strip() and not (linea.startswith('        ') or linea.startswith('    ') and len(linea) > len(linea.lstrip())):
            # Esta línea debería tener 8 espacios dentro de __init__
            lineas_corregidas.append('        ' + linea.lstrip())
        else:
            lineas_corregidas.append(linea)
    
    # Fuera de __init__
    else:
        # Asegurar que métodos de clase tengan 4 espacios
        if linea.strip().startswith('async def') or linea.strip().startswith('def '):
            if not linea.startswith('    '):
                lineas_corregidas.append('    ' + linea.lstrip())
            else:
                lineas_corregidas.append(linea)
        else:
            lineas_corregidas.append(linea)

# Guardar archivo corregido
with open('cerebros/cerebro_base_futures.py', 'w') as f:
    f.writelines(lineas_corregidas)

print('✅ Archivo corregido')
print('\n📋 Mostrando estructura corregida:')

# Mostrar las primeras 70 líneas
for i in range(min(70, len(lineas_corregidas))):
    linea = lineas_corregidas[i]
    if linea.strip():  # Solo mostrar líneas con contenido
        print(f'{i+1:3}: {linea.rstrip()}')
