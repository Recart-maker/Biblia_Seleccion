import json
from flask import Flask, render_template, request, jsonify
import random
import unicodedata
import os
import re
from urllib.parse import unquote

# --- 1. Inicialización de la Aplicación Flask (¡SOLO UNA VEZ!) ---
app = Flask(__name__)

# --- 2. Configuraciones (opcional, pero buena práctica) ---
# app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui' # Descomenta y cambia por una clave fuerte si usas sesiones o formularios

# --- 3. Definición de la ruta base para los archivos de datos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 4. Carga de los archivos JSON (¡SOLO UNA VEZ!) ---
# Cargar la Biblia completa con versículos
try:
    with open(os.path.join(BASE_DIR, 'biblia.json'), 'r', encoding='utf-8') as f:
        biblia = json.load(f)
    print("biblia.json cargado exitosamente.")
    if 'biblia_data' in biblia:
        print(f"Libros encontrados en biblia.json: {list(biblia['biblia_data'].keys())}")
    else:
        print("Advertencia: 'biblia_data' no encontrada como clave principal en biblia.json.")
except FileNotFoundError:
    print(f"Error: 'biblia.json' no encontrado en '{BASE_DIR}'. Asegúrate de que esté en la misma carpeta que 'app.py'.")
    biblia = {} # Cargar un diccionario vacío para evitar errores posteriores
except json.JSONDecodeError:
    print("Error: 'biblia.json' contiene un JSON inválido. Revisa su formato.")
    biblia = {}

# Cargar los resúmenes de los libros
try:
    with open(os.path.join(BASE_DIR, 'resumen_libros.json'), 'r', encoding='utf-8') as f:
        resumenes_libros = json.load(f)
    print("resumen_libros.json cargado exitosamente.")
except FileNotFoundError:
    print(f"Error: 'resumen_libros.json' no encontrado en '{BASE_DIR}'. Asegúrate de que esté en la misma carpeta que 'app.py'.")
    resumenes_libros = {}
except json.JSONDecodeError:
    print("Error: 'resumen_libros.json' contiene un JSON inválido. Revisa su formato.")
    resumenes_libros = {}

# --- 5. Función para normalizar texto (utilizada en la búsqueda) ---
def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Normalizar para quitar acentos y otros caracteres diacríticos
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Puedes añadir más limpieza, por ejemplo, quitar puntuación si no la quieres en la búsqueda
    # text = re.sub(r'[^\w\s]', '', text)
    return text

# --- 6. Definición de todas las Rutas de la Aplicación ---

@app.route('/')
def index():
    versiculo_aleatorio_texto = "¡Bienvenido a tu Biblia App! Navega para empezar."
    versiculo_aleatorio_referencia = ""

    biblia_data_contenido = biblia.get('biblia_data', {})

    if biblia_data_contenido:
        libros_disponibles = [nombre for nombre in biblia_data_contenido.keys() if nombre != 'info']
        if libros_disponibles:
            libro_elegido_nombre = random.choice(libros_disponibles)
            libro_elegido_data = biblia_data_contenido.get(libro_elegido_nombre, {})

            capitulos_disponibles = [cap for cap in libro_elegido_data.keys() if cap != 'info']
            if capitulos_disponibles:
                capitulo_elegido_num = random.choice(capitulos_disponibles)
                versiculos_capitulo = libro_elegido_data.get(capitulo_elegido_num, {})

                versiculos_nums = [v_num for v_num in versiculos_capitulo.keys()]
                if versiculos_nums:
                    versiculo_elegido_num = random.choice(versiculos_nums)
                    versiculo_aleatorio_texto = versiculos_capitulo.get(versiculo_elegido_num)
                    versiculo_aleatorio_referencia = f"{libro_elegido_nombre} {capitulo_elegido_num}:{versiculo_elegido_num}"

    return render_template('index.html',
                           portada_versiculo=versiculo_aleatorio_texto,
                           portada_referencia=versiculo_aleatorio_referencia,
                           libros=biblia_data_contenido.keys(),
                           resumenes_libros=resumenes_libros)

@app.route('/libros')
def lista_libros():
    nombres_libros = biblia.get('biblia_data', {}).keys()
    libros_ordenados = sorted(nombres_libros)
    return render_template('libros.html', libros=libros_ordenados, resumenes_libros=resumenes_libros)

#
    
    # RUTA PARA VER UN LIBRO Y LISTAR SUS CAPÍTULOS (CONSOLIDADA)
@app.route('/libro/<nombre_libro>')
def ver_libro(nombre_libro):
    # *** AÑADE ESTA LÍNEA PARA DECODIFICAR EL NOMBRE DEL LIBRO ***
    nombre_libro_decodificado = unquote(nombre_libro)

    # Obtener los datos del libro específico desde 'biblia_data'
    # *** USA EL NOMBRE DECODIFICADO AQUÍ ***
    libro_data = biblia.get('biblia_data', {}).get(nombre_libro_decodificado, None)

    # --- INICIO DE LÍNEAS DE DEPURACIÓN ---
    # *** ACTUALIZA TUS PRINTS PARA MOSTRAR EL NOMBRE DECODIFICADO ***
    print(f"DEBUG: Nombre del libro recibido en la URL (original): '{nombre_libro}'")
    print(f"DEBUG: Nombre del libro decodificado: '{nombre_libro_decodificado}'")
    if 'biblia_data' in biblia:
        nombres_de_libros_cargados = list(biblia['biblia_data'].keys())
        print(f"DEBUG: Nombres de libros cargados en biblia.json: {nombres_de_libros_cargados}")
        # *** USA EL NOMBRE DECODIFICADO PARA LA COMPARACIÓN ***
        if nombre_libro_decodificado in nombres_de_libros_cargados:
            print(f"DEBUG: ¡El libro '{nombre_libro_decodificado}' SÍ se encuentra entre los cargados!")
        else:
            print(f"DEBUG: El libro '{nombre_libro_decodificado}' NO se encuentra entre los cargados.")
    else:
        print("DEBUG: 'biblia_data' no está presente en el diccionario 'biblia'.")
    # --- FIN DE LÍNEAS DE DEPURACIÓN ---

    if libro_data:
        capitulos = [cap for cap in libro_data.keys() if cap != 'info']
        capitulos_ordenados = sorted(capitulos, key=int)

        resumen = resumenes_libros.get(nombre_libro_decodificado, "Resumen no disponible.") # *** USA EL NOMBRE DECODIFICADO AQUÍ ***

        return render_template('ver_libro.html',
                               libro_nombre=nombre_libro_decodificado, # *** PASA EL NOMBRE DECODIFICADO A LA PLANTILLA ***
                               capitulos=capitulos_ordenados,
                               resumen=resumen)
    else:
        # Devuelve un error 404 si el libro no existe en biblia_data
        return render_template('error.html', mensaje=f"Lo siento, el libro '{nombre_libro_decodificado}' no fue encontrado."), 404 # *** USA EL NOMBRE DECODIFICADO AQUÍ ***

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').strip()
    resultados = []

    if query:
        query_normalized = normalize_text(query)
        print(f"Buscando el término normalizado: '{query_normalized}'")

        for libro_nombre, libro_contenido in biblia.get('biblia_data', {}).items():
            if libro_nombre == 'info':
                continue

            for num_capitulo, capitulo_versiculos in libro_contenido.items():
                if num_capitulo == 'info':
                    continue

                for num_versiculo, texto_versiculo in capitulo_versiculos.items():
                    texto_normalized = normalize_text(texto_versiculo)

                    if query_normalized in texto_normalized:
                        resultados.append({
                            'libro': libro_nombre,
                            'capitulo': num_capitulo,
                            'versiculo_num': num_versiculo,
                            'texto': texto_versiculo
                        })
        print(f"Se encontraron {len(resultados)} resultados.")

    resultados_ordenados = sorted(resultados, key=lambda x: (x['libro'], int(x['capitulo']), int(x['versiculo_num'])))

    return render_template('resultados_busqueda.html',
                           query=query,
                           resultados=resultados_ordenados)

@app.route('/favoritos')
def mostrar_favoritos():
    return render_template('favoritos.html')

# --- 7. Ejecutar la Aplicación ---
if __name__ == '__main__':
    app.run(debug=True)