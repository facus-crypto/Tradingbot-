"""
CEREBRO ETH - MACD Divergencias + Bollinger Squeeze + OBV
Estrategia institucional para Ethereum (timeframe 4H/1D)
"""
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
import ta

# Configuración
from config import MONEDAS, PARAMETROS_STRATEGY

logger = logging.getLogger(__name__)

class CerebroETH:
    """Cerebro especializado para Ethereum"""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("ETHUSDT", binance_manager, telegram_bot)
        self.simbolo = "ETHUSDT"
        self.config = MONEDAS.get(self.simbolo, {})
        self.parametros = PARAMETROS_STRATEGY.get("macd_bollinger", {})
        
        # Estado interno
        self.ultimo_analisis = None
        self.estado = "INICIADO"
        self.senal_actual = None
        
        logger.info(f"🧠 CEREBRO ETH INICIADO - Estrategia: MACD + Bollinger + OBV")
    
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
    
    def calcular_macd_divergencias(self, df: pd.DataFrame) -> Dict:
        """Calcula MACD y detecta divergencias"""
        if len(df) < 50:
            return {"divergencia_alcista": False, "divergencia_bajista": False, "histograma": 0}
        
        # Parámetros MACD
        fast = self.parametros.get("macd_fast", 12)
        slow = self.parametros.get("macd_slow", 26)
        signal = self.parametros.get("macd_signal", 9)
        
        # Calcular MACD
        macd_indicator = ta.trend.MACD(
            close=df['close'],
            window_slow=slow,
            window_fast=fast,
            window_sign=signal
        )
        
        macd_line = macd_indicator.macd()
        signal_line = macd_indicator.macd_signal()
        histograma = macd_indicator.macd_diff()
        
        # Análisis de divergencias (últimos 30 períodos)
        lookback = 30
        if len(df) < lookback:
            return {
                "divergencia_alcista": False,
                "divergencia_bajista": False,
                "histograma_actual": round(float(histograma.iloc[-1]), 4),
                "macd_line": round(float(macd_line.iloc[-1]), 4),
                "signal_line": round(float(signal_line.iloc[-1]), 4),
                "cruce_alcista": macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2],
                "cruce_bajista": macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]
            }
        
        # Buscar divergencias
        precios_recientes = df['close'].iloc[-lookback:]
        histograma_reciente = histograma.iloc[-lookback:]
        
        # Máximos y mínimos
        max_precio_idx = precios_recientes.idxmax()
        max_precio_val = precios_recientes.max()
        max_hist_idx = histograma_reciente.idxmax()
        max_hist_val = histograma_reciente.max()
        
        min_precio_idx = precios_recientes.idxmin()
        min_precio_val = precios_recientes.min()
        min_hist_idx = histograma_reciente.idxmin()
        min_hist_val = histograma_reciente.min()
        
        # Divergencia bajista: Precio nuevo máximo, histograma no
        divergencia_bajista = (
            max_precio_idx == precios_recientes.index[-1] and
            max_hist_idx != histograma_reciente.index[-1] and
            histograma.iloc[-1] < 0  # Histograma negativo
        )
        
        # Divergencia alcista: Precio nuevo mínimo, histograma no
        divergencia_alcista = (
            min_precio_idx == precios_recientes.index[-1] and
            min_hist_idx != histograma_reciente.index[-1] and
            histograma.iloc[-1] > 0  # Histograma positivo
        )
        
        # Tendencia del histograma
        if len(histograma) >= 5:
            ultimos_5 = histograma.iloc[-5:]
            tendencia_hist = "ALCISTA" if ultimos_5.is_monotonic_increasing else \
                            "BAJISTA" if ultimos_5.is_monotonic_decreasing else "NEUTRAL"
        else:
            tendencia_hist = "NEUTRAL"
        
        return {
            "divergencia_alcista": divergencia_alcista,
            "divergencia_bajista": divergencia_bajista,
            "histograma_actual": round(float(histograma.iloc[-1]), 4),
            "macd_line": round(float(macd_line.iloc[-1]), 4),
            "signal_line": round(float(signal_line.iloc[-1]), 4),
            "cruce_alcista": macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2],
            "cruce_bajista": macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2],
            "tendencia_histograma": tendencia_hist,
            "max_precio": round(float(max_precio_val), 2),
            "min_precio": round(float(min_precio_val), 2)
        }
    
    def calcular_bollinger_squeeze(self, df: pd.DataFrame) -> Dict:
        """Calcula Bandas de Bollinger y detecta squeeze"""
        if len(df) < 50:
            return {"squeeze": False, "ancho_actual": 0, "ancho_promedio": 0}
        
        period = self.parametros.get("bb_period", 20)
        std = self.parametros.get("bb_std", 2)
        
        # Calcular Bandas de Bollinger
        bb = ta.volatility.BollingerBands(
            close=df['close'],
            window=period,
            window_dev=std
        )
        
        banda_superior = bb.bollinger_hband()
        banda_inferior = bb.bollinger_lband()
        banda_media = bb.bollinger_mavg()
        
        # Calcular ancho de bandas (como porcentaje del precio)
        ancho_actual = (banda_superior.iloc[-1] - banda_inferior.iloc[-1]) / banda_media.iloc[-1] * 100
        
        # Ancho promedio de las últimas 50 velas
        if len(df) >= 50:
            ancho_bandas = (banda_superior - banda_inferior) / banda_media * 100
            ancho_promedio = ancho_bandas.iloc[-50:].mean()
        else:
            ancho_promedio = ancho_actual
        
        # Detectar squeeze (umbral ajustable)
        squeeze_ratio = self.parametros.get("squeeze_ratio", 0.7)
        squeeze = ancho_actual < (ancho_promedio * squeeze_ratio)
        
        # Posición del precio dentro de las bandas
        precio_actual = df['close'].iloc[-1]
        posicion_banda = (precio_actual - banda_inferior.iloc[-1]) / (banda_superior.iloc[-1] - banda_inferior.iloc[-1]) * 100
        
        return {
            "squeeze": bool(squeeze),
            "ancho_actual": round(float(ancho_actual), 2),
            "ancho_promedio": round(float(ancho_promedio), 2),
            "ratio_squeeze": round(float(ancho_actual / ancho_promedio if ancho_promedio > 0 else 1), 2),
            "banda_superior": round(float(banda_superior.iloc[-1]), 2),
            "banda_inferior": round(float(banda_inferior.iloc[-1]), 2),
            "banda_media": round(float(banda_media.iloc[-1]), 2),
            "posicion_precio": round(float(posicion_banda), 2),
            "precio_sobre_media": precio_actual > banda_media.iloc[-1]
        }
    
    def calcular_obv(self, df: pd.DataFrame) -> Dict:
        """Calcula On-Balance Volume (OBV)"""
        if len(df) < 20:
            return {"obv_tendencia": "NEUTRAL", "rotura_estructura": False}
        
        # Calcular OBV
        obv_indicator = ta.volume.OnBalanceVolumeIndicator(
            close=df['close'],
            volume=df['volume']
        )
        obv = obv_indicator.on_balance_volume()
        
        # Tendencia OBV (últimos 20 períodos)
        obv_reciente = obv.iloc[-20:]
        
        # Calcular SMA de OBV para tendencia
        obv_sma = obv.rolling(window=20).mean()
        
        # Determinar tendencia
        if obv.iloc[-1] > obv_sma.iloc[-1] and obv_reciente.is_monotonic_increasing:
            tendencia = "ALCISTA"
        elif obv.iloc[-1] < obv_sma.iloc[-1] and obv_reciente.is_monotonic_decreasing:
            tendencia = "BAJISTA"
        else:
            tendencia = "NEUTRAL"
        
        # Detectar rotura de estructura (nuevo máximo/mínimo en OBV)
        if len(obv) >= 30:
            max_obv_previo = obv.iloc[-30:-1].max()
            min_obv_previo = obv.iloc[-30:-1].min()
            
            rotura_alcista = obv.iloc[-1] > max_obv_previo
            rotura_bajista = obv.iloc[-1] < min_obv_previo
            rotura_estructura = rotura_alcista or rotura_bajista
        else:
            rotura_estructura = False
        
        # Divergencia precio-OBV
        precio_tendencia = "ALCISTA" if df['close'].iloc[-1] > df['close'].iloc[-20] else "BAJISTA"
        divergencia_obv = precio_tendencia != tendencia
        
        return {
            "obv_actual": round(float(obv.iloc[-1]), 2),
            "obv_tendencia": tendencia,
            "rotura_estructura": bool(rotura_estructura),
            "divergencia_precio_obv": bool(divergencia_obv),
            "obv_vs_sma": round(float(obv.iloc[-1] - obv_sma.iloc[-1]), 2)
        }
    
    def evaluar_entrada_breakout(self, squeeze_info: Dict, macd_info: Dict, 
                                obv_info: Dict, precio_actual: float) -> Tuple[bool, List[str], str]:
        """Evalúa entrada por breakout después de squeeze"""
        razones = []
        condiciones_cumplidas = 0
        direccion = ""
        
        # 1. Squeeze detectado
        if squeeze_info.get('squeeze'):
            razones.append(f"Bollinger Squeeze ({squeeze_info.get('ratio_squeeze', 0):.2f} ratio)")
            condiciones_cumplidas += 1
        
        # 2. Confirmación OBV
        if obv_info.get('rotura_estructura'):
            razones.append("OBV rompiendo estructura")
            condiciones_cumplidas += 1
        
        if obv_info.get('obv_tendencia') == "ALCISTA":
            razones.append("OBV tendencia alcista")
            condiciones_cumplidas += 1
        
        # 3. MACD confirmando dirección
        if squeeze_info.get('precio_sobre_media') and macd_info.get('cruce_alcista'):
            direccion = "LONG"
            razones.append("MACD cruce alcista + precio sobre banda media")
            condiciones_cumplidas += 2
        elif not squeeze_info.get('precio_sobre_media') and macd_info.get('cruce_bajista'):
            direccion = "SHORT"
            razones.append("MACD cruce bajista + precio bajo banda media")
            condiciones_cumplidas += 2
        
        # 4. Breakout de bandas
        if direccion == "LONG" and precio_actual > squeeze_info.get('banda_superior', precio_actual * 1.1):
            razones.append("Breakout banda superior")
            condiciones_cumplidas += 1
        elif direccion == "SHORT" and precio_actual < squeeze_info.get('banda_inferior', precio_actual * 0.9):
            razones.append("Breakout banda inferior")
            condiciones_cumplidas += 1
        
        # Decisión final
        entrada_breakout = (
            condiciones_cumplidas >= 4 and
            direccion in ["LONG", "SHORT"] and
            squeeze_info.get('squeeze')
        )
        
        return entrada_breakout, razones, direccion
    
    def evaluar_entrada_divergencia(self, macd_info: Dict, squeeze_info: Dict, 
                                   obv_info: Dict, precio_actual: float) -> Tuple[bool, List[str], str]:
        """Evalúa entrada por divergencia MACD"""
        razones = []
        condiciones_cumplidas = 0
        direccion = ""
        
        # 1. Divergencia MACD
        if macd_info.get('divergencia_alcista'):
            direccion = "LONG"
            razones.append("Divergencia alcista MACD")
            condiciones_cumplidas += 2
        
        if macd_info.get('divergencia_bajista'):
            direccion = "SHORT"
            razones.append("Divergencia bajista MACD")
            condiciones_cumplidas += 2
        
        # 2. Confirmación precio
        if direccion == "LONG" and macd_info.get('histograma_actual', 0) > 0:
            razones.append("Histograma MACD positivo")
            condiciones_cumplidas += 1
        elif direccion == "SHORT" and macd_info.get('histograma_actual', 0) < 0:
            razones.append("Histograma MACD negativo")
            condiciones_cumplidas += 1
        
        # 3. Posición en bandas (no extremos)
        posicion = squeeze_info.get('posicion_precio', 50)
        if direccion == "LONG" and posicion < 70:
            razones.append(f"Posición en bandas favorable ({posicion}%)")
            condiciones_cumplidas += 1
        elif direccion == "SHORT" and posicion > 30:
            razones.append(f"Posición en bandas favorable ({posicion}%)")
            condiciones_cumplidas += 1
        
        # 4. OBV confirmando
        if direccion == "LONG" and obv_info.get('obv_tendencia') in ["ALCISTA", "NEUTRAL"]:
            razones.append("OBV no bajista")
            condiciones_cumplidas += 1
        elif direccion == "SHORT" and obv_info.get('obv_tendencia') in ["BAJISTA", "NEUTRAL"]:
            razones.append("OBV no alcista")
            condiciones_cumplidas += 1
        
        # Decisión final
        entrada_divergencia = (
            condiciones_cumplidas >= 4 and
            direccion in ["LONG", "SHORT"] and
            (macd_info.get('divergencia_alcista') or macd_info.get('divergencia_bajista'))
        )
        
        return entrada_divergencia, razones, direccion
    
    async def analizar(self):
        """Método principal de análisis"""
        try:
            logger.info(f"🔍 Analizando {self.simbolo}...")
            
            # 1. Obtener datos
            df_4h = self.obtener_datos_binance(self.config.get("timeframe_analisis", "15m"), 200)
            if df_4h is None or df_4h.empty:
                logger.error(f"No se pudieron obtener datos para {self.simbolo}")
                return None
            
            # 2. Calcular indicadores
            precio_actual = float(df_4h['close'].iloc[-1])
            
            macd_info = self.calcular_macd_divergencias(df_4h)
            squeeze_info = self.calcular_bollinger_squeeze(df_4h)
            obv_info = self.calcular_obv(df_4h)
            
            # 3. Evaluar entradas por breakout
            entrada_breakout, razones_breakout, direccion_breakout = self.evaluar_entrada_breakout(
                squeeze_info, macd_info, obv_info, precio_actual
            )
            
            # 4. Evaluar entradas por divergencia
            entrada_divergencia, razones_divergencia, direccion_divergencia = self.evaluar_entrada_divergencia(
                macd_info, squeeze_info, obv_info, precio_actual
            )
            
            # 5. Generar señal
            if entrada_breakout:
                razones = razones_breakout
                direccion = direccion_breakout
                tipo = "BREAKOUT"
                fuerza_base = 7
            elif entrada_divergencia:
                razones = razones_divergencia
                direccion = direccion_divergencia
                tipo = "DIVERGENCIA"
                fuerza_base = 6
            else:
                # Log detallado
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(f"No hay señal para {self.simbolo}")
                    logger.debug(f"  Precio: ${precio_actual:.2f}")
                    logger.debug(f"  MACD: {macd_info.get('histograma_actual')}")
                    logger.debug(f"  Squeeze: {squeeze_info.get('squeeze')}")
                    logger.debug(f"  OBV: {obv_info.get('obv_tendencia')}")
                
                self.senal_actual = None
                return None
            
            # Calcular fuerza final
            fuerza = min(10, fuerza_base + len(razones))
            
            logger.info(f"✅ SEÑAL {direccion} ({tipo}) detectada para {self.simbolo}")
            logger.info(f"   Razones: {', '.join(razones[:3])}")
            
            # Crear señal
            señal = {
                "simbolo": self.simbolo,
                "direccion": direccion,
                "fuerza": fuerza,
                "razones": razones,
                "precio_entrada": precio_actual,
                "timestamp": datetime.now(),
                "tipo_entrada": tipo,
                "macd_info": macd_info,
                "squeeze_info": squeeze_info,
                "obv_info": obv_info
            }
            
            self.senal_actual = señal
            self.ultimo_analisis = datetime.now()
            return señal
            
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
            "estrategia": self.config.get("combinacion", "macd_bollinger")
        }

# Prueba básica
if __name__ == "__main__":
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    async def prueba():
        cerebro = CerebroETH()
        señal = await cerebro.analizar()
        
        if señal:
            print(f"\n✅ SEÑAL ENCONTRADA:")
            print(f"   Símbolo: {señal['simbolo']}")
            print(f"   Dirección: {señal['direccion']} ({señal['tipo_entrada']})")
            print(f"   Fuerza: {señal['fuerza']}/10")
            print(f"   Precio: ${señal['precio_entrada']:.2f}")
            print(f"   Razones: {', '.join(señal['razones'][:3])}")
        else:
            print(f"\n⚠️ No hay señal para ETH en este momento")
    
    asyncio.run(prueba())
