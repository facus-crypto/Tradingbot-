import asyncio
import logging

# Activar logs DETALLADOS
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    print("🔍 INICIANDO CON DEBUG ACTIVADO")
    
    from core.sistema_principal_futures import SistemaPrincipalFutures
    
    sistema = SistemaPrincipalFutures()
    await sistema.iniciar()
    
    # Mantener activo
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
