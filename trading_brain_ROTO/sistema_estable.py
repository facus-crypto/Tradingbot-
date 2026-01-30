import asyncio
import time
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    print("🤖 INICIANDO SISTEMA ESTABLE...")
    
    from core.sistema_principal_futures import SistemaPrincipalFutures
    
    sistema = SistemaPrincipalFutures()
    
    print("1. Inicializando componentes...")
    
    # Inicializar manualmente paso a paso
    await sistema.inicializar_binance()
    print("✅ Binance listo")
    
    await sistema.inicializar_telegram()
    print("✅ Telegram listo")
    
    # Inicializar cerebros
    await sistema._inicializar_cerebros()
    print("✅ 5 cerebros listos")
    
    print("\n🎯 SISTEMA COMPLETAMENTE INICIALIZADO")
    print("📱 Escribe /status en Telegram")
    print("⏳ Ciclo de análisis comenzará en 10 segundos...")
    
    # Esperar que Telegram se estabilice
    await asyncio.sleep(10)
    
    # Iniciar ciclo normal
    print("🔄 Iniciando ciclo continuo...")
    await sistema.iniciar_ciclo_continuo()
    
    # Mantener activo
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
