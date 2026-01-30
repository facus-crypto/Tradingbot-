import os
import re

def agregar_trailing_a_archivo(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()
    
    # Buscar patrones de return de señal
    patrones = [
        # Patrón para return { 'action': 'LONG'... }
        (r"(return\s*\{[^}]+'action'\s*:\s*['\"]LONG['\"][^}]+)\}", r"\1,\n            'stop_loss': sl,\n            'take_profit': tp,\n            'fase_trailing': fase\n        }"),
        (r"(return\s*\{[^}]+'action'\s*:\s*['\"]SHORT['\"][^}]+)\}", r"\1,\n            'stop_loss': sl,\n            'take_profit': tp,\n            'fase_trailing': fase\n        }"),
        # Patrón para return señal (diccionario)
        (r"(senal\s*=\s*\{[^}]+)\}", r"\1,\n            'stop_loss': sl,\n            'take_profit': tp,\n            'fase_trailing': fase\n        }"),
    ]
    
    modificado = False
    for patron, reemplazo in patrones:
        if re.search(patron, contenido, re.DOTALL):
            contenido = re.sub(patron, reemplazo, contenido, flags=re.DOTALL)
            modificado = True
    
    # Agregar cálculo de trailing antes del return
    if modificado:
        # Buscar lugar para insertar cálculo
        lineas = contenido.split('\n')
        nuevas_lineas = []
        for i, linea in enumerate(lineas):
            nuevas_lineas.append(linea)
            if 'return {' in linea and "'action':" in ' '.join(lineas[i:i+10]):
                # Insertar cálculo antes del return
                nuevas_lineas.insert(-1, ' ' * 12 + '# Calcular trailing stop')
                nuevas_lineas.insert(-1, ' ' * 12 + 'sl, tp, fase = self.calcular_trailing_directo(precio_actual, precio_actual)')
        
        contenido = '\n'.join(nuevas_lineas)
        with open(archivo, 'w') as f:
            f.write(contenido)
        print(f"✅ Modificado: {archivo}")
        return True
    
    print(f"⚠️  No se pudo modificar: {archivo}")
    return False

# Aplicar a todos los cerebros
cerebros = [
    'cerebros/cerebro_btc.py',
    'cerebros/cerebro_eth_futures.py',
    'cerebros/cerebro_sol.py',
    'cerebros/cerebro_link_futures.py',
    'cerebros/cerebro_bnb_futures.py',
    'cerebros/cerebro_ada_futures.py',
    'cerebros/cerebro_avax_futures.py',
    'cerebros/cerebro_dot.py',
    'cerebros/cerebro_atom.py'
    # XRP ya tiene
]

for cerebro in cerebros:
    if os.path.exists(cerebro):
        agregar_trailing_a_archivo(cerebro)
    else:
        print(f"❌ No existe: {cerebro}")

print("🎯 Script completado. Verifica los cambios manualmente.")
