from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import subprocess
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Permitir acceso desde móvil

# Ruta a los archivos del bot
BOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Obtener estado del sistema"""
    try:
        # Leer stats.json
        with open(BOT_PATH + 'stats.json', 'r') as f:
            stats = json.load(f)
        
        # Leer precios aproximados (de logs o simular)
        precios = obtener_precios_estimados()
        
        return jsonify({
            'success': True,
            'data': {
                'sistema': 'OPERATIVO',
                'hora': datetime.now().strftime('%H:%M:%S'),
                'stats': stats,
                'precios': precios,
                'procesos': obtener_estado_procesos()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/señales')
def get_señales():
    """Obtener últimas señales"""
    # Por ahora simulamos, luego conectamos a DB
    return jsonify({
        'success': True,
        'señales': [
            {'par': 'BTCUSDT', 'direccion': 'COMPRA', 'entrada': 90500, 'hora': '10:30'},
            {'par': 'ETHUSDT', 'direccion': 'VENTA', 'entrada': 3015, 'hora': '11:15'}
        ]
    })

@app.route('/api/graficos/<par>')
def get_grafico(par):
    """Datos para gráfico de un par"""
    # Datos simulados para gráfico
    import random
    datos = []
    base = 90000 if par == 'BTC' else 3000 if par == 'ETH' else 100
    for i in range(50):
        datos.append({
            'time': f'10:{30-i}',
            'open': base + random.uniform(-100, 100),
            'high': base + random.uniform(0, 150),
            'low': base + random.uniform(-150, 0),
            'close': base + random.uniform(-100, 100)
        })
    
    return jsonify({'success': True, 'datos': datos})

def obtener_precios_estimados():
    """Obtener precios actuales estimados"""
    # Por ahora simulados, luego de API real
    return {
        'BTC': 90500,
        'ETH': 3015,
        'SOL': 130,
        'LINK': 12.5,
        'BNB': 890,
        'ADA': 0.365,
        'AVAX': 12.5,
        'XRP': 1.95,
        'DOT': 1.94,
        'ATOM': 2.38
    }

def obtener_estado_procesos():
    """Verificar estado de PM2"""
    try:
        result = subprocess.run(['pm2', 'jlist'], capture_output=True, text=True)
        procesos = json.loads(result.stdout)
        
        estados = {}
        for p in procesos:
            if p['name'] in ['trading_bot', 'telegram_status', 'monitor_simple']:
                estados[p['name']] = p['pm2_env']['status']
        
        return estados
    except:
        return {'trading_bot': 'unknown', 'telegram_status': 'unknown'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
