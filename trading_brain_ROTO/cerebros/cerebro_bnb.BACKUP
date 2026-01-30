#!/usr/bin/env python3
"""
CEREBRO BNB - ADX + Volume Profile + Correlación
Estrategia para Binance Coin (event-driven, timeframe 1D)
"""
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests
import ta
import sys
import os

# Agregar path para importar config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuración - AHORA DEBERÍA FUNCIONAR
try:
    from config import MONEDAS, PARAMETROS_STRATEGY
    CONFIG_CARGADA = True
except ImportError as e:
    print(f"⚠️  No se pudo importar config: {e}")
    CONFIG_CARGADA = False
    # Configuración por defecto
    MONEDAS = {"BNBUSDT": {"combinacion": "adx_volume_profile", "timeframe_analisis": "1h"}}
    PARAMETROS_STRATEGY = {
        "adx_volume_profile": {
            "adx_period": 14,
            "adx_umbral_fuerte": 25,
            "vp_lookback_days": 30,
            "correlacion_umbral": 0.7
        }
    }

logger = logging.getLogger(__name__)

class CerebroBNB:
    """Cerebro especializado para Binance Coin (event-driven)"""
    
def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("BNBUSDT", binance_manager, telegram_bot)
        self.simbolo = "BNBUSDT"
        self.config = MONEDAS.get(self.simbolo, {})
        self.parametros = PARAMETROS_STRATEGY.get("adx_volume_profile", {})
        
        # Estado interno
        self.ultimo_analisis = None
        self.estado = "INICIADO"
        self.senal_actual = None
        
        logger.info(f"🧠 CEREBRO BNB INICIADO - Estrategia: ADX + Volume Profile + Correlación BTC")
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
    
    def calcular_adx(self, df: pd.DataFrame) -> Dict:
        """Calcula ADX (Average Directional Index)"""
        if len(df) < self.adx_period * 2:
            return {"adx": 0, "tendencia_fuerte": False, "+di": 0, "-di": 0}
        
        # Calcular ADX
        adx_indicator = ta.trend.ADXIndicator(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            window=self.adx_period
        )
        
        adx = adx_indicator.adx()
        plus_di = adx_indicator.adx_pos()
        minus_di = adx_indicator.adx_neg()
        
        adx_actual = float(adx.iloc[-1])
        plus_di_actual = float(plus_di.iloc[-1])
        minus_di_actual = float(minus_di.iloc[-1])
        
        # Tendencia según ADX
        tendencia_fuerte = adx_actual > self.adx_umbral_fuerte
        tendencia_direccion = "ALCISTA" if plus_di_actual > minus_di_actual else "BAJISTA"
        
        # Guardar para uso futuro
        self.ultimo_adx = adx_actual
        
        return {
            "adx": round(adx_actual, 2),
            "tendencia_fuerte": tendencia_fuerte,
            "tendencia_direccion": tendencia_direccion,
            "+di": round(plus_di_actual, 2),
            "-di": round(minus_di_actual, 2),
            "cruce_di": plus_di_actual > minus_di_actual,
            "nivel": "FUERTE" if adx_actual > 40 else "MODERADA" if adx_actual > 25 else "DEBIL"
        }
    
    def calcular_volume_profile(self, df: pd.DataFrame, lookback_days: int = 30) -> Dict:
        """Calcula Volume Profile (perfil de volumen)"""
        if len(df) < lookback_days:
            return {"poc": None, "hvns": [], "lvns": [], "valor_justo": None}
        
        # Calcular POC (Point of Control) - precio con mayor volumen
        # Simplificado: agrupar por niveles de precio
        df_reciente = df.iloc[-lookback_days:] if len(df) > lookback_days else df
        
        # Crear bins de precio (20 niveles entre min y max)
        min_precio = df_reciente['low'].min()
        max_precio = df_reciente['high'].max()
        bins = np.linspace(min_precio, max_precio, 20)
        
        # Asignar cada vela a un bin
        df_reciente['price_bin'] = pd.cut(df_reciente['close'], bins=bins)
        
        # Sumar volumen por bin
        volume_by_bin = df_reciente.groupby('price_bin')['volume'].sum()
        
        if volume_by_bin.empty:
            return {"poc": None, "hvns": [], "lvns": [], "valor_justo": None}
        
        # POC es el bin con mayor volumen
        poc_bin = volume_by_bin.idxmax()
        poc_volume = volume_by_bin.max()
        
        # Calcular POC como punto medio del bin
        if hasattr(poc_bin, 'left') and hasattr(poc_bin, 'right'):
            poc_price = (poc_bin.left + poc_bin.right) / 2
        else:
            poc_price = float(df_reciente['close'].mean())
        
        # Identificar HVNs (High Volume Nodes) y LVNs (Low Volume Nodes)
        mean_volume = volume_by_bin.mean()
        std_volume = volume_by_bin.std()
        
        hvns = []
        lvns = []
        
        for bin_range, volume in volume_by_bin.items():
            if hasattr(bin_range, 'left') and hasattr(bin_range, 'right'):
                bin_mid = (bin_range.left + bin_range.right) / 2
                
                if volume > (mean_volume + std_volume):
                    hvns.append({
                        "precio": round(bin_mid, 4),
                        "volumen": round(float(volume), 2),
                        "tipo": "HVN"
                    })
                elif volume < (mean_volume - std_volume):
                    lvns.append({
                        "precio": round(bin_mid, 4),
                        "volumen": round(float(volume), 2),
                        "tipo": "LVN"
                    })
        
        # Valor justo (POC)
        valor_justo = poc_price
        
        return {
            "poc": round(poc_price, 4),
            "poc_volume": round(float(poc_volume), 2),
            "hvns": hvns[:3],  # Top 3 HVNs
            "lvns": lvns[:3],  # Top 3 LVNs
            "valor_justo": round(valor_justo, 4),
            "precio_vs_poc": round(float(df['close'].iloc[-1] - poc_price), 4)
        }
    
    def calcular_correlacion_btc(self, df_bnb: pd.DataFrame, lookback: int = 20) -> Dict:
        """Calcula correlación entre BNB y BTC"""
        try:
            # Obtener datos de BTC para mismo período
            url = "https://api.binance.com/api/v3/klines"
            params_btc = {
                "symbol": "BTCUSDT",
                "interval": "1h",
                "limit": lookback
            }
            
            response = requests.get(url, params=params_btc, timeout=10)
            response.raise_for_status()
            datos_btc = response.json()
            
            # Extraer precios de cierre de BTC
            precios_btc = [float(v[4]) for v in datos_btc]  # índice 4 = close
            
            # Precios de BNB (últimos 'lookback' períodos)
            precios_bnb = df_bnb['close'].iloc[-lookback:].tolist()
            
            # Asegurar misma longitud
            min_len = min(len(precios_btc), len(precios_bnb))
            if min_len < 10:
                return {"correlacion": 0, "desacoplado": False, "muestras": min_len}
            
            precios_btc = precios_btc[:min_len]
            precios_bnb = precios_bnb[:min_len]
            
            # Calcular correlación
            correlacion = np.corrcoef(precios_btc, precios_bnb)[0, 1]
            
            # Determinar si está desacoplado
            desacoplado = abs(correlacion) < self.correlacion_umbral
            
            # Guardar para uso futuro
            self.ultima_correlacion_btc = correlacion
            
            return {
                "correlacion": round(correlacion, 3),
                "desacoplado": desacoplado,
                "muestras": min_len,
                "interpretacion": "ALTA" if abs(correlacion) > 0.8 else 
                                 "MEDIA" if abs(correlacion) > 0.5 else 
                                 "BAJA"
            }
            
        except Exception as e:
            logger.error(f"Error calculando correlación: {e}")
            return {"correlacion": 0, "desacoplado": False, "muestras": 0}
    
    def evaluar_entrada_tendencia_fuerte(self, adx_info: Dict, vp_info: Dict, 
                                       correlacion_info: Dict, precio_actual: float) -> Tuple[bool, List[str], str]:
        """Evalúa entrada en tendencia fuerte (estrategia principal BNB)"""
        razones = []
        condiciones_cumplidas = 0
        direccion = ""
        
        # 1. ADX indica tendencia fuerte
        if adx_info.get("tendencia_fuerte"):
            razones.append(f"ADX {adx_info.get('adx')} > {self.adx_umbral_fuerte} (tendencia fuerte)")
            condiciones_cumplidas += 1
            
            # Determinar dirección según +DI/-DI
            if adx_info.get("cruce_di"):
                direccion = "LONG"
                razones.append(f"+DI ({adx_info.get('+di')}) > -DI ({adx_info.get('-di')})")
            else:
                direccion = "SHORT"
                razones.append(f"-DI ({adx_info.get('-di')}) > +DI ({adx_info.get('+di')})")
            condiciones_cumplidas += 1
        
        # 2. Precio respetando Volume Profile
        if vp_info.get("poc"):
            distancia_poc = abs(precio_actual - vp_info["poc"]) / vp_info["poc"] * 100
            
            if distancia_poc < 5:  # Precio cerca del POC (valor justo)
                razones.append(f"Precio cerca de POC (${vp_info['poc']})")
                condiciones_cumplidas += 1
            
            # Verificar si precio está en HVN (soporte/resistencia)
            for hvn in vp_info.get("hvns", []):
                distancia_hvn = abs(precio_actual - hvn["precio"]) / hvn["precio"] * 100
                if distancia_hvn < 2:
                    razones.append(f"Precio en HVN (${hvn['precio']})")
                    condiciones_cumplidas += 1
                    break
        
        # 3. BNB desacoplado de BTC (movimiento independiente)
        if correlacion_info.get("desacoplado"):
            razones.append(f"BNB desacoplado de BTC (corr: {correlacion_info.get('correlacion'):.3f})")
            condiciones_cumplidas += 1
        
        # 4. Event-driven: Precio reaccionando a noticias de Binance
        # (En producción real, integrar feed de noticias)
        
        # Decisión final
        entrada_tendencia = (
            condiciones_cumplidas >= 3 and
            direccion in ["LONG", "SHORT"] and
            adx_info.get("tendencia_fuerte")
        )
        
        return entrada_tendencia, razones, direccion
    
    async def analizar(self):
        """Método principal de análisis"""
        try:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logger.info(f"🔍 Analizando {self.simbolo}...")
            
            # 1. Obtener datos (1D para BNB)
            df_diario = self.obtener_datos_binance(self.config.get("timeframe_analisis", "1h"), 200)
            if df_diario is None or df_diario.empty:
                logger.error(f"No se pudieron obtener datos para {self.simbolo}")
                return None
            
            # 2. Calcular indicadores
            precio_actual = float(df_diario['close'].iloc[-1])
            
            adx_info = self.calcular_adx(df_diario)
            vp_info = self.calcular_volume_profile(df_diario, self.vp_lookback_days)
            correlacion_info = self.calcular_correlacion_btc(df_diario)
            
            # 3. Evaluar entrada
            entrada_tendencia, razones, direccion = self.evaluar_entrada_tendencia_fuerte(
                adx_info, vp_info, correlacion_info, precio_actual
            )
            
            # 4. Generar señal
            if entrada_tendencia:
                # Calcular fuerza
                fuerza = min(10, 7 + len(razones))  # Base 7 + confirmaciones
                
                logger.info(f"✅ SEÑAL {direccion} detectada para {self.simbolo}")
                logger.info(f"   Razones: {', '.join(razones[:3])}")
                logger.info(f"   ADX: {adx_info.get('adx')} ({adx_info.get('nivel')})")
                logger.info(f"   Correlación BTC: {correlacion_info.get('correlacion'):.3f}")
                
                # Crear señal
                señal = {
                    "simbolo": self.simbolo,
                    "direccion": direccion,
                    "fuerza": fuerza,
                    "razones": razones,
                    "precio_entrada": precio_actual,
                    "timestamp": datetime.now(),
                    "tipo_entrada": "TENDENCIA_FUERTE",
                    "adx_info": adx_info,
                    "vp_info": vp_info,
                    "correlacion_info": correlacion_info
                }
                
                self.senal_actual = señal
                self.ultimo_analisis = datetime.now()
                return señal
            else:
                # Log detallado
                logger.info(f"No hay señal para {self.simbolo}")
                logger.info(f"  Precio: ${precio_actual:.2f}")
                logger.info(f"  ADX: {adx_info.get('adx')} ({adx_info.get('tendencia_fuerte')})")
                logger.info(f"  Correlación BTC: {correlacion_info.get('correlacion'):.3f}")
                
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
            "estrategia": self.config.get("combinacion", "adx_volume_profile"),
            "ultimo_adx": self.ultimo_adx,
            "ultima_correlacion": self.ultima_correlacion_btc
        }

# Prueba básica
if __name__ == "__main__":
    import asyncio
    
    # Configurar logging simple
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    async def prueba():
        print("🧠 Probando Cerebro BNB...")
        cerebro = CerebroBNB()
        señal = await cerebro.analizar()
        
        if señal:
            print(f"\n✅ SEÑAL ENCONTRADA:")
            print(f"   Símbolo: {señal['simbolo']}")
            print(f"   Dirección: {señal['direccion']} ({señal['tipo_entrada']})")
            print(f"   Fuerza: {señal['fuerza']}/10")
            print(f"   Precio: ${señal['precio_entrada']:.2f}")
            print(f"   ADX: {señal['adx_info']['adx']} ({señal['adx_info']['nivel']})")
            print(f"   Correlación BTC: {señal['correlacion_info']['correlacion']:.3f}")
            if señal['razones']:
                print(f"   Razón: {señal['razones'][0]}")
        else:
            print(f"\n⚠️ No hay señal para BNB en este momento")
    
    asyncio.run(prueba())
