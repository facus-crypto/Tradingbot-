# cerebros/cerebro_avax_futures.py
# Cerebro para Avalanche (AVAXUSDT) - Estrategia: ema_multiple_macd_hist

import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase

class CerebroAVAXFutures(CerebroFuturesBase):
    """Cerebro para Avalanche (AVAX) con EMAs múltiples y MACD Histograma."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("AVAXUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "ema_multiple_macd_hist"
        self.timeframe = "1h"  # Para tendencias
        print(f"[AVAXUSDT] ✅ Cerebro AVAX inicializado - {self.nombre_estrategia}")
    
    def calcular_emas_multiples(self, datos: pd.DataFrame) -> Dict:
        """Calcula múltiples EMAs (20, 50, 100)."""
        if len(datos) < 100:
            return {'ema20': None, 'ema50': None, 'ema100': None, 'tendencia': 'NEUTRAL'}
        
        datos['ema20'] = datos['close'].ewm(span=20, adjust=False).mean()
        datos['ema50'] = datos['close'].ewm(span=50, adjust=False).mean()
        datos['ema100'] = datos['close'].ewm(span=100, adjust=False).mean()
        
        ultimo = datos.iloc[-1]
        
        # Determinar tendencia por alineación de EMAs
        if ultimo['ema20'] > ultimo['ema50'] > ultimo['ema100']:
            tendencia = "ALCISTA"
        elif ultimo['ema20'] < ultimo['ema50'] < ultimo['ema100']:
            tendencia = "BAJISTA"
        else:
            tendencia = "NEUTRAL"
        
        return {
            'ema20': ultimo['ema20'],
            'ema50': ultimo['ema50'],
            'ema100': ultimo['ema100'],
            'tendencia': tendencia,
            'distancia_20_50': abs(ultimo['ema20'] - ultimo['ema50']) / ultimo['ema50'] * 100,
            'distancia_50_100': abs(ultimo['ema50'] - ultimo['ema100']) / ultimo['ema100'] * 100
        }
    
    def calcular_macd_histograma(self, datos: pd.DataFrame) -> Dict:
        """Calcula MACD con enfoque en el histograma."""
        if len(datos) < 50:
            return {'macd': None, 'signal': None, 'histograma': None, 'cruce': 'NEUTRAL'}
        
        # Calcular MACD manualmente
        exp1 = datos['close'].ewm(span=12, adjust=False).mean()
        exp2 = datos['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histograma = macd - signal
        
        ultimo_hist = histograma.iloc[-1]
        previo_hist = histograma.iloc[-2]
        
        # Detectar cruces por histograma (más sensible)
        if previo_hist < 0 and ultimo_hist > 0:
            cruce = "ALCISTA"  # Histograma cruza de negativo a positivo
        elif previo_hist > 0 and ultimo_hist < 0:
            cruce = "BAJISTA"  # Histograma cruza de positivo a negativo
        else:
            cruce = "NEUTRAL"
        
        return {
            'macd': macd.iloc[-1],
            'signal': signal.iloc[-1],
            'histograma': ultimo_hist,
            'cruce': cruce,
            'creciendo': ultimo_hist > previo_hist  # Histograma creciendo/decreciendo
        }
    
    async def analizar(self) -> Optional[Dict]:
        """Método principal de análisis para AVAX."""
        try:
            # 1. Obtener datos
            datos = await self.obtener_datos()
            if datos is None or len(datos) < 100:
                return None
            
            # 2. Calcular indicadores
            emas = self.calcular_emas_multiples(datos)
            macd_info = self.calcular_macd_histograma(datos)
            precio_actual = datos['close'].iloc[-1]
            
            # 3. Lógica de entrada
            senal = None
            
            # COMPRA: EMAs alcistas + MACD histograma cruce alcista
            if (emas['tendencia'] == "ALCISTA" and
                emas['distancia_20_50'] < 2.0 and  # EMAs cercanos (consolidación)
                macd_info['cruce'] == "ALCISTA" and
                macd_info['histograma'] is not None and macd_info['histograma'] > -0.001):
                
                # Precio cerca de EMA 20 (entrada óptima)
                if abs(precio_actual - emas['ema20']) / emas['ema20'] < 0.01:
                    senal = {
                        'accion': 'COMPRAR',
                        'precio_entrada': precio_actual,
                        'stop_loss': precio_actual * 0.96,  # -4%
                        'take_profit': precio_actual * 1.08,  # +8%
                        'motivo': f"EMAs alcistas ({emas['tendencia'],
            'stop_loss': sl,
            'take_profit': tp,
            'fase_trailing': fase
        }) + MACD histograma cruce alcista (hist: {macd_info['histograma']:.6f})"
                    }
            
            # VENTA: EMAs bajistas + MACD histograma cruce bajista
            elif (emas['tendencia'] == "BAJISTA" and
                  emas['distancia_20_50'] < 2.0 and
                  macd_info['cruce'] == "BAJISTA" and
                  macd_info['histograma'] is not None and macd_info['histograma'] < 0.001):
                
                if abs(precio_actual - emas['ema20']) / emas['ema20'] < 0.01:
                    senal = {
                        'accion': 'VENDER',
                        'precio_entrada': precio_actual,
                        'stop_loss': precio_actual * 1.04,  # +4%
                        'take_profit': precio_actual * 0.92,  # -8%
                        'motivo': f"EMAs bajistas ({emas['tendencia'],
            'stop_loss': sl,
            'take_profit': tp,
            'fase_trailing': fase
        }) + MACD histograma cruce bajista (hist: {macd_info['histograma']:.6f})"
                    }
            
            if senal:
                print(f"[AVAXUSDT] 🔍 Señal detectada: {senal['accion']} - {senal['motivo']}")
                return senal
            
            return None
            
        except Exception as e:
            print(f"[AVAXUSDT] ❌ Error en análisis: {e}")
            return None

# Prueba rápida
if __name__ == "__main__":
    print("🧠 Cerebro AVAXUSDT creado - Estrategia: ema_multiple_macd_hist")
    print("📊 Indicadores: EMAs (20, 50, 100) + MACD Histograma")
    print("⏰ Timeframe: 1h (tendencias)")
    print("✅ Archivo listo para integrar")
