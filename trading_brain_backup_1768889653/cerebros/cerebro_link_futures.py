"""
Cerebro LINK actualizado para Binance Futures
Estrategia: Fibonacci + Ichimoku + Order Flow
"""
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime
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

class CerebroLINK(CerebroFuturesBase):
    """Cerebro para LINKUSDT con estrategia Fibonacci + Ichimoku + Order Flow"""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        """Inicializa cerebro LINK"""
        if not BASE_IMPORTED:
            raise ImportError("No se pudo importar la clase base")
            
        super().__init__(
            symbol="LINKUSDT",
            binance_manager=binance_manager,
            telegram_bot=telegram_bot
        )
        
        # Configuración específica de LINK
        self.estrategia = "fibonacci_ichimoku_orderflow"
        self.timeframe = "1h"  # LINK responde mejor a timeframes mayores
        self.min_confidence = 0.70  # 70% confianza mínima para LINK
        
        # Parámetros de la estrategia
        self.ichimoku_conversion = 9
        self.ichimoku_base = 26
        self.ichimoku_span_b = 52
        self.ichimoku_displacement = 26
        
        self.fibonacci_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
        
        # Order Flow parameters
        self.volume_sma_period = 20
        self.volume_spike_multiplier = 2.5
        
        logger.info(f"🧠 Cerebro LINK inicializado - {self.estrategia}")
    
    def calcular_ichimoku(self, datos: List[Dict]) -> Dict[str, List[float]]:
        """Calcula todas las líneas del Ichimoku Cloud"""
        if len(datos) < self.ichimoku_span_b:
            return {
                'tenkan': [], 'kijun': [], 'senkou_a': [],
                'senkou_b': [], 'chikou': []
            }
        
        highs = [d['high'] for d in datos]
        lows = [d['low'] for d in datos]
        closes = [d['close'] for d in datos]
        
        # 1. Tenkan-sen (Conversion Line)
        tenkan = []
        for i in range(len(highs)):
            if i >= self.ichimoku_conversion - 1:
                period_highs = highs[i - self.ichimoku_conversion + 1:i + 1]
                period_lows = lows[i - self.ichimoku_conversion + 1:i + 1]
                tenkan.append((max(period_highs) + min(period_lows)) / 2)
            else:
                tenkan.append(np.nan)
        
        # 2. Kijun-sen (Base Line)
        kijun = []
        for i in range(len(highs)):
            if i >= self.ichimoku_base - 1:
                period_highs = highs[i - self.ichimoku_base + 1:i + 1]
                period_lows = lows[i - self.ichimoku_base + 1:i + 1]
                kijun.append((max(period_highs) + min(period_lows)) / 2)
            else:
                kijun.append(np.nan)
        
        # 3. Senkou Span A (Leading Span A)
        senkou_a = []
        for i in range(len(tenkan)):
            if not np.isnan(tenkan[i]) and not np.isnan(kijun[i]):
                senkou_a.append((tenkan[i] + kijun[i]) / 2)
            else:
                senkou_a.append(np.nan)
        
        # 4. Senkou Span B (Leading Span B)
        senkou_b = []
        for i in range(len(highs)):
            if i >= self.ichimoku_span_b - 1:
                period_highs = highs[i - self.ichimoku_span_b + 1:i + 1]
                period_lows = lows[i - self.ichimoku_span_b + 1:i + 1]
                senkou_b.append((max(period_highs) + min(period_lows)) / 2)
            else:
                senkou_b.append(np.nan)
        
        # 5. Chikou Span (Lagging Span)
        chikou = []
        for i in range(len(closes)):
            if i >= self.ichimoku_displacement:
                chikou.append(closes[i - self.ichimoku_displacement])
            else:
                chikou.append(np.nan)
        
        # Aplicar desplazamiento a Senkou spans
        senkou_a_desplazada = [np.nan] * self.ichimoku_displacement + senkou_a[:-self.ichimoku_displacement] if len(senkou_a) > self.ichimoku_displacement else [np.nan] * len(senkou_a)
        senkou_b_desplazada = [np.nan] * self.ichimoku_displacement + senkou_b[:-self.ichimoku_displacement] if len(senkou_b) > self.ichimoku_displacement else [np.nan] * len(senkou_b)
        
        return {
            'tenkan': tenkan,
            'kijun': kijun,
            'senkou_a': senkou_a_desplazada,
            'senkou_b': senkou_b_desplazada,
            'chikou': chikou,
            'price': closes
        }
    
    def calcular_fibonacci_retracement(self, swing_high: float, swing_low: float) -> Dict[float, float]:
        """Calcula niveles de Fibonacci retracement"""
        difference = swing_high - swing_low
        
        levels = {}
        for level in self.fibonacci_levels:
            price_level = swing_high - (difference * level)
            levels[level] = price_level
        
        # Añadir niveles clave extra
        levels[0] = swing_high
        levels[1] = swing_low
        levels[0.5] = swing_high - (difference * 0.5)  # 50% no es Fibonacci pero es importante
        
        return levels
    
    def identificar_swings(self, datos: List[Dict], lookback: int = 50) -> Dict:
        """Identifica swings altos y bajos recientes"""
        highs = [d['high'] for d in datos]
        lows = [d['low'] for d in datos]
        
        if len(highs) < lookback:
            lookback = len(highs)
        
        # Buscar swing highs
        swing_highs = []
        swing_high_indices = []
        
        for i in range(2, lookback - 2):
            if (highs[i] > highs[i-1] and 
                highs[i] > highs[i-2] and
                highs[i] > highs[i+1] and
                highs[i] > highs[i+2]):
                swing_highs.append(highs[i])
                swing_high_indices.append(i)
        
        # Buscar swing lows
        swing_lows = []
        swing_low_indices = []
        
        for i in range(2, lookback - 2):
            if (lows[i] < lows[i-1] and 
                lows[i] < lows[i-2] and
                lows[i] < lows[i+1] and
                lows[i] < lows[i+2]):
                swing_lows.append(lows[i])
                swing_low_indices.append(i)
        
        # Tomar los swings más recientes significativos
        if swing_highs and swing_lows:
            # Último swing high y low
            last_swing_high = swing_highs[-1] if swing_highs else highs[-1]
            last_swing_low = swing_lows[-1] if swing_lows else lows[-1]
            
            # Swing más alto y más bajo en el período
            highest_swing = max(swing_highs) if swing_highs else highs[-1]
            lowest_swing = min(swing_lows) if swing_lows else lows[-1]
            
            return {
                'last_swing_high': last_swing_high,
                'last_swing_low': last_swing_low,
                'highest_swing': highest_swing,
                'lowest_swing': lowest_swing,
                'swing_highs': swing_highs,
                'swing_lows': swing_lows,
                'is_uptrend': last_swing_high > swing_highs[-2] if len(swing_highs) > 1 else False,
                'is_downtrend': last_swing_low < swing_lows[-2] if len(swing_lows) > 1 else False
            }
        else:
            return {
                'last_swing_high': highs[-1],
                'last_swing_low': lows[-1],
                'highest_swing': max(highs[-lookback:]),
                'lowest_swing': min(lows[-lookback:]),
                'swing_highs': [],
                'swing_lows': [],
                'is_uptrend': False,
                'is_downtrend': False
            }
    
    def analizar_ichimoku_senal(self, ichimoku: Dict) -> Dict:
        """Analiza señales del Ichimoku Cloud"""
        if (len(ichimoku['tenkan']) < 1 or len(ichimoku['kijun']) < 1 or
            len(ichimoku['senkou_a']) < 1 or len(ichimoku['senkou_b']) < 1):
            return {
                'tk_cross': 'none',
                'price_vs_kumo': 'outside',
                'kumo_future': 'neutral',
                'chikou_position': 'neutral'
            }
        
        # 1. Tenkan/Kijun Cross
        tk_cross = 'none'
        if (not np.isnan(ichimoku['tenkan'][-1]) and 
            not np.isnan(ichimoku['kijun'][-1])):
            if ichimoku['tenkan'][-1] > ichimoku['kijun'][-1]:
                tk_cross = 'bullish'
            elif ichimoku['tenkan'][-1] < ichimoku['kijun'][-1]:
                tk_cross = 'bearish'
        
        # 2. Precio vs Kumo (nube)
        current_price = ichimoku['price'][-1]
        senkou_a = ichimoku['senkou_a'][-1]
        senkou_b = ichimoku['senkou_b'][-1]
        
        price_vs_kumo = 'outside'
        if not np.isnan(senkou_a) and not np.isnan(senkou_b):
            kumo_top = max(senkou_a, senkou_b)
            kumo_bottom = min(senkou_a, senkou_b)
            
            if current_price > kumo_top:
                price_vs_kumo = 'above'
            elif current_price < kumo_bottom:
                price_vs_kumo = 'below'
            else:
                price_vs_kumo = 'inside'
        
        # 3. Kumo futuro (color de la nube)
        kumo_future = 'neutral'
        if (not np.isnan(ichimoku['senkou_a'][-self.ichimoku_displacement]) and
            not np.isnan(ichimoku['senkou_b'][-self.ichimoku_displacement])):
            
            future_senkou_a = ichimoku['senkou_a'][-self.ichimoku_displacement]
            future_senkou_b = ichimoku['senkou_b'][-self.ichimoku_displacement]
            
            if future_senkou_a > future_senkou_b:
                kumo_future = 'bullish'
            elif future_senkou_a < future_senkou_b:
                kumo_future = 'bearish'
        
        # 4. Chikou Span position
        chikou_position = 'neutral'
        chikou = ichimoku['chikou'][-1]
        if not np.isnan(chikou):
            # Comparar chikou con precio de hace 26 periodos
            chikou_price_idx = len(ichimoku['price']) - self.ichimoku_displacement - 1
            if chikou_price_idx >= 0:
                price_26_periods_ago = ichimoku['price'][chikou_price_idx]
                if chikou > price_26_periods_ago:
                    chikou_position = 'bullish'
                else:
                    chikou_position = 'bearish'
        
        return {
            'tk_cross': tk_cross,
            'price_vs_kumo': price_vs_kumo,
            'kumo_future': kumo_future,
            'chikou_position': chikou_position,
            'tenkan': ichimoku['tenkan'][-1] if not np.isnan(ichimoku['tenkan'][-1]) else 0,
            'kijun': ichimoku['kijun'][-1] if not np.isnan(ichimoku['kijun'][-1]) else 0
        }
    
    def analizar_order_flow(self, datos: List[Dict]) -> Dict:
        """Analiza el flujo de órdenes basado en volumen"""
        if len(datos) < self.volume_sma_period:
            return {
                'volume_sma': 0,
                'current_volume': 0,
                'volume_spike': False,
                'volume_trend': 'neutral'
            }
        
        volumes = [d['volume'] for d in datos if 'volume' in d]
        
        if len(volumes) < self.volume_sma_period:
            return {
                'volume_sma': 0,
                'current_volume': 0,
                'volume_spike': False,
                'volume_trend': 'neutral'
            }
        
        # Calcular SMA de volumen
        recent_volumes = volumes[-self.volume_sma_period:]
        volume_sma = np.mean(recent_volumes)
        
        current_volume = volumes[-1] if volumes else 0
        
        # Detectar spike de volumen
        volume_spike = current_volume > volume_sma * self.volume_spike_multiplier
        
        # Determinar tendencia de volumen
        volume_trend = 'neutral'
        if len(volumes) >= 5:
            recent_trend = np.polyfit(range(5), volumes[-5:], 1)[0]
            if recent_trend > 0.1:
                volume_trend = 'increasing'
            elif recent_trend < -0.1:
                volume_trend = 'decreasing'
        
        return {
            'volume_sma': volume_sma,
            'current_volume': current_volume,
            'volume_spike': volume_spike,
            'volume_trend': volume_trend,
            'volume_ratio': current_volume / volume_sma if volume_sma > 0 else 0
        }
    
    def generar_senal(self, datos: List[Dict], precio_actual: float) -> Optional[Dict]:
        """
        Implementación específica de la estrategia Fibonacci + Ichimoku + Order Flow
        
        Args:
            datos: Datos OHLCV
            precio_actual: Precio actual
            
        Returns:
            Señal generada o None
        """
        try:
            if len(datos) < 100:
                logger.warning(f"LINK - Datos insuficientes")
                return None
            
            # 1. Calcular Ichimoku
            ichimoku = self.calcular_ichimoku(datos)
            
            # 2. Identificar swings para Fibonacci
            swings = self.identificar_swings(datos)
            
            # 3. Calcular niveles Fibonacci
            fib_levels = self.calcular_fibonacci_retracement(
                swings['highest_swing'],
                swings['lowest_swing']
            )
            
            # 4. Analizar Ichimoku
            ichimoku_senal = self.analizar_ichimoku_senal(ichimoku)
            
            # 5. Analizar Order Flow
            order_flow = self.analizar_order_flow(datos)
            
            # 6. Determinar nivel Fibonacci actual más cercano
            current_fib_level = None
            fib_distance = float('inf')
            
            for level, price in fib_levels.items():
                distance = abs(precio_actual - price) / price
                if distance < fib_distance:
                    fib_distance = distance
                    current_fib_level = level
            
            # 7. Tomar decisión basada en múltiples factores
            razones = []
            indicadores = {
                'ichimoku_tk_cross': ichimoku_senal['tk_cross'],
                'ichimoku_price_vs_kumo': ichimoku_senal['price_vs_kumo'],
                'ichimoku_kumo_future': ichimoku_senal['kumo_future'],
                'ichimoku_chikou': ichimoku_senal['chikou_position'],
                'fibonacci_level': current_fib_level,
                'fibonacci_distance_pct': fib_distance * 100,
                'volume_spike': order_flow['volume_spike'],
                'volume_trend': order_flow['volume_trend'],
                'market_trend': 'uptrend' if swings['is_uptrend'] else 'downtrend' if swings['is_downtrend'] else 'range'
            }
            
            confianza_base = 0.0
            señales_alcistas = 0
            señales_bajistas = 0
            
            # SEÑAL ALCISTA FUERTE: Precio en soporte Fibonacci + TK Cross alcista + Precio sobre Kumo
            if (current_fib_level in [0.618, 0.786] and  # Soporte Fibonacci fuerte
                ichimoku_senal['tk_cross'] == 'bullish' and
                ichimoku_senal['price_vs_kumo'] == 'above' and
                order_flow['volume_spike']):
                
                razones.append(f"Precio en soporte Fibonacci fuerte ({current_fib_level})")
                razones.append("Tenkan-sen sobre Kijun-sen (TK Cross alcista)")
                razones.append("Precio sobre la nube Ichimoku")
                razones.append("Spike de volumen confirmando acumulación")
                confianza_base = 0.85
                señales_alcistas = 4
            
            # SEÑAL BAJISTA FUERTE: Precio en resistencia Fibonacci + TK Cross bajista + Precio bajo Kumo
            elif (current_fib_level in [0.236, 0.382] and  # Resistencia Fibonacci fuerte
                  ichimoku_senal['tk_cross'] == 'bearish' and
                  ichimoku_senal['price_vs_kumo'] == 'below' and
                  order_flow['volume_spike']):
                
                razones.append(f"Precio en resistencia Fibonacci fuerte ({current_fib_level})")
                razones.append("Tenkan-sen bajo Kijun-sen (TK Cross bajista)")
                razones.append("Precio bajo la nube Ichimoku")
                razones.append("Spike de volumen confirmando distribución")
                confianza_base = 0.85
                señales_bajistas = 4
            
            # SEÑAL ALCISTA MODERADA: Precio cerca de Fibonacci 0.5 + Kumo futuro alcista + Chikou bullish
            elif (0.45 <= current_fib_level <= 0.55 and  # Cerca de 50%
                  ichimoku_senal['kumo_future'] == 'bullish' and
                  ichimoku_senal['chikou_position'] == 'bullish'):
                
                razones.append(f"Precio cerca del nivel 50% Fibonacci ({current_fib_level:.3f})")
                razones.append("Nube Ichimoku futura alcista")
                razones.append("Chikou Span en posición alcista")
                confianza_base = 0.75
                señales_alcistas = 3
            
            # SEÑAL BAJISTA MODERADA: Precio cerca de Fibonacci 0.5 + Kumo futuro bajista + Chikou bearish
            elif (0.45 <= current_fib_level <= 0.55 and
                  ichimoku_senal['kumo_future'] == 'bearish' and
                  ichimoku_senal['chikou_position'] == 'bearish'):
                
                razones.append(f"Precio cerca del nivel 50% Fibonacci ({current_fib_level:.3f})")
                razones.append("Nube Ichimoku futura bajista")
                razones.append("Chikou Span en posición bajista")
                confianza_base = 0.75
                señales_bajistas = 3
            
            # SEÑAL DÉBIL: Solo Ichimoku o solo Fibonacci con confirmación menor
            elif (ichimoku_senal['tk_cross'] == 'bullish' and
                  ichimoku_senal['price_vs_kumo'] == 'above'):
                
                razones.append("TK Cross alcista")
                razones.append("Precio sobre la nube")
                if swings['is_uptrend']:
                    razones.append("Mercado en tendencia alcista")
                    confianza_base = 0.68
                else:
                    confianza_base = 0.60
                señales_alcistas = 2
            
            elif (ichimoku_senal['tk_cross'] == 'bearish' and
                  ichimoku_senal['price_vs_kumo'] == 'below'):
                
                razones.append("TK Cross bajista")
                razones.append("Precio bajo la nube")
                if swings['is_downtrend']:
                    razones.append("Mercado en tendencia bajista")
                    confianza_base = 0.68
                else:
                    confianza_base = 0.60
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
            logger.debug(f"LINK - Sin señal clara. "
                        f"Fib: {current_fib_level:.3f}, "
                        f"Ichimoku TK: {ichimoku_senal['tk_cross']}, "
                        f"Price vs Kumo: {ichimoku_senal['price_vs_kumo']}")
            
            return None
            
        except Exception as e:
            logger.error(f"LINK - Error en generación de señal: {e}")
            return None
    
    def get_info_estrategia(self) -> Dict:
        """Devuelve información detallada de la estrategia"""
        return {
            'nombre': 'Fibonacci + Ichimoku + Order Flow',
            'descripcion': 'Combina niveles Fibonacci, Ichimoku Cloud y análisis de volumen',
            'parametros': {
                'ichimoku_conversion': self.ichimoku_conversion,
                'ichimoku_base': self.ichimoku_base,
                'ichimoku_span_b': self.ichimoku_span_b,
                'ichimoku_displacement': self.ichimoku_displacement,
                'fibonacci_levels': self.fibonacci_levels,
                'volume_sma_period': self.volume_sma_period,
                'volume_spike_multiplier': self.volume_spike_multiplier,
                'timeframe': self.timeframe,
                'min_confidence': self.min_confidence
            },
            'reglas': [
                'Señal fuerte: Fibonacci extremo + Ichimoku confirmación + Volume spike',
                'Señal moderada: Fibonacci 50% + Kumo futuro + Chikou posición',
                'Señal débil: Solo Ichimoku o tendencia con confirmación menor'
            ]
        }

if __name__ == "__main__":
    # Prueba del cerebro LINK
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    print("🧠 PRUEBA CEREBRO LINK FUTURES")
    print("=" * 50)
    
    async def prueba_cerebro_link():
        cerebro = CerebroLINK()
        
        print(f"✅ Cerebro LINK creado")
        print(f"   Símbolo: {cerebro.symbol}")
        print(f"   Estrategia: {cerebro.estrategia}")
        
        info = cerebro.get_info_estrategia()
        print(f"\n📊 Información de estrategia:")
        print(f"   Nombre: {info['nombre']}")
        print(f"   Descripción: {info['descripcion']}")
        print(f"   Timeframe: {info['parametros']['timeframe']}")
        
        print(f"\n⚙️  Parámetros Ichimoku:")
        print(f"   Conversion: {info['parametros']['ichimoku_conversion']}")
        print(f"   Base: {info['parametros']['ichimoku_base']}")
        print(f"   Span B: {info['parametros']['ichimoku_span_b']}")
        print(f"   Displacement: {info['parametros']['ichimoku_displacement']}")
        
        print(f"\n⚙️  Parámetros Fibonacci:")
        print(f"   Levels: {info['parametros']['fibonacci_levels']}")
        
        print(f"\n🎯 Configuración Futures:")
        print(f"   Leverage: {cerebro.leverage}X")
        print(f"   Posición: {cerebro.position_percent*100}% del capital")
        print(f"   Riesgo por trade: {cerebro.risk_per_trade*100}%")
        
        estado = cerebro.get_estado()
        print(f"\n📈 Estado inicial: {estado['estado']}")
        
        print("\n" + "=" * 50)
        print("✅ Cerebro LINK listo para integrar con Binance Futures")
    
    asyncio.run(prueba_cerebro_link())
