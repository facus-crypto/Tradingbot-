# Leer archivo
with open('cerebros/cerebro_base_futures.py', 'r') as f:
    lineas = f.readlines()

# Corregir indentación
lineas_corregidas = []
en_clase = False

for i, linea in enumerate(lineas):
    # Línea 18 (índice 17) es donde está el problema
    if i == 17:  # Esta es la línea del def __init__
        # Eliminar espacios/tabs iniciales incorrectos
        linea_corregida = linea.lstrip()
        # Asegurarse de que comienza con 'def'
        if linea_corregida.startswith('def'):
            # Añadir 4 espacios (nivel de método dentro de clase)
            linea_corregida = '    ' + linea_corregida
            print(f'✅ Línea {i+1} corregida: {linea_corregida[:50]}...')
        lineas_corregidas.append(linea_corregida)
    
    # Corregir la siguiente línea también (docstring)
    elif i == 18:
        linea_corregida = '    ' + linea.lstrip()
        lineas_corregidas.append(linea_corregida)
    
    # Para el resto de líneas dentro de la clase, mantener indentación relativa
    elif i > 17 and i < 30:  # Aproximadamente las primeras líneas del método
        if linea.strip():  # Si no es línea vacía
            # Si la línea ya tiene indentación, mantenerla pero ajustar
            if linea.startswith(' ' * 8) or linea.startswith('\t'):
                # Reducir un nivel si es necesario
                linea_corregida = '    ' + linea.lstrip()
            else:
                linea_corregida = '    ' + linea.lstrip()
        else:
            linea_corregida = linea  # Mantener líneas vacías
        lineas_corregidas.append(linea_corregida)
    
    else:
        lineas_corregidas.append(linea)

# Guardar archivo corregido
with open('cerebros/cerebro_base_futures.py', 'w') as f:
    f.writelines(lineas_corregidas)

print('✅ Archivo cerebro_base_futures.py corregido')
print('📋 Mostrando líneas corregidas 15-25:')
for i in range(14, 25):
    if i < len(lineas_corregidas):
        print(f'{i+1:3}: {lineas_corregidas[i].rstrip()}')
