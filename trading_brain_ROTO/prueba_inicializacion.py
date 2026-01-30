#!/usr/bin/env python3
"""
Prueba de inicialización del sistema (solo verifica que todo se carga correctamente)
"""
import sys
import asyncio

# Añadir directorio actual al path
sys.path.append('.')

async def prueba_inicializacion():
    print("🚀 PRUEBA DE INICIALIZACIÓN DEL SISTEMA")
    print("=" * 60)
    
    try:
        # 1. Importar el sistema
        print("1️⃣ Importando módulos...")
        from core.sistema_principal_futures import SistemaPrincipalFutures
        print("   ✅ SistemaPrincipalFutures importado")
        
        # 2. Instanciar el sistema
        print("\n2️⃣ Instanciando sistema...")
        sistema = SistemaPrincipalFutures(config_path="config_prueba_rapida.json")
        print("   ✅ Sistema instanciado")
        
        # 3. Inicializar Binance (simulador)
        print("\n3️⃣ Inicializando Binance...")
        binance_ok = await sistema.inicializar_binance()
        if binance_ok:
            print("   ✅ Binance inicializado (modo simulación)")
            print(f"   💰 Balance simulado: {sistema.binance_manager.balance:.2f} USDT")
        else:
            print("   ❌ Error inicializando Binance")
            return False
        
        # 4. Inicializar cerebros
        print("\n4️⃣ Inicializando cerebros...")
        cerebros_ok = await sistema.inicializar_cerebros()
        if cerebros_ok:
            print(f"   ✅ {len(sistema.cerebros)} cerebro(s) inicializado(s)")
            for simbolo, cerebro in sistema.cerebros.items():
                estado = cerebro.get_estado()
                print(f"      • {simbolo}: {estado['estrategia']}")
        else:
            print("   ❌ Error inicializando cerebros")
            return False
        
        # 5. Probar obtención de datos
        print("\n5️⃣ Probando obtención de datos...")
        for simbolo, cerebro in sistema.cerebros.items():
            try:
                datos = await cerebro.obtener_datos_binance(limit=10)
                if datos:
                    print(f"   ✅ {simbolo}: {len(datos)} datos obtenidos")
                    print(f"      Último precio: {datos[-1]['close']:.2f}")
                else:
                    print(f"   ⚠️  {simbolo}: No se pudieron obtener datos")
            except Exception as e:
                print(f"   ❌ {simbolo}: Error obteniendo datos - {e}")
        
        # 6. Probar análisis simple
        print("\n6️⃣ Probando análisis simple...")
        for simbolo, cerebro in sistema.cerebros.items():
            try:
                resultado = await cerebro.analizar()
                if resultado:
                    print(f"   ✅ {simbolo}: Señal generada - {resultado['action']}")
                    print(f"      Confianza: {resultado['confidence']:.0%}")
                else:
                    print(f"   ℹ️  {simbolo}: Sin señal en este momento")
            except Exception as e:
                print(f"   ❌ {simbolo}: Error en análisis - {e}")
        
        print("\n" + "=" * 60)
        print("🎉 PRUEBA DE INICIALIZACIÓN EXITOSA")
        print("📋 El sistema está listo para ejecutarse")
        print("\n📌 Para ejecutar el sistema completo:")
        print("   python iniciar_sistema_futures.py config_prueba_rapida.json")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ ERROR DE IMPORTACIÓN: {e}")
        print("💡 Verifica que todos los módulos estén en el lugar correcto")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ejecutar la prueba
    resultado = asyncio.run(prueba_inicializacion())
    
    if resultado:
        print("\n✅ La prueba fue exitosa. Puedes continuar con la ejecución completa.")
    else:
        print("\n❌ Hubo errores en la prueba. Debes corregirlos antes de continuar.")
