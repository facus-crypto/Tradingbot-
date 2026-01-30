#!/usr/bin/env python3
"""
Módulo de Backtesting para señales de trading
Analiza 30 días históricos para validar señales
"""
import json
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Backtester:
    """Backtesting de señales contra datos históricos"""
    
    def __init__(self, binance_manager):
        self.bm = binance_manager
        self.dias_backtest = 30  # Analizar últimos 30 días
        self.cache_datos = {}  # Cache para no descargar repetido
        
    def obtener_datos_historicos(self, simbolo: str, intervalo: str = '1h') -> pd.DataFrame:
        """Obtiene datos históricos de Binance"""
        try:
            # Verificar cache
            cache_key = f"{simbolo}_{intervalo}"
            if cache_key in self.cache_datos:
                return self.cache_datos[cache_key]
            
            # Calcular fechas (últimos 30 días)
            fecha_fin = datetime.now()
            fecha_inicio = fecha_fin - timedelta(days=self.dias_backtest)
            
            # Convertir a timestamp milisegundos
            start_ts = int(fecha_inicio.timestamp() * 1000)
            end_ts = int(fecha_fin.timestamp() * 1000)
            
            logger.info(f"📥 Descargando datos históricos {simbolo} ({intervalo}) - {self.dias_backtest} días")
            
            # Descargar datos (máximo 1000 velas por request)
            all_velas = []
            current_start = start_ts
            
            while current_start < end_ts:
                current_end = min(current_start + (1000 * 3600000), end_ts)
                
                url = f"https://api.binance.com/api/v3/klines"
                params = {
                    'symbol': simbolo,
                    'interval': intervalo,
                    'startTime': current_start,
                    'endTime': current_end,
                    'limit': 1000
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    velas = response.json()
                    all_velas.extend(velas)
                else:
                    logger.error(f"Error descargando datos: {response.status_code}")
                    break
                
                current_start = current_end + 1
                # Pequeña pausa para no sobrecargar API
                import time
                time.sleep(0.1)
            
            if not all_velas:
                return pd.DataFrame()
            
            # Convertir a DataFrame
            df = pd.DataFrame(all_velas, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            # Convertir tipos
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col])
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Guardar en cache
            self.cache_datos[cache_key] = df
            logger.info(f"✅ Datos descargados: {len(df)} velas para {simbolo}")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo datos históricos {simbolo}: {e}")
            return pd.DataFrame()
    
    def encontrar_señales_similares(self, df: pd.DataFrame, señal_actual: Dict) -> List[Dict]:
        """Encuentra señales históricas similares a la actual"""
        señales_similares = []
        
        try:
            # Parámetros de la señal actual
            direccion_actual = señal_actual['direccion']
            confianza_actual = señal_actual['confianza']
            
            # Buscar en datos históricos (excluyendo últimos 2 días para evitar data snooping)
            df_historico = df.iloc[:-48] if len(df) > 48 else df
            
            for i in range(20, len(df_historico) - 20):  # Necesitamos futuro para evaluar
                precio = float(df_historico.iloc[i]['close'])
                
                # SIMULACIÓN SIMPLE - Aquí iría tu lógica de detección real
                # Por ahora, buscamos momentos con precio similar y tendencia
                precio_actual = señal_actual.get('precio_actual', 0)
                
                if precio_actual > 0:
                    diferencia_porcentual = abs(precio - precio_actual) / precio_actual * 100
                    
                    # Si precio similar (dentro del 3%) y tenemos datos futuros
                    if diferencia_porcentual < 3.0:
                        # Simular resultado futuro (próximas 24 velas = 24 horas)
                        futuro_inicio = i + 1
                        futuro_fin = min(i + 24, len(df))
                        
                        if futuro_fin - futuro_inicio >= 12:  # Al menos 12 horas de datos
                            precio_futuro = float(df.iloc[futuro_fin]['close'])
                            cambio_porcentual = (precio_futuro - precio) / precio * 100
                            
                            # Determinar si fue ganadora según dirección
                            if direccion_actual == "COMPRA":
                                ganadora = cambio_porcentual > 1.0  # +1% = ganadora
                            else:  # VENTA
                                ganadora = cambio_porcentual < -1.0  # -1% = ganadora
                            
                            señales_similares.append({
                                'timestamp': df.index[i],
                                'precio_entrada': precio,
                                'precio_salida': precio_futuro,
                                'cambio_porcentual': cambio_porcentual,
                                'ganadora': ganadora,
                                'horas_holding': futuro_fin - futuro_inicio
                            })
            
            logger.info(f"🔍 Encontradas {len(señales_similares)} señales similares históricas")
            return señales_similares
            
        except Exception as e:
            logger.error(f"❌ Error encontrando señales similares: {e}")
            return []
    
    def calcular_metricas(self, señales_similares: List[Dict]) -> Dict:
        """Calcula métricas de performance"""
        if not señales_similares:
            return {
                'win_rate': 0,
                'total_señales': 0,
                'señales_ganadoras': 0,
                'señales_perdedoras': 0,
                'profit_promedio': 0,
                'loss_promedio': 0,
                'profit_factor': 0,
                'max_drawdown_promedio': 0,
                'confianza_historica': 0
            }
        
        # Separar ganadoras y perdedoras
        ganadoras = [s for s in señales_similares if s['ganadora']]
        perdedoras = [s for s in señales_similares if not s['ganadora']]
        
        # Calcular métricas
        total_señales = len(señales_similares)
        señales_ganadoras = len(ganadoras)
        
        win_rate = (señales_ganadoras / total_señales * 100) if total_señales > 0 else 0
        
        # Profit/Loss promedio
        profit_promedio = np.mean([s['cambio_porcentual'] for s in ganadoras]) if ganadoras else 0
        loss_promedio = np.mean([s['cambio_porcentual'] for s in perdedoras]) if perdedoras else 0
        
        # Profit Factor (ganancias totales / pérdidas totales)
        ganancias_totales = sum([s['cambio_porcentual'] for s in ganadoras]) if ganadoras else 0
        pérdidas_totales = abs(sum([s['cambio_porcentual'] for s in perdedoras])) if perdedoras else 0
        profit_factor = ganancias_totales / pérdidas_totales if pérdidas_totales > 0 else float('inf')
        
        # Confianza histórica (combinación de métricas)
        confianza_historica = min(0.95, (win_rate / 100) * 0.7 + (min(profit_factor, 3) / 3) * 0.3)
        
        return {
            'win_rate': round(win_rate, 1),
            'total_señales': total_señales,
            'señales_ganadoras': señales_ganadoras,
            'señales_perdedoras': len(perdedoras),
            'profit_promedio': round(profit_promedio, 2),
            'loss_promedio': round(loss_promedio, 2),
            'profit_factor': round(profit_factor, 2),
            'confianza_historica': round(confianza_historica, 2),
            'valido': total_señales >= 5  # Mínimo 5 señales para considerarlo válido
        }
    
    def backtestear_señal(self, señal: Dict, simbolo: str) -> Dict:
        """Backtesting principal para una señal"""
        try:
            logger.info(f"🔬 Iniciando backtesting para {simbolo} - {señal['direccion']}")
            
            # 1. Obtener datos históricos
            df_historico = self.obtener_datos_historicos(simbolo, '1h')
            if df_historico.empty:
                return {
                    'backtest_completado': False,
                    'error': 'Sin datos históricos',
                    'win_rate': 0,
                    'valido': False
                }
            
            # 2. Encontrar señales similares
            señales_similares = self.encontrar_señales_similares(df_historico, señal)
            
            # 3. Calcular métricas
            metricas = self.calcular_metricas(señales_similares)
            
            # 4. Recomendar acción
            recomendacion = "NEUTRAL"
            if metricas['valido']:
                if metricas['win_rate'] >= 60 and metricas['profit_factor'] >= 1.5:
                    recomendacion = "FUERTE"
                elif metricas['win_rate'] >= 55 and metricas['profit_factor'] >= 1.2:
                    recomendacion = "MODERADA"
                else:
                    recomendacion = "DEBIL"
            
            resultado = {
                'backtest_completado': True,
                'simbolo': simbolo,
                'direccion_señal': señal['direccion'],
                'confianza_señal': señal.get('confianza', 0),
                'timestamp': datetime.now().isoformat(),
                'señales_analizadas': len(señales_similares),
                'recomendacion': recomendacion,
                **metricas
            }
            
            logger.info(f"✅ Backtesting completado: Win Rate {metricas['win_rate']}%, Recomendación: {recomendacion}")
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Error en backtesting: {e}")
            return {
                'backtest_completado': False,
                'error': str(e),
                'win_rate': 0,
                'valido': False
            }
    
    def sugerir_parametros(self, metricas: Dict) -> Dict:
        """Sugiere parámetros óptimos basado en backtesting"""
        if not metricas['valido']:
            return {
                'stop_loss': -2.0,
                'take_profit': 3.0,
                'trailing_activar': False
            }
        
        # Basado en métricas históricas
        win_rate = metricas['win_rate']
        profit_avg = metricas['profit_promedio']
        loss_avg = metricas['loss_promedio']
        
        # Calcular parámetros sugeridos
        stop_loss_sugerido = max(-3.0, min(-1.0, loss_avg * 0.8))  # 80% del loss promedio
        take_profit_sugerido = min(5.0, max(2.0, profit_avg * 0.9))  # 90% del profit promedio
        
        # Activar trailing solo si win_rate alto
        trailing_activar = win_rate > 65
        
        return {
            'stop_loss': round(stop_loss_sugerido, 2),
            'take_profit': round(take_profit_sugerido, 2),
            'trailing_activar': trailing_activar,
            'trailing_distancia': 1.5 if trailing_activar else 0
        }

# Función de utilidad para usar sin instanciar clase
def backtestear_señal_rapido(señal: Dict, simbolo: str, binance_manager=None) -> Dict:
    """Función rápida para backtesting"""
    backtester = Backtester(binance_manager)
    return backtester.backtestear_señal(señal, simbolo)

if __name__ == "__main__":
    # Ejemplo de uso
    print("🧪 Probando módulo de backtesting...")
    
    # Señal de ejemplo
    señal_ejemplo = {
        'direccion': 'COMPRA',
        'confianza': 0.75,
        'precio_actual': 50000,
        'indicadores': {'rsi': 45, 'ema': 'alcista'}
    }
    
    resultado = backtestear_señal_rapido(señal_ejemplo, 'BTCUSDT')
    print(f"Resultado: {resultado}")
