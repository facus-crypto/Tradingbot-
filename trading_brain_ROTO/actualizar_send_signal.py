import json

# Leer el archivo actual
with open('interfaces/telegram_advanced.py', 'r') as f:
    contenido = f.read()

# Buscar la función send_signal
if 'def send_signal' in contenido:
    print('✅ Función send_signal ya existe')
    
    # Verificar si tiene el formato vertical
    if 'symbols_vertical =.*\\n.*\\n.*\\n.*\\n.*\\n.*\\n.*\\n.*\\n.*\\n' in contenido:
        print('✅ Formato vertical ya implementado')
    else:
        print('⚠️  Formato puede necesitar ajustes')
else:
    print('❌ Función send_signal no encontrada')
    
# Mostrar las primeras líneas de la función
import re
match = re.search(r'def send_signal.*?(?=\n\ndef|\nclass|\Z)', contenido, re.DOTALL)
if match:
    print('\n=== PRIMERAS LÍNEAS DE send_signal ===')
    print(match.group()[:500] + '...' if len(match.group()) > 500 else match.group())
