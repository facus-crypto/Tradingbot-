"""
Cerebro BNB actualizado para Binance Futures
Estrategia: ADX + Volume Profile + Correlación BTC
"""
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.append('.')

try:
    from cerebros.cerebro_base_futures import CerebroFuturesBase
    BASE_IMPORTED = True
except ImportError:
    BASE_IMPORTED = False
    print("❌ No se pudo importar CerebroFuturesBase")

logger = logging.getLogger(__name__)

class CerebroBNB(CerebroFuturesBase):
    """Cerebro para BNBUSDT con estrategia ADX + Volume Profile + Correlación BTC"""
    
    def __init__(self, binance_manager=None, telegram_bot=None, btc_cerebro=None):
        """Inicializa cerebro BNB con referencia opcional a cerebro BTC"""
        if not BASE_IMPORTED:
            raise ImportError("No se pudo importar la clase base")
            
        super().__init__(
            symbol="BNBUSDT",
            binance_manager=binance_manager,
            telegram_bot=telegram_bot
        )
        
        # Configuración específica de BNB
        self.estrategia = "adx_volume_profile_correlation"
        self.timeframe = "1h"  # BNB responde mejor a timeframes mayores
        self.min_confidence = 0.73  # 73% confianza mínima para BNB
        
        # Referencia al cerebro BTC para correlación
        self.btc_cerebro = btc_cerebro
        
        # Parámetros de la estrategia
        self.adx_period = 14
        self.adx_threshold = 25  # Umbral para tendencia fuerte
        
        self.volume_profile_bins = 20
        self.vp_value_area_percent = 0.70  # 70% del volumen concentrado
        
        self.correlation_period = 24  # Horas para calcular correlación
        
        # Umbrales de correlación
        self.correlation_threshold_high = 0.7
        self.correlation_threshold_low = 0.3
        
        logger.info(f"🧠 Cerebro BNB inicializado - {self.estrategia}")
    
    def calcular_adx(self, datos: List[Dict]) -> Dict[str, List[float]]:
        """Calcula ADX, +DI y -DI"""
        if len(datos) < self.adx_period + 1:
            return {'adx': [], 'plus_di': [], 'minus_di': []}
        
        highs = [d['high'] for d in datos]
        lows = [d['low'] for d in datos]
        closes = [d['close'] for d in datos]
        
        # Calcular True Range
        tr = []
        for i in range(1, len(datos)):
            hl = highs[i] - lows[i]
            hc = abs(highs[i] - closes[i-1])
            lc = abs(lows[i] - closes[i-1])
            tr.append(max(hl, hc, lc))
        
        # Calcular Directional Movement
        plus_dm = []
        minus_dm = []
        
        for i in range(1, len(highs)):
            up_move = highs[i] - highs[i-1]
            down_move = lows[i-1] - lows[i]
            
            if up_move > down_move and up_move > 0:
                plus_dm.append(up_move)
            else:
                plus_dm.append(0)
            
            if down_move > up_move and down_move > 0:
                minus_dm.append(down_move)
            else:
                minus_dm.append(0)
        
        # Suavizar TR, +DM y -DM
        tr_smoothed = [sum(tr[:self.adx_period]) / self.adx_period]
        plus_dm_smoothed = [sum(plus_dm[:self.adx_period]) / self.adx_period]
        minus_dm_smoothed = [sum(minus_dm[:self.adx_period]) / self.adx_period]
        
        for i in range(self.adx_period, len(tr)):
            tr_smoothed.append((tr_smoothed[-1] * (self.adx_period - 1) + tr[i]) / self.adx_period)
            plus_dm_smoothed.append((plus_dm_smoothed[-1] * (self.adx_period - 1) + plus_dm[i]) / self.adx_period)
            minus_dm_smoothed.append((minus_dm_smoothed[-1] * (self.adx_period - 1) + minus_dm[i]) / self.adx_period)
        
        # Calcular +DI y -DI
        plus_di = []
        minus_di = []
        
        for i in range(len(tr_smoothed)):
            if tr_smoothed[i] > 0:
                plus_di.append(100 * plus_dm_smoothed[i] / tr_smoothed[i])
                minus_di.append(100 * minus_dm_smoothed[i] / tr_smoothed[i])
            else:
                plus_di.append(0)
                minus_di.append(0)
        
        # Calcular DX y ADX
        dx = []
        for i in range(len(plus_di)):
            di_sum = plus_di[i] + minus_di[i]
            if di_sum > 0:
                dx.append(100 * abs(plus_di[i] - minus_di[i]) / di_sum)
            else:
                dx.append(0)
        
        adx = [sum(dx[:self.adx_period]) / self.adx_period]
        for i in range(self.adx_period, len(dx)):
            adx.append((adx[-1] * (self.adx_period - 1) + dx[i]) / self.adx_period)
        
        # Añadir NaN al inicio para igualar longitud
        nan_padding = [np.nan] * (self.adx_period)
        adx = nan_padding + adx
        plus_di = nan_padding + plus_di
        minus_di = nan_padding + minus_di
        
        return {
            'adx': adx,
            'plus_di': plus_di,
            'minus_di': minus_di
        }
    
    def calcular_volume_profile(self, datos: List[Dict]) -> Dict:
        """Calcula Volume Profile y Value Area"""
        if len(datos) < 20:
            return {
                'poc': 0, 'value_area_high': 0, 'value_area_low': 0,
                'profile': {}, 'total_volume': 0
            }
        
        # Extraer precios y volúmenes
        highs = [d['high'] for d in datos]
        lows = [d['low'] for d in datos]
        volumes = [d['volume'] for d in datos if 'volume' in d]
        
        if len(volumes) != len(highs):
            volumes = [1] * len(highs)  # Volumen dummy si no hay datos
        
        # Determinar rango de precios
        min_price = min(lows)
        max_price = max(highs)
        
        if min_price == max_price:
            return {
                'poc': min_price,
                'value_area_high': min_price,
                'value_area_low': min_price,
                'profile': {min_price: sum(volumes)},
                'total_volume': sum(volumes)
            }
        
        # Crear bins para el perfil
        price_range = max_price - min_price
        bin_size = price_range / self.volume_profile_bins
        
        profile = {}
        for i in range(len(datos)):
            # Distribuir volumen proporcionalmente entre high y low
            candle_range = highs[i] - lows[i]
            if candle_range > 0:
                # Para simplificar, asignar todo el volumen al precio medio
                avg_price = (highs[i] + lows[i]) / 2
                bin_key = round(min_price + round((avg_price - min_price) / bin_size) * bin_size, 4)
                profile[bin_key] = profile.get(bin_key, 0) + volumes[i]
            else:
                # Si no hay rango, usar close
                close_price = datos[i]['close']
                bin_key = round(min_price + round((close_price - min_price) / bin_size) * bin_size, 4)
                profile[bin_key] = profile.get(bin_key, 0) + volumes[i]
        
        # Encontrar POC (Point of Control)
        if profile:
            poc_price = max(profile, key=profile.get)
            total_volume = sum(profile.values())
            
            # Calcular Value Area (70% del volumen alrededor del POC)
            sorted_prices = sorted(profile.items(), key=lambda x: x[1], reverse=True)
            
            value_volume = 0
            value_area_prices = []
            
            for price, volume in sorted_prices:
                if value_volume < total_volume * self.vp_value_area_percent:
                    value_volume += volume
                    value_area_prices.append(price)
                else:
                    break
            
            if value_area_prices:
                value_area_low = min(value_area_prices)
                value_area_high = max(value_area_prices)
            else:
                value_area_low = poc_price
                value_area_high = poc_price
            
            return {
                'poc': poc_price,
                'value_area_high': value_area_high,
                'value_area_low': value_area_low,
                'profile': profile,
                'total_volume': total_volume,
                'price_vs_poc': datos[-1]['close'] - poc_price,
                'price_vs_value_area': 'inside' if value_area_low <= datos[-1]['close'] <= value_area_high else 'outside'
            }
        else:
            return {
                'poc': datos[-1]['close'],
                'value_area_high': datos[-1]['close'],
                'value_area_low': datos[-1]['close'],
                'profile': {},
                'total_volume': 0
            }
    
    def calcular_correlacion_btc(self, datos_bnb: List[Dict], datos_btc: Optional[List[Dict]] = None) -> Dict:
        """Calcula correlación entre BNB y BTC"""
        if not datos_btc or len(datos_bnb) != len(datos_btc):
            # Si no hay datos de BTC, devolver valores por defecto
            return {
                'correlation': 0,
                'correlation_strength': 'none',
                'lag': 0,
                'bnb_returns': [],
                'btc_returns': []
            }
        
        # Tomar últimos N periodos para correlación
        lookback = min(len(datos_bnb), len(datos_btc), self.correlation_period)
        
        if lookback < 10:
            return {
                'correlation': 0,
                'correlation_strength': 'insufficient_data',
                'lag': 0,
                'bnb_returns': [],
                'btc_returns': []
            }
        
        # Extraer precios de cierre
        bnb_closes = [d['close'] for d in datos_bnb[-lookback:]]
        btc_closes = [d['close'] for d in datos_btc[-lookback:]]
        
        # Calcular retornos logarítmicos
        bnb_returns = []
        btc_returns = []
        
        for i in range(1, lookback):
            if bnb_closes[i-1] > 0 and btc_closes[i-1] > 0:
                bnb_returns.append(np.log(bnb_closes[i] / bnb_closes[i-1]))
                btc_returns.append(np.log(btc_closes[i] / btc_closes[i-1]))
        
        if len(bnb_returns) < 5 or len(btc_returns) < 5:
            return {
                'correlation': 0,
                'correlation_strength': 'insufficient_data',
                'lag': 0,
                'bnb_returns': bnb_returns,
                'btc_returns': btc_returns
            }
        
        # Calcular correlación de Pearson
        correlation = np.corrcoef(bnb_returns, btc_returns)[0, 1]
        
        # Determinar fuerza de la correlación
        correlation_strength = 'none'
        if abs(correlation) > self.correlation_threshold_high:
            correlation_strength = 'strong'
        elif abs(correlation) > self.correlation_threshold_low:
            correlation_strength = 'moderate'
        else:
            correlation_strength = 'weak'
        
        # Determinar signo
        correlation_type = 'positive' if correlation > 0 else 'negative'
        
        return {
            'correlation': correlation,
            'correlation_strength': correlation_strength,
            'correlation_type': correlation_type,
            'bnb_returns': bnb_returns,
            'btc_returns': btc_returns
        }
    
    def analizar_adx_senal(self, adx_data: Dict) -> Dict:
        """Analiza señales del ADX"""
        if len(adx_data['adx']) < 2 or len(adx_data['plus_di']) < 2 or len(adx_data['minus_di']) < 2:
            return {
                'trend_strength': 'none',
                'trend_direction': 'neutral',
                'adx_value': 0,
                'di_crossover': 'none'
            }
        
        adx_current = adx_data['adx'][-1]
        plus_di_current = adx_data['plus_di'][-1]
        minus_di_current = adx_data['minus_di'][-1]
        
        plus_di_prev = adx_data['plus_di'][-2]
        minus_di_prev = adx_data['minus_di'][-2]
        
        # Fuerza de la tendencia
        trend_strength = 'none'
        if not np.isnan(adx_current):
            if adx_current > self.adx_threshold:
                trend_strength = 'strong'
            elif adx_current > self.adx_threshold * 0.7:
                trend_strength = 'moderate'
            else:
                trend_strength = 'weak'
        
        # Dirección de la tendencia
        trend_direction = 'neutral'
        if not np.isnan(plus_di_current) and not np.isnan(minus_di_current):
            if plus_di_current > minus_di_current:
                trend_direction = 'bullish'
            else:
                trend_direction = 'bearish'
        
        # Crossover DI
        di_crossover = 'none'
        if (not np.isnan(plus_di_prev) and not np.isnan(minus_di_prev) and
            not np.isnan(plus_di_current) and not np.isnan(minus_di_current)):
            
            if plus_di_prev < minus_di_prev and plus_di_current > minus_di_current:
                di_crossover = 'bullish'
            elif plus_di_prev > minus_di_prev and plus_di_current < minus_di_current:
                di_crossover = 'bearish'
        
        return {
            'trend_strength': trend_strength,
            'trend_direction': trend_direction,
            'adx_value': adx_current if not np.isnan(adx_current) else 0,
            'di_crossover': di_crossover,
            'plus_di': plus_di_current if not np.isnan(plus_di_current) else 0,
            'minus_di': minus_di_current if not np.isnan(minus_di_current) else 0
        }
    
    async def generar_senal(self, datos: List[Dict], precio_actual: float) -> Optional[Dict]:
        """
        Implementación específica de la estrategia ADX + Volume Profile + Correlación BTC
        
        Args:
            datos: Datos OHLCV de BNB
            precio_actual: Precio actual de BNB
            
        Returns:
            Señal generada o None
        """
        try:
            if len(datos) < 100:
                logger.warning(f"BNB - Datos insuficientes")
                return None
            
            # 1. Calcular ADX
            adx_data = self.calcular_adx(datos)
            
            # 2. Calcular Volume Profile
            volume_profile = self.calcular_volume_profile(datos[-100:])  # Últimas 100 velas
            
            # 3. Obtener datos de BTC si está disponible el cerebro
            btc_data = None
            if self.btc_cerebro:
                btc_data = await self.btc_cerebro.obtener_datos_binance(limit=100)
            
            # 4. Calcular correlación con BTC
            correlation = self.calcular_correlacion_btc(datos, btc_data)
            
            # 5. Analizar ADX
            adx_senal = self.analizar_adx_senal(adx_data)
            
            # 6. Tomar decisión basada en múltiples factores
            razones = []
            indicadores = {
                'adx_trend_strength': adx_senal['trend_strength'],
                'adx_trend_direction': adx_senal['trend_direction'],
                'adx_di_crossover': adx_senal['di_crossover'],
                'adx_value': adx_senal['adx_value'],
                'volume_profile_poc': volume_profile['poc'],
                'volume_profile_position': volume_profile['price_vs_value_area'],
                'correlation_strength': correlation['correlation_strength'],
                'correlation_type': correlation['correlation_type'],
                'correlation': correlation['correlation']
            }
            
            confianza_base = 0.0
            señales_alcistas = 0
            señales_bajistas = 0
            
            # SEÑAL ALCISTA FUERTE: ADX fuerte + DI crossover alcista + Precio en Value Area baja + Alta correlación positiva
            if (adx_senal['trend_strength'] == 'strong' and
                adx_senal['di_crossover'] == 'bullish' and
                volume_profile['price_vs_value_area'] == 'inside' and
                precio_actual < volume_profile['poc'] and  # Precio bajo POC
                correlation['correlation_strength'] == 'strong' and
                correlation['correlation_type'] == 'positive'):
                
                razones.append(f"ADX fuerte ({adx_senal['adx_value']:.1f}) con tendencia alcista")
                razones.append("Crossover DI alcista confirmado")
                razones.append("Precio en zona de valor (Value Area) por debajo del POC")
                razones.append(f"Alta correlación positiva con BTC ({correlation['correlation']:.2f})")
                confianza_base = 0.88
                señales_alcistas = 4
            
            # SEÑAL BAJISTA FUERTE: ADX fuerte + DI crossover bajista + Precio en Value Area alta + Alta correlación positiva
            elif (adx_senal['trend_strength'] == 'strong' and
                  adx_senal['di_crossover'] == 'bearish' and
                  volume_profile['price_vs_value_area'] == 'inside' and
                  precio_actual > volume_profile['poc'] and  # Precio sobre POC
                  correlation['correlation_strength'] == 'strong' and
                  correlation['correlation_type'] == 'positive'):
                
                razones.append(f"ADX fuerte ({adx_senal['adx_value']:.1f}) con tendencia bajista")
                razones.append("Crossover DI bajista confirmado")
                razones.append("Precio en zona de valor (Value Area) por encima del POC")
                razones.append(f"Alta correlación positiva con BTC ({correlation['correlation']:.2f})")
                confianza_base = 0.88
                señales_bajistas = 4
            
            # SEÑAL ALCISTA MODERADA: ADX moderado + Tendencia alcista + Precio fuera de Value Area (sobreventa)
            elif (adx_senal['trend_strength'] in ['moderate', 'strong'] and
                  adx_senal['trend_direction'] == 'bullish' and
                  volume_profile['price_vs_value_area'] == 'outside' and
                  precio_actual < volume_profile['value_area_low']):  # Precio bajo Value Area
                
                razones.append(f"ADX {adx_senal['trend_strength']} con dirección alcista")
                razones.append("Precio fuera de Value Area (sobreventa)")
                if correlation['correlation_strength'] != 'none':
                    razones.append(f"Correlación {correlation['correlation_type']} con BTC")
                    confianza_base = 0.75
                else:
                    confianza_base = 0.68
                señales_alcistas = 3
            
            # SEÑAL BAJISTA MODERADA: ADX moderado + Tendencia bajista + Precio fuera de Value Area (sobrecompra)
            elif (adx_senal['trend_strength'] in ['moderate', 'strong'] and
                  adx_senal['trend_direction'] == 'bearish' and
                  volume_profile['price_vs_value_area'] == 'outside' and
                  precio_actual > volume_profile['value_area_high']):  # Precio sobre Value Area
                
                razones.append(f"ADX {adx_senal['trend_strength']} con dirección bajista")
                razones.append("Precio fuera de Value Area (sobrecompra)")
                if correlation['correlation_strength'] != 'none':
                    razones.append(f"Correlación {correlation['correlation_type']} con BTC")
                    confianza_base = 0.75
                else:
                    confianza_base = 0.68
                señales_bajistas = 3
            
            # SEÑAL DÉBIL: Solo ADX o solo correlación
            elif (adx_senal['di_crossover'] == 'bullish' and
                  correlation['correlation_strength'] == 'strong'):
                
                razones.append("Crossover DI alcista")
                razones.append(f"Correlación fuerte con BTC ({correlation['correlation']:.2f})")
                confianza_base = 0.65
                señales_alcistas = 2
            
            elif (adx_senal['di_crossover'] == 'bearish' and
                  correlation['correlation_strength'] == 'strong'):
                
                razones.append("Crossover DI bajista")
                razones.append(f"Correlación fuerte con BTC ({correlation['correlation']:.2f})")
                confianza_base = 0.65
                señales_bajistas = 2
            
            # Determinar dirección final
            if señales_alcistas > señales_bajistas and confianza_base >= self.min_confidence:
            # Calcular trailing stop
            sl, tp, fase = self.calcular_trailing_directo(precio_actual, precio_actual)
                return {
                    'action': 'LONG',
                    'confidence': confianza_base,
                    'entry_price': precio_actual,
                    'razones': razones,
                    'indicadores': indicadores
                ,
            'stop_loss': sl,
            'take_profit': tp,
            'fase_trailing': fase
        }
            
            elif señales_bajistas > señales_alcistas and confianza_base >= self.min_confidence:
            # Calcular trailing stop
            sl, tp, fase = self.calcular_trailing_directo(precio_actual, precio_actual)
                return {
                    'action': 'SHORT',
                    'confidence': confianza_base,
                    'entry_price': precio_actual,
                    'razones': razones,
                    'indicadores': indicadores
                ,
            'stop_loss': sl,
            'take_profit': tp,
            'fase_trailing': fase
        }
            
            # Sin señal clara
            logger.debug(f"BNB - Sin señal clara. "
                        f"ADX: {adx_senal['adx_value']:.1f} ({adx_senal['trend_strength']}), "
                        f"DI Cross: {adx_senal['di_crossover']}, "
                        f"VP Pos: {volume_profile['price_vs_value_area']}, "
                        f"Corr: {correlation['correlation']:.2f}")
            
            return None
            
        except Exception as e:
            logger.error(f"BNB - Error en generación de señal: {e}")
            return None
    
    def set_btc_cerebro(self, btc_cerebro):
        """Establece referencia al cerebro BTC para correlación"""
        self.btc_cerebro = btc_cerebro
        logger.info(f"BNB - Cerebro BTC configurado para correlación")
    
    def get_info_estrategia(self) -> Dict:
        """Devuelve información detallada de la estrategia"""
        return {
            'nombre': 'ADX + Volume Profile + Correlación BTC',
            'descripcion': 'Combina fuerza de tendencia (ADX), perfiles de volumen y correlación con BTC',
            'parametros': {
                'adx_period': self.adx_period,
                'adx_threshold': self.adx_threshold,
                'volume_profile_bins': self.volume_profile_bins,
                'vp_value_area_percent': self.vp_value_area_percent,
                'correlation_period': self.correlation_period,
                'correlation_threshold_high': self.correlation_threshold_high,
                'correlation_threshold_low': self.correlation_threshold_low,
                'timeframe': self.timeframe,
                'min_confidence': self.min_confidence
            },
            'reglas': [
                'Señal fuerte: ADX fuerte + DI crossover + Price en Value Area + Alta correlación BTC',
                'Señal moderada: ADX moderado + tendencia clara + Price fuera Value Area',
                'Señal débil: Solo DI crossover o alta correlación sin confirmación ADX'
            ]
        }

if __name__ == "__main__":
    # Prueba del cerebro BNB
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    print("🧠 PRUEBA CEREBRO BNB FUTURES")
    print("=" * 50)
    
    async def prueba_cerebro_bnb():
        cerebro = CerebroBNB()
        
        print(f"✅ Cerebro BNB creado")
        print(f"   Símbolo: {cerebro.symbol}")
        print(f"   Estrategia: {cerebro.estrategia}")
        
        info = cerebro.get_info_estrategia()
        print(f"\n📊 Información de estrategia:")
        print(f"   Nombre: {info['nombre']}")
        print(f"   Descripción: {info['descripcion']}")
        print(f"   Timeframe: {info['parametros']['timeframe']}")
        
        print(f"\n⚙️  Parámetros ADX:")
        print(f"   Period: {info['parametros']['adx_period']}")
        print(f"   Threshold: {info['parametros']['adx_threshold']}")
        
        print(f"\n⚙️  Parámetros Volume Profile:")
        print(f"   Bins: {info['parametros']['volume_profile_bins']}")
        print(f"   Value Area: {info['parametros']['vp_value_area_percent']*100}%")
        
        print(f"\n⚙️  Parámetros Correlación:")
        print(f"   Period: {info['parametros']['correlation_period']} horas")
        print(f"   Threshold Alta: {info['parametros']['correlation_threshold_high']}")
        print(f"   Threshold Baja: {info['parametros']['correlation_threshold_low']}")
        
        print(f"\n🎯 Configuración Futures:")
        print(f"   Leverage: {cerebro.leverage}X")
        print(f"   Posición: {cerebro.position_percent*100}% del capital")
        print(f"   Riesgo por trade: {cerebro.risk_per_trade*100}%")
        
        estado = cerebro.get_estado()
        print(f"\n📈 Estado inicial: {estado['estado']}")
        
        print("\n" + "=" * 50)
        print("✅ Cerebro BNB listo para integrar con Binance Futures")
        print("   Nota: Requiere cerebro BTC para análisis de correlación completo")
    
    asyncio.run(prueba_cerebro_bnb())
