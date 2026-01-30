import logging
import asyncio
from typing import List, Dict
import sys
import os

# Añadir ruta
sys.path.append('.')

# Importar configuración
try:
    import config
    CONFIG_CARGADA = True
    MONEDAS = config.MONEDAS
except ImportError:
    CONFIG_CARGADA = False
    MONEDAS = {}
    print("⚠️ No se pudo cargar config.py")

# Diccionario global para cerebros cargados
cerebros_cargados = {}

# CEREBRO BTC
try:
    from cerebros.cerebro_btc import CerebroBTC
    cerebros_cargados["BTCUSDT"] = CerebroBTC
    print("✅ BTCUSDT cargado")
except ImportError as e:
    print(f"⚠️ No CerebroBTC: {e}")

# CEREBRO ETH
try:
    from cerebros.cerebro_eth import CerebroETH
    cerebros_cargados["ETHUSDT"] = CerebroETH
    print("✅ ETHUSDT cargado")
except ImportError as e:
    print(f"⚠️ No CerebroETH: {e}")

# CEREBRO SOL
try:
    from cerebros.cerebro_sol import CerebroSOL
    cerebros_cargados["SOLUSDT"] = CerebroSOL
    print("✅ SOLUSDT cargado")
except ImportError as e:
    print(f"⚠️ No CerebroSOL: {e}")

# CEREBRO LINK
try:
    from cerebros.cerebro_link import CerebroLINK
    cerebros_cargados["LINKUSDT"] = CerebroLINK
    print("✅ LINKUSDT cargado")
except ImportError as e:
    print(f"⚠️ No CerebroLINK: {e}")

# CEREBRO BNB
try:
    from cerebros.cerebro_bnb import CerebroBNB
    cerebros_cargados["BNBUSDT"] = CerebroBNB
    print("✅ BNBUSDT cargado")
except ImportError as e:
    print(f"⚠️ No CerebroBNB: {e}")

print(f"\n📊 cerebros_cargados tiene {len(cerebros_cargados)} elementos: {list(cerebros_cargados.keys())}")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class SistemaCompleto:
    """Sistema completo de trading integrado"""

    def __init__(self, usar_telegram=True):
        self.cerebros_especializados = {}
        self.interfaz_telegram = None
        self.senales_enviadas = 0
        self.senales_confirmadas = 0
        self.estado = "INICIANDO"
        
        # Inicializar cerebros
        self.inicializar_cerebros()
        
        logger.info(f"🚀 SISTEMA COMPLETO INICIADO ({len(self.cerebros_especializados)} cerebros)")

    def inicializar_cerebros(self):
        """Inicializa todos los cerebros especializados"""
        logger.info("Inicializando cerebros...")
        
        print(f"DEBUG: cerebros_cargados tiene {len(cerebros_cargados)} elementos: {list(cerebros_cargados.keys())}")
        
        for simbolo, CerebroClass in cerebros_cargados.items():
            print(f"  Procesando {simbolo}...")
            try:
                cerebro = CerebroClass()
                self.cerebros_especializados[simbolo] = cerebro

                # Obtener nombre de estrategia
                estrategia = "N/A"
                if CONFIG_CARGADA and simbolo in MONEDAS:
                    estrategia = MONEDAS[simbolo].get("combinacion", "N/A")

                logger.info(f"  ✅ {simbolo}: {estrategia}")
                
            except Exception as e:
                logger.error(f"  ❌ Error {simbolo}: {e}")

# Para probar directamente
if __name__ == "__main__":
    sistema = SistemaCompleto(usar_telegram=False)
    print(f"\n🎯 Sistema creado con {len(sistema.cerebros_especializados)} cerebros")
    print("Lista completa:")
    for s in sorted(sistema.cerebros_especializados.keys()):
        print(f"  • {s}")
