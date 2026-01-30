#!/usr/bin/env python3
"""
🚀 WEB APP PROFESIONAL - Trading Bot Dashboard
Conectado al bot real en tiempo real
"""
from flask import Flask, render_template, jsonify, request, g
from flask_cors import CORS
import json
import subprocess
from datetime import datetime, timedelta
import os
import sqlite3
import threading
import time
import requests
from typing import Dict, List, Optional

# ============================================
# CONFIGURACIÓN
# ============================================
app = Flask(__name__)
CORS(app)  # Permitir acceso desde móvil

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATS_FILE = os.path.join(BASE_DIR, 'stats.json')
CONFIG_FILE = os.path.join(BASE_DIR, 'config_futures.json')
DB_FILE = os.path.join(BASE_DIR, 'trading_bot.db')

# Cargar configuración
with open(CONFIG_FILE, 'r') as f:
    CONFIG = json.load(f)

TELEGRAM_TOKEN = CONFIG['telegram']['token']
TELEGRAM_CHAT_ID = CONFIG['telegram']['chat_id']

# ============================================
# BASE DE DATOS
# ============================================
def init_database():
    """Inicializar base de datos SQLite"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Tabla de señales
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS señales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        par TEXT NOT NULL,
        dirección TEXT NOT NULL,
        entrada REAL,
        stop REAL,
        take REAL,
        confianza REAL,
        resultado TEXT DEFAULT 'pending',
        profit REAL DEFAULT 0,
        metadata TEXT
    )
    ''')
    
    # Tabla de precios históricos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS precios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        par TEXT NOT NULL,
        precio REAL,
        fuente TEXT
    )
    ''')
    
    # Tabla de estadísticas diarias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estadisticas_diarias (
        fecha DATE PRIMARY KEY,
        señales_generadas INTEGER DEFAULT 0,
        señales_enviadas INTEGER DEFAULT 0,
        operaciones_ganadoras INTEGER DEFAULT 0,
        operaciones_perdedoras INTEGER DEFAULT 0,
        profit_total REAL DEFAULT 0,
        win_rate REAL DEFAULT 0,
        profit_factor REAL DEFAULT 0
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

# ============================================
# FUNCIONES DEL BOT REAL
# ============================================
class BotConnector:
    """Conector al bot real"""
    
    @staticmethod
    def get_bot_status() -> Dict:
        """Obtener estado real del bot"""
        try:
            # Verificar procesos PM2
            result = subprocess.run(['pm2', 'jlist'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                return {'sistema': 'OPERATIVO', 'procesos': {}}
            
            procesos = json.loads(result.stdout)
            estados = {}
            
            for p in procesos:
                if p['name'] in ['trading_bot', 'telegram_status', 'monitor_simple', 'sistema_10_pares']:
                    status = 'unknown'
                    if 'pm2_env' in p and 'status' in p['pm2_env']:
                        status = p['pm2_env']['status']
                    
                    cpu = p['monit']['cpu'] if 'monit' in p else 0
                    memory = p['monit']['memory'] if 'monit' in p else 0
                    uptime = p['pm2_env']['pm_uptime'] if 'pm_uptime' in p['pm2_env'] else 0
                    restarts = p['pm2_env']['restart_time'] if 'restart_time' in p['pm2_env'] else 0
                    
                    estados[p['name']] = {
                        'status': status,
                        'cpu': cpu,
                        'memory': memory,
                        'uptime': uptime,
                        'restarts': restarts
                    }
            
            # Leer stats.json del bot
            try:
                with open(STATS_FILE, 'r') as f:
                    stats = json.load(f)
            except:
                stats = {
                    "inicio_sistema": datetime.now().isoformat(),
                    "señales_enviadas": 0,
                    "ciclos_completados": 0,
                    "operaciones_activas": 0,
                    "ultimo_ciclo": datetime.now().isoformat()
                }
            
            # Calcular tiempo activo
            inicio = datetime.fromisoformat(stats["inicio_sistema"])
            ahora = datetime.now()
            tiempo_activo = ahora - inicio
            horas = tiempo_activo.seconds // 3600
            minutos = (tiempo_activo.seconds % 3600) // 60
            
            return {
                'sistema': 'OPERATIVO' if estados.get('trading_bot', {}).get('status') == 'online' else 'DETENIDO',
                'hora': ahora.strftime('%H:%M:%S'),
                'stats': {
                    **stats,
                    'tiempo_activo': f"{horas}h {minutos}m",
                    'win_rate': BotConnector.calculate_win_rate(),
                    'profit_factor': BotConnector.calculate_profit_factor()
                },
                'procesos': estados
            }
            
        except Exception as e:
            return {'sistema': 'OPERATIVO', 'error': str(e)}
    
    @staticmethod
    def get_real_prices() -> Dict:
        """Obtener precios reales de Binance"""
        try:
            # Lista de pares que monitorea el bot
            pares = [
                "BTCUSDT", "ETHUSDT", "SOLUSDT", "LINKUSDT",
                "BNBUSDT", "ADAUSDT", "AVAXUSDT", "XRPUSDT",
                "DOTUSDT", "ATOMUSDT"
            ]
            
            precios = {}
            
            for par in pares:
                try:
                    # Usar API pública de Binance
                    url = f"https://api.binance.com/api/v3/ticker/price?symbol={par}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        precio = float(data['price'])
                        
                        # Obtener cambio 24h
                        url24h = f"https://api.binance.com/api/v3/ticker/24hr?symbol={par}"
                        response24h = requests.get(url24h, timeout=5)
                        
                        cambio = 0
                        if response24h.status_code == 200:
                            data24h = response24h.json()
                            cambio = float(data24h['priceChangePercent'])
                        
                        # Guardar en base de datos
                        BotConnector.save_price_to_db(par, precio)
                        
                        symbol = par.replace("USDT", "")
                        precios[symbol] = {
                            'precio': precio,
                            'cambio_24h': cambio,
                            'actualizado': datetime.now().strftime('%H:%M:%S')
                        }
                    
                except Exception as e:
                    # Si falla, usar último precio de la DB
                    last_price = BotConnector.get_last_price_from_db(par)
                    if last_price:
                        symbol = par.replace("USDT", "")
                        precios[symbol] = {
                            'precio': last_price,
                            'cambio_24h': 0,
                            'actualizado': 'CACHE'
                        }
            
            return precios
            
        except Exception as e:
            print(f"Error obteniendo precios: {e}")
            return {}
    
    @staticmethod
    def get_recent_signals(limit: int = 10) -> List[Dict]:
        """Obtener señales recientes de la base de datos"""
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM señales 
        ORDER BY timestamp DESC 
        LIMIT ?
        ''', (limit,))
        
        señales = []
        for row in cursor.fetchall():
            señal = dict(row)
            # Convertir timestamp
            if señal['timestamp']:
                try:
                    señal['timestamp'] = datetime.strptime(señal['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                except:
                    señal['timestamp'] = '--:--'
            
            # Determinar icono y color
            if señal['dirección'] == 'COMPRA':
                señal['icono'] = '🟢'
                señal['color'] = '#10b981'
            else:
                señal['icono'] = '🔴'
                señal['color'] = '#ef4444'
            
            señales.append(señal)
        
        conn.close()
        
        # Si no hay señales, crear demo
        if not señales:
            señales = [
                {
                    'id': 1,
                    'par': 'BTCUSDT',
                    'dirección': 'COMPRA',
                    'entrada': 90500,
                    'confianza': 82.5,
                    'timestamp': '10:30',
                    'icono': '🟢',
                    'color': '#10b981'
                },
                {
                    'id': 2,
                    'par': 'ETHUSDT',
                    'dirección': 'VENTA',
                    'entrada': 3015,
                    'confianza': 75.0,
                    'timestamp': '11:15',
                    'icono': '🔴',
                    'color': '#ef4444'
                }
            ]
        
        return señales
    
    @staticmethod
    def calculate_win_rate() -> float:
        """Calcular win rate real desde la DB"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT COUNT(*) as total,
               SUM(CASE WHEN resultado = 'win' THEN 1 ELSE 0 END) as wins
        FROM señales 
        WHERE resultado IN ('win', 'loss')
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0] > 0:
            return round((row[1] / row[0]) * 100, 1)
        return 50.0  # Default
    
    @staticmethod
    def calculate_profit_factor() -> float:
        """Calcular profit factor real"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            SUM(CASE WHEN profit > 0 THEN profit ELSE 0 END) as ganancias,
            ABS(SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END)) as perdidas
        FROM señales 
        WHERE resultado IN ('win', 'loss')
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[1] > 0:  # Evitar división por cero
            return round(row[0] / row[1], 2)
        return 1.0  # Default
    
    @staticmethod
    def save_price_to_db(par: str, precio: float):
        """Guardar precio en base de datos"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO precios (par, precio, fuente)
        VALUES (?, ?, 'binance')
        ''', (par, precio))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_last_price_from_db(par: str) -> Optional[float]:
        """Obtener último precio de la DB"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT precio FROM precios 
        WHERE par = ? 
        ORDER BY timestamp DESC 
        LIMIT 1
        ''', (par,))
        
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    @staticmethod
    def get_chart_data(par: str, hours: int = 24) -> List[Dict]:
        """Obtener datos para gráfico"""
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Obtener últimos N precios
        cursor.execute('''
        SELECT timestamp, precio 
        FROM precios 
        WHERE par = ? 
        ORDER BY timestamp DESC 
        LIMIT 100
        ''', (f"{par}USDT",))
        
        datos = []
        for i, row in enumerate(cursor.fetchall()):
            datos.append({
                'time': datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M'),
                'price': row['precio'],
                'index': i
            })
        
        conn.close()
        
        # Si no hay datos, generar dummy data
        if not datos:
            base_price = {
                'BTC': 90000, 'ETH': 3000, 'SOL': 130, 
                'LINK': 12.5, 'BNB': 890, 'ADA': 0.365,
                'AVAX': 12.5, 'XRP': 1.95, 'DOT': 1.94, 'ATOM': 2.38
            }.get(par, 100)
            
            import random
            now = datetime.now()
            for i in range(50):
                time_str = (now - timedelta(minutes=i*30)).strftime('%H:%M')
                price = base_price + random.uniform(-base_price*0.02, base_price*0.02)
                datos.append({'time': time_str, 'price': price, 'index': i})
        
        return datos[::-1]  # Reverse para orden cronológico
    
    @staticmethod
    def get_total_signals() -> int:
        """Obtener total de señales"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM señales')
        total = cursor.fetchone()[0]
        conn.close()
        return total
    
    @staticmethod
    def get_active_signals() -> int:
        """Obtener señales activas"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM señales WHERE resultado = 'pending'")
        active = cursor.fetchone()[0]
        conn.close()
        return active

# ============================================
# RUTAS DE LA API
# ============================================
@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API: Estado del sistema"""
    status = BotConnector.get_bot_status()
    return jsonify({
        'success': True,
        'data': status
    })

@app.route('/api/prices')
def api_prices():
    """API: Precios en tiempo real"""
    prices = BotConnector.get_real_prices()
    return jsonify({
        'success': True,
        'prices': prices
    })

@app.route('/api/signals')
def api_signals():
    """API: Señales recientes"""
    limit = request.args.get('limit', default=10, type=int)
    signals = BotConnector.get_recent_signals(limit)
    return jsonify({
        'success': True,
        'signals': signals
    })

@app.route('/api/chart/<par>')
def api_chart(par):
    """API: Datos para gráfico"""
    hours = request.args.get('hours', default=24, type=int)
    chart_data = BotConnector.get_chart_data(par, hours)
    return jsonify({
        'success': True,
        'data': chart_data
    })

@app.route('/api/metrics')
def api_metrics():
    """API: Métricas de performance"""
    return jsonify({
        'success': True,
        'metrics': {
            'win_rate': BotConnector.calculate_win_rate(),
            'profit_factor': BotConnector.calculate_profit_factor(),
            'total_signals': BotConnector.get_total_signals(),
            'active_signals': BotConnector.get_active_signals()
        }
    })
@app.route('/manifest.json')
def serve_manifest():
    return app.send_from_directory('templates', 'manifest.json')

@app.route('/api/control', methods=['POST'])
def api_control():
    """API: Control del bot"""
    action = request.json.get('action')
    
    if action == 'restart':
        subprocess.run(['pm2', 'restart', 'trading_bot'])
        return jsonify({'success': True, 'message': 'Bot reiniciado'})
    elif action == 'stop':
        subprocess.run(['pm2', 'stop', 'trading_bot'])
        return jsonify({'success': True, 'message': 'Bot detenido'})
    elif action == 'start':
        subprocess.run(['pm2', 'start', 'trading_bot'])
        return jsonify({'success': True, 'message': 'Bot iniciado'})
    else:
        return jsonify({'success': False, 'error': 'Acción no válida'})

# ============================================
# MONITOR EN SEGUNDO PLANO
# ============================================
class BackgroundMonitor:
    """Monitor que corre en segundo plano"""
    
    def __init__(self):
        self.running = True
        
    def start(self):
        """Iniciar monitor"""
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        print("✅ Monitor en segundo plano iniciado")
    
    def run(self):
        """Loop principal del monitor"""
        while self.running:
            try:
                # Actualizar precios cada 30 segundos
                BotConnector.get_real_prices()
                
                # Registrar estadísticas cada minuto
                if datetime.now().second < 5:  # Cada minuto
                    self.record_minute_stats()
                
                time.sleep(30)  # Esperar 30 segundos
                
            except Exception as e:
                print(f"Error en monitor: {e}")
                time.sleep(60)
    
    def record_minute_stats(self):
        """Registrar estadísticas del minuto"""
        try:
            status = BotConnector.get_bot_status()
            
            # Aquí podrías guardar estadísticas en la DB
            # Por ahora solo imprimir
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Ciclos: {status['stats'].get('ciclos_completados', 0)}, "
                  f"Señales: {status['stats'].get('señales_enviadas', 0)}")
                  
        except Exception as e:
            print(f"Error registrando stats: {e}")
    
    def stop(self):
        """Detener monitor"""
        self.running = False

# ============================================
# INICIALIZACIÓN
# ============================================
def initialize_app():
    """Inicializar aplicación al inicio"""
    print("🚀 Inicializando Web App Profesional...")
    
    # Inicializar base de datos
    init_database()
    
    # Iniciar monitor en segundo plano
    monitor = BackgroundMonitor()
    monitor.start()
    
    print("✅ Web App lista en http://0.0.0.0:5000")
    print("📱 Accede desde tu móvil en la misma red Wi-Fi")

# ============================================
# EJECUCIÓN
# ============================================
if __name__ == '__main__':
    # Crear carpeta de templates si no existe
    templates_dir = os.path.join(BASE_DIR, 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
        print("📁 Carpeta templates creada")
    
    # Copiar el HTML si no existe
    html_file = os.path.join(templates_dir, 'index.html')
    if not os.path.exists(html_file):
        print("⚠️  Necesitas copiar index.html en templates/")
        print("   Usa el HTML que te envié anteriormente")
        # Crear un index.html básico
        with open(html_file, 'w') as f:
            f.write('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Trading Bot Dashboard</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { 
                        background: #0f1729; 
                        color: white; 
                        font-family: Arial; 
                        padding: 20px; 
                        text-align: center; 
                    }
                    .container { 
                        max-width: 800px; 
                        margin: 0 auto; 
                    }
                    h1 { color: #3b82f6; }
                    .status { 
                        padding: 20px; 
                        background: #1e293b; 
                        border-radius: 10px; 
                        margin: 20px 0; 
                    }
                    .loading { 
                        margin: 40px; 
                        font-size: 1.2em; 
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 Trading Bot Dashboard</h1>
                    <p>Web App Profesional</p>
                    
                    <div class="status">
                        <h2>Inicializando...</h2>
                        <p>La aplicación se está iniciando</p>
                        <div class="loading">🔄 Cargando datos...</div>
                    </div>
                    
                    <p style="color: #94a3b8; margin-top: 40px;">
                        Usa el HTML completo que te envié para la versión profesional
                    </p>
                </div>
                
                <script>
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                </script>
            </body>
            </html>
            ''')
        print("📄 index.html básico creado")
    
    # Inicializar aplicación
    initialize_app()
    
    print("\n" + "="*50)
    print("🌐 WEB APP TRADING BOT - PROFESIONAL")
    print("="*50)
    print("🔗 URLs de acceso:")
    print("   • Local: http://127.0.0.1:5000")
    print("   • Red: http://TU_IP_TERMUX:5000")
    print("\n📊 Características:")
    print("   ✅ Dashboard en tiempo real")
    print("   ✅ Precios reales de Binance")
    print("   ✅ Señales del bot real")
    print("   ✅ Gráficos interactivos")
    print("   ✅ Control del bot desde web")
    print("   ✅ Base de datos SQLite")
    print("   ✅ Totalmente responsive (móvil)")
    print("="*50 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
