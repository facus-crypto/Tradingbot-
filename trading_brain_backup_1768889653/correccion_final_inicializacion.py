#!/usr/bin/env python3
"""
Corrección FINAL de inicialización de cerebros
"""
import sys
sys.path.append('.')

print("🔧 CORRECCIÓN FINAL DE INICIALIZACIÓN")
print("=" * 50)

# Verificar el problema
print("📋 PROBLEMA IDENTIFICADO:")
print("• Los cerebros funcionan CUANDO se les pasa binance_manager")
print("• Pero en sistema_principal_futures.py no se pasa correctamente")
print("• O se pasa, pero hay un timing issue")

# Revisar cómo se inicializan los cerebros
archivo = "core/sistema_principal_futures.py"

with open(archivo, 'r') as f:
    contenido = f.read()

# Buscar la función inicializar_cerebros
lineas = contenido.split('\n')
inicio_cerebros = -1

for i, linea in enumerate(lineas):
    if "async def inicializar_cerebros" in linea:
        inicio_cerebros = i
        print(f"✅ Encontrada función inicializar_cerebros en línea {i+1}")
        break

if inicio_cerebros != -1:
    # Mostrar las siguientes 20 líneas para ver el problema
    print("\n🔍 Revisando implementación actual:")
    for i in range(inicio_cerebros, min(inicio_cerebros + 30, len(lineas))):
        print(f"{i+1:4d}: {lineas[i]}")
        
    print("\n🎯 El problema probable:")
    print("• Los cerebros se crean SIN binance_manager")
    print("• O el manager no está disponible aún")
    
else:
    print("❌ No se encontró la función inicializar_cerebros")

print("\n🔄 Aplicando corrección...")

# La corrección más simple: asegurarnos que los cerebros reciban el manager
correccion_necesaria = False

for i, linea in enumerate(lineas):
    if "cerebro = clase_cerebro(" in linea and "binance_manager=self.binance_manager" not in linea:
        print(f"✅ Encontrada línea a corregir en {i+1}:")
        print(f"   ANTES: {linea}")
        
        # Reemplazar
        if "telegram_bot=self.telegram_bot" in linea:
            # Insertar binance_manager antes de telegram_bot
            nueva_linea = linea.replace(
                "telegram_bot=self.telegram_bot",
                "binance_manager=self.binance_manager, telegram_bot=self.telegram_bot"
            )
        else:
            # Añadir binance_manager
            nueva_linea = linea.replace(
                "cerebro = clase_cerebro(",
                "cerebro = clase_cerebro(binance_manager=self.binance_manager, "
            )
        
        lineas[i] = nueva_linea
        print(f"   DESPUÉS: {nueva_linea}")
        correccion_necesaria = True

if correccion_necesaria:
    # Guardar archivo corregido
    with open(archivo, 'w') as f:
        f.write('\n'.join(lineas))
    print(f"\n✅ {archivo} corregido")
    
    # Probar la corrección
    print("\n🔍 Probando corrección...")
    
    test_correccion = '''
import sys
sys.path.append('.')
import asyncio

async def test_correccion():
    from core.sistema_principal_futures import SistemaPrincipalFutures
    
    sistema = SistemaPrincipalFutures()
    
    # Inicializar binance
    print("1. Inicializando Binance...")
    await sistema.inicializar_binance()
    
    # Inicializar cerebros
    print("2. Inicializando cerebros...")
    await sistema.inicializar_cerebros()
    
    # Verificar
    print("3. Verificando cerebros...")
    if sistema.cerebros:
        cerebro_btc = sistema.cerebros.get('BTCUSDT')
        if cerebro_btc:
            print(f"   • Cerebro BTC creado: ✅")
            print(f"   • Tiene binance_manager: {'✅' if cerebro_btc.binance else '❌'}")
            
            if cerebro_btc.binance:
                print("4. Probando precio...")
                try:
                    precio = await cerebro_btc.obtener_precio_actual()
                    print(f"   • Precio BTC: {precio}")
                    print("🎉 ¡CORRECCIÓN EXITOSA!")
                    return True
                except Exception as e:
                    print(f"   • Error: {e}")
    
    return False

resultado = asyncio.run(test_correccion())
print(f"\\n🎯 Resultado final: {'✅ ÉXITO' if resultado else '❌ FALLO'}")
'''
    
    with open("test_final_correccion.py", "w") as f:
        f.write(test_correccion)
    
    import subprocess
    result = subprocess.run(["python", "test_final_correccion.py"], capture_output=True, text=True)
    print(result.stdout)
    
    if result.stderr:
        print("⚠️  Errores:", result.stderr)
    
    import os
    os.remove("test_final_correccion.py")
    
else:
    print("⚠️  No se encontraron líneas para corregir")
    print("💡 El problema puede ser otro")

print("\n" + "=" * 50)
print("🚀 EJECUTAR SISTEMA FINAL:")
print("python iniciar_sistema_futures.py")
print("\n📋 Si sigue sin funcionar, el problema puede ser:")
print("1. Timing de inicialización")
print("2. Manager no disponible cuando se crean cerebros")
print("3. Necesita reiniciar el sistema completamente")
