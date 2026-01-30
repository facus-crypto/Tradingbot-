"""
CEREBRO LINK - Fibonacci + Ichimoku + Order Flow
Estrategia para Chainlink (swing trading, timeframe 1D)
"""
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
import ta

# Configuración
from config import MONEDAS, PARAMETROS_STRATEGY

logger = logging.getLogger(__name__)

class CerebroLINK:
    """Cerebro especializado para Chainlink (acción de precio limpia)"""
    
def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("LINKUSDT", binance_manager, telegram_bot)
        self.simbolo = "LINKUSDT"
        self.config = MONEDAS.get(self.simbolo, {})
        self.parametros = PARAMETROS_STRATEGY.get("fibonacci_ichimoku", {})
        
        # Estado interno
        self.ultimo_analisis = None
        self.estado = "INICIADO"
        self.senal_actual = None
        
        logger.info(f"🧠 CEREBRO LIN INICIADO - Estrategia: Fibonacci + Ichimoku + Order Flow")
    def obtener_datos_binance(self, intervalo: str, limite: int = 200) -> Optional[pd.DataFrame]:
        """Obtiene datos históricos de Binance"""
        try:
            url = "https://api.binance.com/api/v3/klines"
            params = {
                "symbol": self.simbolo,
                "interval": intervalo,
                "limit": limite
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            datos = response.json()
            
            # Convertir a DataFrame
            columnas = [
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ]
            
            df = pd.DataFrame(datos, columns=columnas)
            
            # Convertir tipos numéricos
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
            
            # Convertir timestamp
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de Binance: {e}")
            return None
    
    def identificar_swings(self, df: pd.DataFrame, lookback: int = 100) -> Dict:
        """Identifica swing highs y swing lows para Fibonacci"""
        if len(df) < lookback:
            return {"swing_high": None, "swing_low": None, "rango_completo": None}
        
        # Encontrar swing high (máximo local)
        high_series = df['high'].iloc[-lookback:]
        swing_high_idx = high_series.idxmax()
        swing_high = high_series.max()
        
        # Encontrar swing low (mínimo local)
        low_series = df['low'].iloc[-lookback:]
        swing_low_idx = low_series.idxmin()
        swing_low = low_series.min()
        
        # Asegurar que swing high viene después de swing low para uptrend
        es_uptrend = swing_high_idx > swing_low_idx
        
        # Guardar para uso futuro
        self.ultimo_swing_high = swing_high
        self.ultimo_swing_low = swing_low
        
        return {
            "swing_high": round(float(swing_high), 4),
            "swing_low": round(float(swing_low), 4),
            "swing_high_date": swing_high_idx,
            "swing_low_date": swing_low_idx,
            "es_uptrend": es_uptrend,
            "rango_absoluto": round(float(swing_high - swing_low), 4),
            "rango_porcentual": round(float((swing_high - swing_low) / swing_low * 100), 2)
        }
    
    def calcular_fibonacci_levels(self, swing_info: Dict) -> Dict:
        """Calcula niveles de Fibonacci retroceso y extensión"""
        if not swing_info.get("swing_high") or not swing_info.get("swing_low"):
            return {}
        
        swing_high = swing_info["swing_high"]
        swing_low = swing_info["swing_low"]
        rango = swing_high - swing_low
        
        # Niveles de retroceso
        retrocesos = {}
        for level in self.fibo_levels:
            precio_nivel = swing_high - (rango * level)
            retrocesos[f"fib_{str(level).replace('.', '_')}"] = round(precio_nivel, 4)
        
        # Niveles de extensión (para take profit)
        extensiones = {
            "ext_1_272": round(swing_low + (rango * 1.272), 4),
            "ext_1_414": round(swing_low + (rango * 1.414), 4),
            "ext_1_618": round(swing_low + (rango * 1.618), 4),
            "ext_2_0": round(swing_low + (rango * 2.0), 4),
            "ext_2_618": round(swing_low + (rango * 2.618), 4)
        }
        
        # Precio actual relativo a niveles Fibonacci
        precio_actual = swing_info.get("precio_actual", swing_high)
        
        # Encontrar nivel Fibonacci más cercano
        niveles = list(retrocesos.values())
        nivel_cercano = min(niveles, key=lambda x: abs(x - precio_actual))
        idx_cercano = niveles.index(nivel_cercano)
        nivel_cercano_pct = self.fibo_levels[idx_cercano] if idx_cercano < len(self.fibo_levels) else 0
        
        return {
            "retrocesos": retrocesos,
            "extensiones": extensiones,
            "nivel_cercano": round(nivel_cercano, 4),
            "nivel_cercano_pct": round(nivel_cercano_pct * 100, 2),
            "distancia_nivel": round(((precio_actual - nivel_cercano) / nivel_cercano * 100), 2),
            "rango_original": round(rango, 4)
        }
    
    def calcular_ichimoku(self, df: pd.DataFrame) -> Dict:
        """Calcula todas las líneas del Ichimoku Cloud"""
        if len(df) < self.senkou:
            return {"cloud_top": None, "cloud_bottom": None, "tendencia": "INSUFICIENTE_DATA"}
        
        # Calcular componentes Ichimoku
        # Tenkan-sen (Conversion Line)
        period_high = df['high'].rolling(window=self.tenkan).max()
        period_low = df['low'].rolling(window=self.tenkan).min()
        tenkan_sen = (period_high + period_low) / 2
        
        # Kijun-sen (Base Line)
        period_high_k = df['high'].rolling(window=self.kijun).max()
        period_low_k = df['low'].rolling(window=self.kijun).min()
        kijun_sen = (period_high_k + period_low_k) / 2
        
        # Senkou Span A (Leading Span A)
        senkou_a = ((tenkan_sen + kijun_sen) / 2).shift(self.kijun)
        
        # Senkou Span B (Leading Span B)
        period_high_s = df['high'].rolling(window=self.senkou).max()
        period_low_s = df['low'].rolling(window=self.senkou).min()
        senkou_b = ((period_high_s + period_low_s) / 2).shift(self.kijun)
        
        # Chikou Span (Lagging Span)
        chikou_span = df['close'].shift(-self.kijun)
        
        # Valores actuales
        tenkan_actual = tenkan_sen.iloc[-1]
        kijun_actual = kijun_sen.iloc[-1]
        senkou_a_actual = senkou_a.iloc[-1]
        senkou_b_actual = senkou_b.iloc[-1]
        chikou_actual = chikou_span.iloc[-self.kijun] if len(chikou_span) >= self.kijun else None
        
        # Nube (Kumo)
        cloud_top = max(senkou_a_actual, senkou_b_actual)
        cloud_bottom = min(senkou_a_actual, senkou_b_actual)
        
        # Tendencia según Ichimoku
        precio_actual = df['close'].iloc[-1]
        
        # 1. Posición respecto a la nube
        sobre_nube = precio_actual > cloud_top
        bajo_nube = precio_actual < cloud_bottom
        en_nube = cloud_bottom <= precio_actual <= cloud_top
        
        # 2. Color de la nube
        nube_alcista = senkou_a_actual > senkou_b_actual
        nube_bajista = senkou_a_actual < senkou_b_actual
        
        # 3. TK Cross
        tk_cross_alcista = tenkan_actual > kijun_actual and tenkan_sen.iloc[-2] <= kijun_sen.iloc[-2]
        tk_cross_bajista = tenkan_actual < kijun_actual and tenkan_sen.iloc[-2] >= kijun_sen.iloc[-2]
        
        # 4. Chikou Span análisis
        chikou_sobre_precio = False
        if chikou_actual is not None:
            precio_pasado = df['close'].iloc[-self.kijun]
            chikou_sobre_precio = chikou_actual > precio_pasado
        
        # Determinar tendencia general
        if sobre_nube and nube_alcista and tk_cross_alcista:
            tendencia = "ALCISTA_FUERTE"
        elif sobre_nube and nube_alcista:
            tendencia = "ALCISTA"
        elif bajo_nube and nube_bajista and tk_cross_bajista:
            tendencia = "BAJISTA_FUERTE"
        elif bajo_nube and nube_bajista:
            tendencia = "BAJISTA"
        elif en_nube:
            tendencia = "NEUTRAL_NUBE"
        else:
            tendencia = "INDETERMINADA"
        
        return {
            "tenkan": round(float(tenkan_actual), 4),
            "kijun": round(float(kijun_actual), 4),
            "senkou_a": round(float(senkou_a_actual), 4),
            "senkou_b": round(float(senkou_b_actual), 4),
            "cloud_top": round(float(cloud_top), 4),
            "cloud_bottom": round(float(cloud_bottom), 4),
            "cloud_width": round(float(cloud_top - cloud_bottom), 4),
            "nube_alcista": nube_alcista,
            "sobre_nube": sobre_nube,
            "bajo_nube": bajo_nube,
            "en_nube": en_nube,
            "tk_cross_alcista": tk_cross_alcista,
            "tk_cross_bajista": tk_cross_bajista,
            "chikou_sobre_precio": chikou_sobre_precio,
            "tendencia": tendencia,
            "precio_vs_tenkan": precio_actual > tenkan_actual,
            "precio_vs_kijun": precio_actual > kijun_actual
        }
    
    def simular_order_flow(self, df: pd.DataFrame) -> Dict:
        """Simula análisis de order flow (en producción usar datos reales)"""
        if len(df) < 20:
            return {"block_buy": False, "block_sell": False, "volume_imbalance": 0}
        
        # Análisis de volumen por precio
        ultimos_20 = df.iloc[-20:]
        
        # Volumen en velas alcistas vs bajistas
        velas_alcistas = ultimos_20[ultimos_20['close'] > ultimos_20['open']]
        velas_bajistas = ultimos_20[ultimos_20['close'] < ultimos_20['open']]
        
        volume_alcista = velas_alcistas['volume'].sum() if not velas_alcistas.empty else 0
        volume_bajista = velas_bajistas['volume'].sum() if not velas_bajistas.empty else 0
        
        total_volume = volume_alcista + volume_bajista
        volume_imbalance = ((volume_alcista - volume_bajista) / total_volume * 100) if total_volume > 0 else 0
        
        # Detectar "bloques grandes" (velas con volumen significativo)
        volume_promedio = ultimos_20['volume'].mean()
        volumen_alto = volume_promedio * 2  # 2x volumen promedio
        
        bloques_compra = velas_alcistas[velas_alcistas['volume'] > volumen_alto]
        bloques_venta = velas_bajistas[velas_bajistas['volume'] > volumen_alto]
        
        block_buy = not bloques_compra.empty
        block_sell = not bloques_venta.empty
        
        # Precio de cierre vs volumen
        if not ultimos_20.empty:
            ultima_vela = ultimos_20.iloc[-1]
            volume_ratio = ultima_vela['volume'] / volume_promedio if volume_promedio > 0 else 1
        else:
            volume_ratio = 1
        
        return {
            "block_buy": block_buy,
            "block_sell": block_sell,
            "volume_imbalance": round(float(volume_imbalance), 2),
            "volume_alcista": round(float(volume_alcista), 2),
            "volume_bajista": round(float(volume_bajista), 2),
            "volume_ratio_actual": round(float(volume_ratio), 2),
            "bloques_compra_count": len(bloques_compra),
            "bloques_venta_count": len(bloques_venta)
        }
    
    def evaluar_entrada_swing(self, fib_info: Dict, ichimoku_info: Dict, 
                             order_flow_info: Dict, precio_actual: float, 
                             swing_info: Dict) -> Tuple[bool, List[str], str]:
        """Evalúa entrada para swing trading"""
        razones = []
        condiciones_cumplidas = 0
        direccion = ""
        
        # ESTRATEGIA 1: Retroceso a Fibonacci + Soporte Ichimoku
        # 1. Precio en nivel Fibonacci clave (0.618 o 0.786)
        nivel_cercano_pct = fib_info.get("nivel_cercano_pct", 0)
        if nivel_cercano_pct in [61.8, 78.6]:  # 0.618 o 0.786
            direccion = "LONG" if swing_info.get("es_uptrend") else "SHORT"
            razones.append(f"Precio en Fib {nivel_cercano_pct}%")
            condiciones_cumplidas += 2
        
        # 2. Confirmación Ichimoku: Precio cerca de Tenkan/Kijun o nube
        if ichimoku_info.get("precio_vs_tenkan") and ichimoku_info.get("precio_vs_kijun"):
            if direccion == "LONG":
                razones.append("Precio sobre Tenkan y Kijun")
                condiciones_cumplidas += 1
        
        if ichimoku_info.get("en_nube") and ichimoku_info.get("nube_alcista"):
            if direccion == "LONG":
                razones.append("Precio en nube alcista")
                condiciones_cumplidas += 1
        
        # 3. Order Flow: Bloques de compra en el nivel
        if order_flow_info.get("block_buy") and order_flow_info.get("volume_imbalance", 0) > 20:
            if direccion == "LONG":
                razones.append("Bloques de compra detectados")
                condiciones_cumplidas += 1
        
        # 4. TK Cross reciente
        if ichimoku_info.get("tk_cross_alcista"):
            if direccion == "LONG":
                razones.append("TK Cross alcista reciente")
                condiciones_cumplidas += 1
        
        # ESTRATEGIA 2: Breakout de nube Ichimoku
        if not direccion:  # Si no hay señal por Fibonacci
            if ichimoku_info.get("tk_cross_alcista") and ichimoku_info.get("sobre_nube"):
                direccion = "LONG"
                razones.append("Breakout nube + TK Cross alcista")
                condiciones_cumplidas += 2
            
            if ichimoku_info.get("tk_cross_bajista") and ichimoku_info.get("bajo_nube"):
                direccion = "SHORT"
                razones.append("Breakout nube + TK Cross bajista")
                condiciones_cumplidas += 2
        
        # Decisión final
        entrada_swing = (
            condiciones_cumplidas >= 3 and
            direccion in ["LONG", "SHORT"]
        )
        
        return entrada_swing, razones, direccion
    
    async def analizar(self):
        """Método principal de análisis"""
        try:
            logger.info(f"🔍 Analizando {self.simbolo}...")
            
            # 1. Obtener datos (1D para LINK)
            df_diario = self.obtener_datos_binance(self.config.get("timeframe_analisis", "4h"), 200)
            if df_diario is None or df_diario.empty:
                logger.error(f"No se pudieron obtener datos para {self.simbolo}")
                return None
            
            # 2. Identificar swings para Fibonacci
            precio_actual = float(df_diario['close'].iloc[-1])
            swing_info = self.identificar_swings(df_diario)
            swing_info["precio_actual"] = precio_actual
            
            # 3. Calcular indicadores
            fib_info = self.calcular_fibonacci_levels(swing_info)
            ichimoku_info = self.calcular_ichimoku(df_diario)
            order_flow_info = self.simular_order_flow(df_diario)
            
            # 4. Evaluar entrada
            entrada_swing, razones, direccion = self.evaluar_entrada_swing(
                fib_info, ichimoku_info, order_flow_info, precio_actual, swing_info
            )
            
            # 5. Generar señal
            if entrada_swing:
                # Calcular fuerza basada en confirmaciones
                fuerza = min(10, 6 + len(razones))  # Base 6 + confirmaciones
                
                logger.info(f"✅ SEÑAL {direccion} (SWING) detectada para {self.simbolo}")
                logger.info(f"   Razones: {', '.join(razones[:3])}")
                logger.info(f"   Nivel Fib: {fib_info.get('nivel_cercano_pct')}%")
                logger.info(f"   Tendencia Ichimoku: {ichimoku_info.get('tendencia')}")
                
                # Crear señal
                señal = {
                    "simbolo": self.simbolo,
                    "direccion": direccion,
                    "fuerza": fuerza,
                    "razones": razones,
                    "precio_entrada": precio_actual,
                    "timestamp": datetime.now(),
                    "tipo_entrada": "SWING",
                    "fib_info": fib_info,
                    "ichimoku_info": ichimoku_info,
                    "order_flow_info": order_flow_info,
                    "swing_info": swing_info
                }
                
                self.senal_actual = señal
                self.ultimo_analisis = datetime.now()
                return señal
            else:
                # Log detallado
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"No hay señal para {self.simbolo}")
                    logger.debug(f"  Precio: ${precio_actual:.2f}")
                    logger.debug(f"  Nivel Fib más cercano: {fib_info.get('nivel_cercano_pct', 0)}%")
                    logger.debug(f"  Tendencia Ichimoku: {ichimoku_info.get('tendencia')}")
                    logger.debug(f"  Imbalance volumen: {order_flow_info.get('volume_imbalance')}%")
                
                self.senal_actual = None
                return None
            
        except Exception as e:
            logger.error(f"Error en análisis de {self.simbolo}: {e}", exc_info=True)
            return None
    
    def get_estado(self) -> Dict:
        """Devuelve estado actual del cerebro"""
        return {
            "simbolo": self.simbolo,
            "estado": self.estado,
            "ultimo_analisis": self.ultimo_analisis,
            "senal_actual": self.senal_actual,
            "estrategia": self.config.get("combinacion", "fibonacci_ichimoku"),
            "swing_high": self.ultimo_swing_high,
            "swing_low": self.ultimo_swing_low
        }

# Prueba básica
if __name__ == "__main__":
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    async def prueba():
        cerebro = CerebroLINK()
        señal = await cerebro.analizar()
        
        if señal:
            print(f"\n✅ SEÑAL ENCONTRADA:")
            print(f"   Símbolo: {señal['simbolo']}")
            print(f"   Dirección: {señal['direccion']} ({señal['tipo_entrada']})")
            print(f"   Fuerza: {señal['fuerza']}/10")
            print(f"   Precio: ${señal['precio_entrada']:.2f}")
            print(f"   Nivel Fib: {señal['fib_info'].get('nivel_cercano_pct')}%")
            print(f"   Razones: {', '.join(señal['razones'][:3])}")
        else:
            print(f"\n⚠️ No hay señal para LINK en este momento")
    
    asyncio.run(prueba())
