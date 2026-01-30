#!/usr/bin/env python3
"""
Script simplificado para iniciar el Sistema Principal Futures
"""
import asyncio
import sys
import os

# Añadir directorio actual al path
sys.path.append('.')

async def main():
    print("🚀 Iniciando Sistema de Trading Futures...")
    print("📁 Directorio:", os.getcwd())
    
    try:
        # Importar e instanciar sistema
        from core.sistema_principal_futures import SistemaPrincipalFutures
        
        sistema = SistemaPrincipalFutures(config_path="config_futures.json")
        
        # Iniciar sistema
        print("⏳ Inicializando componentes...")
        exito = await sistema.iniciar()
        
        if exito:
            print("✅ Sistema iniciado correctamente")
            print("🔄 Ciclo de análisis en ejecución")
            print("🛑 Presiona Ctrl+C para detener")
            
            # Mantener el programa ejecutándose
            try:
                while sistema.estado == "EJECUTANDO":
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Detención solicitada por usuario")
                await sistema.detener()
        else:
            print("❌ Error al iniciar el sistema")
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de tener todos los módulos instalados")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ejecutar el sistema
    asyncio.run(main())
