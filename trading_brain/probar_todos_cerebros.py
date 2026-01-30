#!/usr/bin/env python3
"""Script para probar los 10 cerebros CORREGIDO."""
import sys
import json
import logging
import pandas as pd

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapeo correcto de pares a archivos
mapeo_cerebros = {
    "BTCUSDT": ("cerebro_btc_futures", "CerebroBTCFutures"),
    "ETHUSDT": ("cerebro_eth_futures", "CerebroETHFutures"),
    "SOLUSDT": ("cerebro_sol_futures", "CerebroSOLFutures"),
    "LINKUSDT": ("cerebro_link_futures", "CerebroLINKFutures"),
    "BNBUSDT": ("cerebro_bnb_futures", "CerebroBNBFutures"),
    "ADAUSDT": ("cerebro_ada_futures", "CerebroADAFutures"),
    "AVAXUSDT": ("cerebro_avax_futures", "CerebroAVAXFutures"),
    "XRPUSDT": ("cerebro_xrp_futures", "CerebroXRPFutures"),
    "DOTUSDT": ("cerebro_dot_futures", "CerebroDOTFutures"),
    "ATOMUSDT": ("cerebro_atom_futures", "CerebroATOMFutures"),
}

print("=== PRUEBA DE 10 CEREBROS (CORREGIDO) ===\n")

for par, (modulo, clase) in mapeo_cerebros.items():
    try:
        print(f"🧠 Probando {par}...")
        
        # Importar dinámicamente
        module_path = f"cerebros.{modulo}"
        cerebro_module = __import__(module_path, fromlist=[clase])
        cerebro_class = getattr(cerebro_module, clase)
        
        # Crear instancia
        cerebro = cerebro_class(None, None)
        
        # Probar análisis
        resultado = cerebro.analizar()
        
        if resultado:
            estado = "✅" if resultado['direccion'] != "NEUTRAL" else "⚠️"
            print(f"   {estado} {resultado['direccion']} (conf: {resultado['confianza']})")
            print(f"   📊 Precio: {resultado['precio_actual']:.4f}")
            
            # Mostrar indicadores clave
            if 'rsi' in resultado['indicadores']:
                print(f"   📈 RSI: {resultado['indicadores']['rsi']}")
            if 'macd' in resultado['indicadores']:
                print(f"   📉 MACD: {resultado['indicadores']['macd']:.4f}")
        else:
            print("   ❌ Sin resultado")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:60]}...")
    
    print()  # Línea en blanco

print("=== FIN DE PRUEBA ===")
print("\n📊 RESUMEN:")
print("-" * 40)
print("✅ Con lógica real: BTC, ETH, SOL, LINK, BNB, ADA")
print("⚠️  Template básico: XRP, DOT, ATOM")
print("✅ Original funcional: AVAX")
print("-" * 40)
print("\n🎯 SIGUIENTE PASO: Conectar Binance API para datos reales")
