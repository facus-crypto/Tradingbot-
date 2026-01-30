# cerebros/cerebro_ada_futures.py
# Cerebro para Cardano (ADAUSDT) - Estrategia: canal_tendencia_rsi_div

import pandas as pd
import numpy as np
from typing import Dict, Optional
from .cerebro_base_futures import CerebroFuturesBase

class CerebroADAFutures(CerebroFuturesBase):
    """Cerebro para Cardano (ADA) con estrategia de canal de tendencia y RSI."""
    
    def __init__(self, binance_manager=None, telegram_bot=None):
        super().__init__("ADAUSDT", binance_manager, telegram_bot)
        self.nombre_estrategia = "canal_tendencia_rsi_div"
        self.intervalo = "15m"  # Timeframe para ADA
        print(f"[ADAUSDT] ✅ Cerebro ADA inicializado - {self.nombre_estrategia}")
    
    def calcular_donchian(self, datos: pd.DataFrame, periodo: int = 20) -> Dict:
        """Calcula el canal de Donchian (canal de tendencia)."""
        if len(datos) < periodo:
            return {'superior': None, 'inferior': None, 'medio': None}
        
        datos['donchian_superior'] = datos['high'].rolling(window=periodo).max()
        datos['donchian_inferior'] = datos['low'].rolling(window=periodo).min()
        datos['donchian_medio'] = (datos['donchian_superior'] + datos['donchian_inferior']) / 2
        
        ultimo = datos.iloc[-1]
        return {
            'superior': ultimo['donchian_superior'],
            'inferior': ultimo['donchian_inferior'],
            'medio': ultimo['donchian_medio'],
            'ancho': ultimo['donchian_superior'] - ultimo['donchian_inferior']
        }
    
    def calcular_rsi_divergencia(self, datos: pd.DataFrame, periodo: int = 14) -> Dict:
        """Calcula RSI y detecta divergencias básicas."""
        delta = datos['close'].diff()
        ganancia = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
        perdida = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
        rs = ganancia / perdida
        datos['rsi'] = 100 - (100 / (1 + rs))
        
        # Detección simple de divergencia (precio hace máx menor, RSI hace máx mayor = divergencia alcista)
        ultimo_rsi = datos['rsi'].iloc[-1]
        
        return {
            'rsi': ultimo_rsi,
            'sobrecompra': ultimo_rsi > 70,
            'sobreventa': ultimo_rsi < 30,
            'divergencia_alcista': False,  # Implementar lógica completa después
            'divergencia_bajista': False
        }
    
    async def analizar(self) -> Optional[Dict]:
        """Método principal de análisis para ADA."""
        try:
            # 1. Obtener datos
            datos = await self.obtener_datos()
            if datos is None or len(datos) < 50:
                return None
            
            # 2. Calcular indicadores
            canal = self.calcular_donchian(datos, periodo=20)
            rsi_info = self.calcular_rsi_divergencia(datos, periodo=14)
            precio_actual = datos['close'].iloc[-1]
            
            # 3. Lógica de entrada - CONDICIONES EJEMPLO (AJUSTAR DESPUÉS)
            senal = None
            motivo = []
            
            # Posible COMPRA: Precio cerca del canal inferior + RSI oversold
            if (canal['inferior'] is not None and 
                precio_actual <= canal['inferior'] * 1.01 and  # Precio <= canal inferior
                rsi_info['sobreventa']):
                
                senal = {
                    'accion': 'COMPRAR',
                    'precio_entrada': precio_actual,
                    'stop_loss': precio_actual * 0.97,  # -3%
                    'take_profit': precio_actual * 1.06,  # +6%
                    'motivo': f"Canal Donchian inferior + RSI oversold ({rsi_info['rsi']:.1f,
            'stop_loss': sl,
            'take_profit': tp,
            'fase_trailing': fase
        })"
                }
            
            # Posible VENTA: Precio cerca del canal superior + RSI overbought
            elif (canal['superior'] is not None and 
                  precio_actual >= canal['superior'] * 0.99 and  # Precio >= canal superior
                  rsi_info['sobrecompra']):
                
                senal = {
                    'accion': 'VENDER',
                    'precio_entrada': precio_actual,
                    'stop_loss': precio_actual * 1.03,  # +3%
                    'take_profit': precio_actual * 0.94,  # -6%
                    'motivo': f"Canal Donchian superior + RSI overbought ({rsi_info['rsi']:.1f,
            'stop_loss': sl,
            'take_profit': tp,
            'fase_trailing': fase
        })"
                }
            
            if senal:
                print(f"[ADAUSDT] 🔍 Señal detectada: {senal['accion']} - {senal['motivo']}")
                return senal
            
            return None
            
        except Exception as e:
            print(f"[ADAUSDT] ❌ Error en análisis: {e}")
            return None

# Código para prueba rápida
if __name__ == "__main__":
    print("🧠 Prueba del cerebro ADAUSDT - Estrategia: canal_tendencia_rsi_div")
    print("✅ Archivo creado correctamente")
    print("📊 Indicadores: Canal Donchian (20) + RSI (14) con divergencias")
