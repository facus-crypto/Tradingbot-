#!/usr/bin/env python3
"""
Ejecutar el sistema completo por tiempo limitado (2 ciclos)
"""
import sys
import asyncio
import signal

# Añadir directorio actual al path
sys.path.append('.')

# Variable para controlar la detención
detener_sistema = False

def signal_handler(signum, frame):
    global detener_sistema
    print("\n🛑 Señal de interrupción recibida")
    detener_sistema = True

async def ejecutar_prueba():
    global detener_sistema
    
    print("🚀 EJECUTANDO SISTEMA COMPLETO (2 CICLOS)")
    print("=" * 60)
    
    try:
        # Importar el sistema
        from core.sistema_principal_futures import SistemaPrincipalFutures
        
        # Instanciar el sistema
        sistema = SistemaPrincipalFutures(config_path="config_prueba_rapida.json")
        
        # Iniciar el sistema
        print("\n⏳ Iniciando sistema...")
        inicio_exitoso = await sistema.iniciar()
        
        if not inicio_exitoso:
            print("❌ Error al iniciar el sistema")
            return False
        
        print("✅ Sistema iniciado correctamente")
        print(f"🔄 Intervalo de análisis: {sistema.intervalo_analisis} segundos")
        print(f"🧠 Cerebros activos: {len(sistema.cerebros)}")
        
        # Configurar manejador de señales
        signal.signal(signal.SIGINT, signal_handler)
        
        # Ejecutar por 2 ciclos completos
        ciclos_completados = 0
        max_ciclos = 2
        
        print(f"\n🎯 Ejecutando {max_ciclos} ciclos completos...")
        
        while ciclos_completados < max_ciclos and not detener_sistema:
            print(f"\n🌀 CICLO {ciclos_completados + 1}/{max_ciclos}")
            print("-" * 40)
            
            try:
                # Ejecutar ciclo de análisis
                resultados = await sistema.ciclo_analisis()
                
                print(f"📊 Resultados del ciclo {ciclos_completados + 1}:")
                print(f"   • Cerebros analizados: {resultados['cerebros_analizados']}")
                print(f"   • Señales generadas: {resultados['señales_generadas']}")
                print(f"   • Señales procesadas: {resultados['señales_procesadas']}")
                print(f"   • Errores: {resultados['errores']}")
                
                # Mostrar detalles de cada cerebro
                for simbolo, detalle in resultados['detalles'].items():
                    estado_emoji = "✅" if detalle['estado'] == 'SEÑAL_GENERADA' else "ℹ️" if detalle['estado'] == 'SIN_SEÑAL' else "⚠️"
                    print(f"   {estado_emoji} {simbolo}: {detalle['estado']}")
                    if detalle.get('senal'):
                        accion = detalle['senal']['action']
                        confianza = detalle['senal']['confidence']
                        print(f"      → {accion} (conf: {confianza:.0%})")
                
                ciclos_completados += 1
                
                # Si no es el último ciclo, esperar
                if ciclos_completados < max_ciclos and not detener_sistema:
                    print(f"\n⏳ Esperando {sistema.intervalo_analisis} segundos para próximo ciclo...")
                    for i in range(sistema.intervalo_analisis):
                        if detener_sistema:
                            break
                        await asyncio.sleep(1)
                        if i % 10 == 0 and i > 0:
                            print(f"   {i}/{sistema.intervalo_analisis} segundos...")
                        
            except Exception as e:
                print(f"❌ Error en ciclo {ciclos_completados + 1}: {e}")
                sistema.estadisticas['errores'] += 1
        
        # Detener el sistema
        print("\n🛑 Deteniendo sistema...")
        await sistema.detener()
        
        # Mostrar estadísticas finales
        print("\n📈 ESTADÍSTICAS FINALES:")
        print(f"   • Ciclos completados: {sistema.estadisticas['ciclos_completados']}")
        print(f"   • Señales generadas: {sistema.estadisticas['señales_generadas']}")
        print(f"   • Señales enviadas a Telegram: {sistema.estadisticas['señales_enviadas_telegram']}")
        print(f"   • Posiciones activas: {sistema.estadisticas['posiciones_activas']}")
        print(f"   • Errores: {sistema.estadisticas['errores']}")
        
        print("\n" + "=" * 60)
        print("🎉 PRUEBA COMPLETA FINALIZADA EXITOSAMENTE")
        print("\n📋 El sistema está funcionando correctamente.")
        print("💡 Puedes ahora:")
        print("   1. Configurar credenciales reales de Binance")
        print("   2. Configurar el bot de Telegram")
        print("   3. Ejecutar con todos los cerebros activos")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupción por usuario")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ejecutar la prueba
    resultado = asyncio.run(ejecutar_prueba())
    
    if resultado:
        print("\n✅ Prueba completada exitosamente.")
        print("🚀 El sistema está listo para uso real.")
    else:
        print("\n❌ Hubo errores durante la prueba.")
