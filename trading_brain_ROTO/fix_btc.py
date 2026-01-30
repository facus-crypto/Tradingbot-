with open('cerebros/cerebro_btc.py', 'r') as f:
    lines = f.readlines()

# Buscar línea con def __init__
for i, line in enumerate(lines):
    if 'def __init__' in line:
        print(f"✅ __init__ en línea {i+1}")
        # Las siguientes líneas deben tener 4 espacios más
        for j in range(i+1, len(lines)):
            # Si la línea no está vacía y no es otro método
            if lines[j].strip() and not lines[j].strip().startswith('def '):
                # Añadir 4 espacios si no los tiene
                if not lines[j].startswith('    '):
                    lines[j] = '    ' + lines[j]
            elif lines[j].strip().startswith('def '):
                # Fin del __init__
                break
        
        # Guardar
        with open('cerebros/cerebro_btc.py', 'w') as f:
            f.writelines(lines)
        print("✅ cerebro_btc.py corregido")
        break
