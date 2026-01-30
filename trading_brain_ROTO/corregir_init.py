# Leer archivo completo
with open('cerebros/cerebro_base_futures.py', 'r') as f:
    contenido = f.read()

# Separar en líneas
lineas = contenido.split('\n')
corregidas = []
en_init = False
nivel_init = 0

for i, linea in enumerate(lineas):
    # Detectar inicio de __init__
    if 'def __init__' in linea:
        corregidas.append(linea)  # La línea del def ya está bien
        en_init = True
        nivel_init = len(linea) - len(linea.lstrip())
        continue
    
    # Si estamos dentro de __init__
    if en_init:
        # Si la línea tiene contenido
        if linea.strip():
            # Si es el final del método (línea sin indentación o nueva definición)
            if linea.lstrip().startswith('def ') or (linea.strip() and len(linea) - len(linea.lstrip()) < nivel_init):
                en_init = False
                corregidas.append(linea)
            else:
                # Añadir 4 espacios adicionales dentro del método
                corregidas.append(' ' * 8 + linea.lstrip())
        else:
            # Línea vacía dentro del método
            if i+1 < len(lineas) and lineas[i+1].strip() and not lineas[i+1].lstrip().startswith('def '):
                corregidas.append(' ' * 8)
            else:
                corregidas.append(linea)
    else:
        corregidas.append(linea)

# Guardar
with open('cerebros/cerebro_base_futures.py', 'w') as f:
    f.write('\n'.join(corregidas))

print('✅ Método __init__ completamente corregido')
print('\n📋 Líneas 18-35 corregidas:')
for i in range(17, 35):
    if i < len(corregidas):
        print(f'{i+1:3}: {corregidas[i]}')
