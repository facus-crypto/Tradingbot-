import os
import glob

print("🔧 Corrigiendo TODOS los cerebros...")

# Lista de cerebros
cerebros = [
    "cerebro_btc.py", "cerebro_eth_futures.py", "cerebro_sol.py",
    "cerebro_link_futures.py", "cerebro_bnb_futures.py", "cerebro_ada_futures.py",
    "cerebro_avax_futures.py", "cerebro_xrp.py", "cerebro_dot.py", "cerebro_atom.py"
]

for cerebro in cerebros:
    archivo = f"cerebros/{cerebro}"
    if os.path.exists(archivo):
        print(f"📝 Corrigiendo {cerebro}...")
        
        # Leer archivo
        with open(archivo, 'r') as f:
            lines = f.readlines()
        
        # Crear nuevo contenido
        nuevo_contenido = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            nuevo_contenido.append(line)
            
            # Si encontramos def __init__, las siguientes líneas deben estar indentadas
            if 'def __init__' in line and '):' in line:
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('def ') and not lines[i].strip().startswith('async def '):
                    # Esta línea debe tener 4 espacios
                    if lines[i].strip() and not lines[i].startswith('    '):
                        nuevo_contenido.append('    ' + lines[i])
                    else:
                        nuevo_contenido.append(lines[i])
                    i += 1
                continue
            
            i += 1
        
        # Guardar
        with open(archivo, 'w') as f:
            f.writelines(nuevo_contenido)
        
        print(f"✅ {cerebro} corregido")
    else:
        print(f"⚠️  {cerebro} no existe")

print("🎯 TODOS los cerebros corregidos")
print("📋 Probando importaciones...")

# Probar cada cerebro
for cerebro in cerebros[:3]:  # Probar solo los primeros 3
    nombre_clase = cerebro.replace('.py', '').replace('cerebro_', '').title().replace('_', '')
    if '_futures' in cerebro:
        nombre_clase = nombre_clase.replace('Futures', '') + 'Futures'
    
    try:
        exec(f"from cerebros.{cerebro.replace('.py', '')} import Cerebro{nombre_clase}")
        print(f"✅ Cerebro{nombre_clase}: OK")
    except Exception as e:
        print(f"❌ Cerebro{nombre_clase}: {str(e)[:50]}...")

print("🚀 Ejecuta: python3 iniciar_sistema_futures.py")
