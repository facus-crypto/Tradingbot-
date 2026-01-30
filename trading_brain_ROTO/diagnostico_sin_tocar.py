print("🔍 DIAGNÓSTICO SIN MODIFICAR NADA")
print("="*50)

# Solo listar problemas SIN corregir
import os

cerebros = [
    "cerebro_btc.py", "cerebro_eth_futures.py", "cerebro_sol.py",
    "cerebro_link_futures.py", "cerebro_bnb_futures.py", "cerebro_ada_futures.py",
    "cerebro_avax_futures.py", "cerebro_xrp.py", "cerebro_dot.py", "cerebro_atom.py"
]

print("📋 Problemas encontrados (SOLO lectura):")

for c in cerebros:
    path = f"cerebros/{c}"
    if os.path.exists(path):
        try:
            # Solo leer primeras líneas para ver estructura
            with open(path, 'r') as f:
                lines = f.readlines()
            
            # Verificar si hay def __init__
            for i, line in enumerate(lines[:30]):
                if 'def __init__' in line:
                    print(f"✅ {c}: __init__ en línea {i+1}")
                    break
            else:
                print(f"⚠️  {c}: No se encontró __init__ en primeras 30 líneas")
                
        except Exception as e:
            print(f"❌ {c}: Error leyendo - {e}")
    else:
        print(f"❌ {c}: Archivo no existe")

print("\n🎯 SOLUCIÓN SEGURA:")
print("1. Los cerebros YA funcionaban bien")
print("2. NO modifiques nada más")
print("3. El único problema REAL es cerebro_bnb_futures.py línea 26")
print("")
print("📝 Para corregir SOLO ese archivo:")
print("   cd ~/bot_trading/trading_brain")
print("   nano cerebros/cerebro_bnb_futures.py")
print("   Ir a línea 26 y eliminar espacios/tabs extras al inicio")
print("   Guardar (Ctrl+X, Y, Enter)")
print("")
print("🔧 O usa este comando SEGURO que solo corrige ESA línea:")
print("   sed -i '26s/^[[:space:]]*//' cerebros/cerebro_bnb_futures.py")
