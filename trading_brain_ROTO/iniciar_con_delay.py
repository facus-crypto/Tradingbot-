import asyncio
import time
from core.sistema_principal_futures import SistemaPrincipalFutures

async def main():
    sistema = SistemaPrincipalFutures()
    
    print("🚀 INICIANDO CON DELAY PARA TELEGRAM...")
    
    # Iniciar sistema
    await sistema.iniciar()
    
    print("✅ Sistema iniciado - Telegram debería estar estable")
    print("📱 Escribe /status en Telegram")
    
    # Mantener activo
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
