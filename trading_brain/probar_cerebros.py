#!/usr/bin/env python3
"""Script para probar los 10 cerebros."""
import sys
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar configuración
with open('config_futures_completo.json', 'r') as f:
    config = json.load(f)

# Probar cada cerebro
print("=== PRUEBA DE 10 CEREBROS ===")

for par, info in config['cerebros'].items():
    if info['activo']:
        try:
            # Importar dinámicamente
            module_name = f"cerebros.cerebro_{par[:3].lower()}_futures"
            class_name = f"Cerebro{par[:3]}Futures"
            
            print(f"\n🧠 Probando {par}...")
            
            # Importar
            module = __import__(f"cerebros.cerebro_{par[:3].lower()}_futures", fromlist=[class_name])
            cerebro_class = getattr(module, class_name)
            
            # Crear instancia
            cerebro = cerebro_class(None, None)
            
            # Probar análisis
            resultado = cerebro.analizar()
            
            if resultado:
                print(f"   ✅ Funciona: {resultado['direccion']} (conf: {resultado['confianza']})")
                print(f"   📊 Precio: {resultado['precio_actual']}")
            else:
                print(f"   ⚠️  Sin señal")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}...")

print("\n=== PRUEBA COMPLETADA ===")
