#!/bin/bash
echo "🚨 SOLUCIÓN DEFINITIVA - NO TOCAR LÓGICA, SOLO FORMATEAR"

# Backup
backup="cerebros_backup_$(date +%s)"
cp -r cerebros "$backup"
echo "✅ Backup creado: $backup"

# Formatear SOLO indentación
for archivo in cerebros/*.py; do
    echo "📝 Formateando: $(basename $archivo)"
    # Usar Python para reformatear
    python3 -c "
import re
with open('$archivo', 'r') as f:
    lines = f.readlines()

# Corregir indentación básica
new_lines = []
indent_level = 0
in_class = False

for line in lines:
    stripped = line.strip()
    
    # Detectar clase
    if stripped.startswith('class '):
        in_class = True
        indent_level = 4
        new_lines.append(line)
        continue
    
    # Dentro de clase
    if in_class:
        # Métodos deben tener 4 espacios
        if stripped.startswith('def ') and '):' in line:
            if not line.startswith(' ' * 4):
                line = ' ' * 4 + line.lstrip()
        # Código dentro de métodos debe tener 8 espacios
        elif line.strip() and not line.startswith(' ' * 8) and not line.startswith(' ' * 4):
            line = ' ' * 8 + line.lstrip()
    
    new_lines.append(line)

# Guardar
with open('$archivo', 'w') as f:
    f.writelines(new_lines)
"
done

echo "🎯 Formateo completado"
echo "🔍 Probando sistema..."
python3 iniciar_sistema_futures.py 2>&1 | head -20
