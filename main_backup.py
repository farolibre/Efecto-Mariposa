from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Archivos de datos
DATA_FILE = 'data.json'
HISTORIAL_FILE = 'historial.json'

# Asegurarse de que los archivos existan
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(HISTORIAL_FILE):
    with open(HISTORIAL_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/datos')
def get_datos():
    """Obtener todos los datos"""
    with open(DATA_FILE, 'r') as f:
        datos = json.load(f)
    return jsonify(datos)

@app.route('/api/datos', methods=['POST'])
def add_dato():
    """Añadir un nuevo dato"""
    nuevo_dato = request.json
    with open(DATA_FILE, 'r') as f:
        datos = json.load(f)
    
    # Añadir timestamp
    nuevo_dato['fecha'] = datetime.now().isoformat()
    datos.append(nuevo_dato)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(datos, f, indent=2)
    
    return jsonify({'success': True, 'mensaje': 'Dato guardado'})

@app.route('/api/historial')
def get_historial():
    """Obtener historial"""
    with open(HISTORIAL_FILE, 'r') as f:
        historial = json.load(f)
    return jsonify(historial)

@app.route('/api/historial', methods=['POST'])
def add_historial():
    """Añadir al historial"""
    entrada = request.json
    entrada['fecha'] = datetime.now().isoformat()
    
    with open(HISTORIAL_FILE, 'r') as f:
        historial = json.load(f)
    
    historial.append(entrada)
    
    with open(HISTORIAL_FILE, 'w') as f:
        json.dump(historial, f, indent=2)
    
    return jsonify({'success': True, 'mensaje': 'Historial actualizado'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)