"""
CEREBRO PRINCIPAL - Coordinador Maestro
Orquesta los 4 cerebros especializados (BTC, ETH, SOL, LINK)
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Agregar el directorio padre al path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración
try:
    from config import MONEDAS, CAPITAL_CONFIG, REGLAS_GLOBALES
    CONFIG_CARGADA = True
except ImportError as e:
    print(f"⚠️  Advertencia: No se pudo cargar config.py: {e}")
    CONFIG_CARGADA = False
    MONEDAS = {}
    CAPITAL_CONFIG = {"max_operaciones_simultaneas": 3}
    REGLAS_GLOBALES = {}

# Agregar carpeta cerebros al path
cerebros_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cerebros')
sys.path.append(cerebros_path)

# Importar cerebros especializados (4 disponibles)
cerebros_cargados = {}
try:
    from cerebro_btc import CerebroBTC
    cerebros_cargados["BTCUSDT"] = CerebroBTC
except ImportError as e:
    print(f"⚠️  No se pudo cargar CerebroBTC: {e}")

try:
    from cerebro_eth import CerebroETH
    cerebros_cargados["ETHUSDT"] = CerebroETH
except ImportError as e:
    print(f"⚠️  No se pudo cargar CerebroETH: {e}")

try:
    from cerebro_sol import CerebroSOL
    cerebros_cargados["SOLUSDT"] = CerebroSOL
except ImportError as e:
    print(f"⚠️  No se pudo cargar CerebroSOL: {e}")

try:
    from cerebro_link import CerebroLINK
    cerebros_cargados["LINKUSDT"] = CerebroLINK
except ImportError as e:
    print(f"⚠️  No se pudo cargar CerebroLINK: {e}")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class SenalTrading:
    """Clase para representar una señal de trading"""
    def __init__(self, senal_dict: Dict):
        self.simbolo = senal_dict.get("simbolo")
        self.direccion = senal_dict.get("direccion", "").upper()
        self.fuerza = senal_dict.get("fuerza", 5)
        self.razones = senal_dict.get("razones", [])
        self.precio_entrada = senal_dict.get("precio_entrada", 0.0)
        self.timestamp = senal_dict.get("timestamp", datetime.now())
        self.data_completa = senal_dict
        self.confirmada = False
        self.ejecutada = False
        
    def __str__(self):
        razones_cortas = ', '.join(self.razones[:2]) if self.razones else 'Sin razones'
        return (f"Señal({self.simbolo} {self.direccion} - Fuerza: {self.fuerza}/10) "
                f"Precio: ${self.precio_entrada:.2f} - {razones_cortas}")

class CerebroPrincipal:
    """Cerebro coordinador maestro con 4 cerebros"""
    
    def __init__(self):
        self.senales_activas: Dict[str, SenalTrading] = {}
        self.operaciones_activas = {}
        self.cerebro_classes = cerebros_cargados
        self.cerebros_especializados = {}
        self.estado = "INICIANDO"
        
        # Estadísticas
        self.senales_generadas = 0
        self.senales_enviadas = 0
        self.operaciones_completadas = 0
        
        logger.info("🧠 CEREBRO PRINCIPAL INICIADO (4 MONEDAS)")
        logger.info(f"📊 Monedas cargadas: {list(self.cerebro_classes.keys())}")
        
    def inicializar_cerebros(self) -> bool:
        """Inicializa todos los cerebros especializados disponibles"""
        logger.info("Inicializando cerebros especializados...")
        
        cerebros_inicializados = 0
        for simbolo, CerebroClass in self.cerebro_classes.items():
            try:
                cerebro_instance = CerebroClass()
                self.cerebros_especializados[simbolo] = cerebro_instance
                estrategia = "N/A"
                if CONFIG_CARGADA and simbolo in MONEDAS:
                    estrategia = MONEDAS[simbolo].get("combinacion", "N/A")
                logger.info(f"  ✅ {simbolo}: {estrategia}")
                cerebros_inicializados += 1
            except Exception as e:
                logger.error(f"  ❌ Error inicializando {simbolo}: {e}")
        
        if cerebros_inicializados == 0:
            logger.error("❌ No se pudo inicializar ningún cerebro")
            return False
        
        logger.info(f"✅ {cerebros_inicializados} cerebros inicializados")
        return True
    
    async def ciclo_analisis(self, ciclos_maximos: int = 3):
        """Ciclo principal de análisis (versión para pruebas)"""
        logger.info("🚀 INICIANDO CICLO DE ANÁLISIS (4 monedas)")
        
        for ciclo in range(1, ciclos_maximos + 1):
            try:
                self.estado = f"ANALIZANDO Ciclo {ciclo}/{ciclos_maximos}"
                logger.info(f"\n{'='*60}")
                logger.info(f"CICLO {ciclo}/{ciclos_maximos}")
                logger.info(f"{'='*60}")
                
                # 1. Ejecutar análisis en cada cerebro
                senales_nuevas = await self.ejecutar_analisis_paralelo()
                
                # 2. Filtrar y mostrar resultados
                if senales_nuevas:
                    senales_filtradas = self.filtrar_senales(senales_nuevas)
                    if senales_filtradas:
                        logger.info(f"\n📢 SEÑALES ENCONTRADAS en ciclo {ciclo}:")
                        for senal in senales_filtradas:
                            logger.info(f"   • {senal}")
                            # Registrar señal
                            self.senales_activas[senal.simbolo] = senal
                            self.senales_generadas += 1
                            logger.info(f"     → Se enviaría a Telegram para confirmación")
                    else:
                        logger.info(f"⚠️  {len(senales_nuevas)} señales encontradas pero filtradas por reglas")
                else:
                    logger.info(f"📭 No se encontraron señales en ciclo {ciclo}")
                
                # 3. Mostrar estado de cada cerebro
                self.mostrar_estado_cerebros()
                
                # 4. Esperar para siguiente ciclo
                if ciclo < ciclos_maximos:
                    logger.info(f"\n⏳ Esperando 10 segundos para próximo ciclo...")
                    await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error en ciclo {ciclo}: {e}")
                await asyncio.sleep(5)
        
        logger.info(f"\n{'='*60}")
        logger.info("PRUEBA COMPLETADA")
        logger.info(f"{'='*60}")
        self.estado = "PRUEBA_COMPLETADA"
    
    async def ejecutar_analisis_paralelo(self) -> List[SenalTrading]:
        """Ejecuta análisis en todas las monedas en paralelo"""
        senales = []
        
        # Crear tareas para análisis paralelo
        tasks = []
        for simbolo, cerebro in self.cerebros_especializados.items():
            task = asyncio.create_task(self.analizar_moneda(simbolo, cerebro))
            tasks.append(task)
        
        # Esperar resultados
        if tasks:
            resultados = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, resultado in enumerate(resultados):
                simbolo = list(self.cerebros_especializados.keys())[i]
                if isinstance(resultado, Exception):
                    logger.error(f"Error analizando {simbolo}: {resultado}")
                elif resultado:
                    senales.append(resultado)
                else:
                    logger.debug(f"{simbolo}: Sin señal")
        
        return senales
    
    async def analizar_moneda(self, simbolo: str, cerebro) -> Optional[SenalTrading]:
        """Analiza una moneda específica y devuelve señal si existe"""
        try:
            # Llamar al método analizar() del cerebro específico
            if hasattr(cerebro, 'analizar'):
                senal_dict = await cerebro.analizar()
                
                if senal_dict and isinstance(senal_dict, dict):
                    # Convertir a objeto SenalTrading
                    senal = SenalTrading(senal_dict)
                    return senal
                
        except Exception as e:
            logger.error(f"Error analizando {simbolo}: {e}")
        
        return None
    
    def filtrar_senales(self, senales: List[SenalTrading]) -> List[SenalTrading]:
        """Filtra señales según reglas globales"""
        senales_filtradas = []
        
        for senal in senales:
            # 1. Fuerza mínima
            if senal.fuerza < 6:
                logger.debug(f"Señal {senal.simbolo} descartada - Fuerza insuficiente: {senal.fuerza}")
                continue
                
            # 2. No duplicar señales activas
            if senal.simbolo in self.senales_activas:
                logger.debug(f"Señal {senal.simbolo} descartada - Ya hay señal activa")
                continue
                
            # 3. Límite de operaciones simultáneas
            if len(self.operaciones_activas) >= CAPITAL_CONFIG["max_operaciones_simultaneas"]:
                logger.debug(f"Señal {senal.simbolo} descartada - Máximo de operaciones alcanzado")
                continue
                
            senales_filtradas.append(senal)
            
        return senales_filtradas
    
    def mostrar_estado_cerebros(self):
        """Muestra estado de cada cerebro especializado"""
        logger.info(f"\n📋 ESTADO DETALLADO DE CEREBROS:")
        
        for simbolo, cerebro in self.cerebros_especializados.items():
            try:
                if hasattr(cerebro, 'get_estado'):
                    estado = cerebro.get_estado()
                    
                    # Icono según si tiene señal
                    icono = "✅" if estado.get("senal_actual") else "⚪"
                    
                    # Información específica por cerebro
                    info_extra = ""
                    if simbolo == "BTCUSDT" and estado.get("estrategia") == "ema_ribbon_rsi":
                        info_extra = "[EMA Ribbon]"
                    elif simbolo == "ETHUSDT" and estado.get("estrategia") == "macd_bollinger":
                        info_extra = "[MACD+Bollinger]"
                    elif simbolo == "SOLUSDT":
                        if estado.get("umbrales_rsi"):
                            info_extra = f"[RSI {estado.get('umbrales_rsi')}]"
                    elif simbolo == "LINKUSDT":
                        info_extra = "[Fibonacci+Ichimoku]"
                    
                    logger.info(f"   {icono} {simbolo} {info_extra}")
                    
                    # Mostrar datos adicionales si hay señal
                    if estado.get("senal_actual"):
                        senal = estado["senal_actual"]
                        logger.info(f"      • Dirección: {senal.get('direccion', 'N/A')}")
                        logger.info(f"      • Fuerza: {senal.get('fuerza', 0)}/10")
                        logger.info(f"      • Precio: ${senal.get('precio_entrada', 0):.2f}")
                        
            except Exception as e:
                logger.info(f"   ⚠️  {simbolo}: Error obteniendo estado ({e})")
    
    async def ejecutar_prueba(self, ciclos: int = 3):
        """Método de prueba simplificado para 4 cerebros"""
        logger.info("🧪 EJECUTANDO PRUEBA DEL SISTEMA (4 cerebros)")
        logger.info("=" * 60)
        
        # 1. Inicializar componentes
        if not self.inicializar_cerebros():
            logger.error("❌ No se pudieron inicializar cerebros. Abortando.")
            return
        
        # 2. Mostrar estado inicial
        logger.info(f"📊 Estado inicial: {len(self.cerebros_especializados)} cerebros activos")
        
        # 3. Ejecutar ciclos de análisis
        self.estado = "PRUEBA_EN_CURSO"
        await self.ciclo_analisis(ciclos)
        
        # 4. Mostrar resumen detallado
        logger.info(f"\n{'📈'*15} RESUMEN FINAL {'📈'*15}")
        logger.info(f"   • Cerebros activos: {len(self.cerebros_especializados)}")
        logger.info(f"   • Señales generadas: {self.senales_generadas}")
        logger.info(f"   • Señales filtradas: {self.senales_generadas - len(self.senales_activas)}")
        logger.info(f"   • Señales activas: {len(self.senales_activas)}")
        logger.info(f"   • Estado final: {self.estado}")
        
        # Mostrar señales encontradas
        if self.senales_activas:
            logger.info(f"\n   📢 SEÑALES ACTIVAS:")
            for simbolo, senal in self.senales_activas.items():
                logger.info(f"      • {simbolo}: {senal.direccion} (Fuerza: {senal.fuerza}/10)")
                logger.info(f"        Precio: ${senal.precio_entrada:.2f}")
                if senal.razones:
                    logger.info(f"        Razón: {senal.razones[0]}")
        
        logger.info(f"\n{'✅'*20} PRUEBA COMPLETADA {'✅'*20}")

# Punto de entrada para pruebas
if __name__ == "__main__":
    cerebro = CerebroPrincipal()
    
    try:
        asyncio.run(cerebro.ejecutar_prueba(ciclos=3))
    except KeyboardInterrupt:
        print("\n🧪 Prueba interrumpida por usuario")
    except Exception as e:
        print(f"\n❌ Error en prueba: {e}")
