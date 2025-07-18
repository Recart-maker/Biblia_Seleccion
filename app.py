import json
from flask import Flask, render_template, request, jsonify
import random
import unicodedata # <--- ¡Añade esta línea!

# Función para normalizar texto (quitar acentos y convertir a minúsculas)
def normalize_text(text):
    if not isinstance(text, str): # Asegurarse de que sea una cadena
        return ""
    # Convertir a minúsculas
    text = text.lower()
    # Normalizar para quitar acentos
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Puedes añadir más limpieza si es necesario (ej. quitar puntuación, espacios extra)
    # text = re.sub(r'[^\w\s]', '', text) # Para quitar puntuación (requiere import re)
    return text

app = Flask(__name__)

# Cargar la Biblia completa con versículos
try:
    with open('biblia.json', 'r', encoding='utf-8') as f:
        biblia = json.load(f)
        print(biblia.keys())
except FileNotFoundError:
    print("Error: 'biblia.json' no encontrado. Asegúrate de que esté en la misma carpeta que 'app.py'.")
    biblia = {} # Cargar un diccionario vacío para evitar errores en la app
except json.JSONDecodeError:
    print("Error: 'biblia.json' contiene un JSON inválido. Revisa su formato.")
    biblia = {}

# Cargar los resúmenes de los libros
try:
    with open('resumen_libros.json', 'r', encoding='utf-8') as f:
        resumenes_libros = json.load(f)
except FileNotFoundError:
    print("Error: 'resumen_libros.json' no encontrado. Asegúrate de que esté en la misma carpeta que 'app.py'.")
    resumenes_libros = {}
except json.JSONDecodeError:
    print("Error: 'resumen_libros.json' contiene un JSON inválido. Revisa su formato.")
    resumenes_libros = {}




@app.route('/')
def index():
    # --- Lógica para seleccionar un versículo aleatorio ---
    versiculo_aleatorio_texto = "¡Bienvenido a tu Biblia App! Navega para empezar." # Versículo por defecto
    versiculo_aleatorio_referencia = ""

    biblia_data_contenido = biblia.get('biblia_data', {})

    if biblia_data_contenido:
        libros_disponibles = [nombre for nombre in biblia_data_contenido.keys() if nombre != 'info']
        if libros_disponibles:
            # Seleccionar un libro al azar
            libro_elegido_nombre = random.choice(libros_disponibles)
            libro_elegido_data = biblia_data_contenido.get(libro_elegido_nombre, {})

            capitulos_disponibles = [cap for cap in libro_elegido_data.keys() if cap != 'info']
            if capitulos_disponibles:
                # Seleccionar un capítulo al azar
                capitulo_elegido_num = random.choice(capitulos_disponibles)
                versiculos_capitulo = libro_elegido_data.get(capitulo_elegido_num, {})

                versiculos_nums = [v_num for v_num in versiculos_capitulo.keys()]
                if versiculos_nums:
                    # Seleccionar un versículo al azar
                    versiculo_elegido_num = random.choice(versiculos_nums)
                    versiculo_aleatorio_texto = versiculos_capitulo.get(versiculo_elegido_num)
                    versiculo_aleatorio_referencia = f"{libro_elegido_nombre} {capitulo_elegido_num}:{versiculo_elegido_num}"
    # --- FIN Lógica para versículo aleatorio ---

    return render_template('index.html',
                           portada_versiculo=versiculo_aleatorio_texto,
                           portada_referencia=versiculo_aleatorio_referencia, # <--- Pasa también la referencia
                           libros=biblia_data_contenido.keys(), # Puedes seguir usando biblia.keys() para la lista de nombres
                           resumenes_libros=resumenes_libros)


    
@app.route('/libros')
def lista_libros():
    # Acceder a los nombres de los libros desde 'biblia_data'
    nombres_libros = biblia.get('biblia_data', {}).keys()
    
    # Ordenar los libros alfabéticamente si lo deseas
    libros_ordenados = sorted(nombres_libros)
    return render_template('libros.html', libros=libros_ordenados, resumenes_libros=resumenes_libros)

@app.route('/libro/<nombre_libro>')
def ver_libro(nombre_libro):
    # Obtener los datos del libro específico desde 'biblia_data'
    libro_data = biblia.get('biblia_data', {}).get(nombre_libro, None)

    if libro_data:
        # Los capítulos son las claves del diccionario de libro_data (excluyendo 'info')
        capitulos = [cap for cap in libro_data.keys() if cap != 'info']
        capitulos_ordenados = sorted(capitulos, key=int) # Ordenar capítulos numéricamente

        # Obtener el resumen del libro para mostrarlo también
        resumen = resumenes_libros.get(nombre_libro, "Resumen no disponible.")

        return render_template('ver_libro.html',
                               libro_nombre=nombre_libro,
                               capitulos=capitulos_ordenados,
                               resumen=resumen)
    else:
        return "Libro no encontrado.", 404 # Si el libro no existe, devuelve un error 404
    
@app.route('/libro/<nombre_libro>/capitulo/<int:num_capitulo>')
def ver_capitulo(nombre_libro, num_capitulo):
    # Obtener los datos del libro específico
    libro_data = biblia.get('biblia_data', {}).get(nombre_libro, None)

    if libro_data:
        # Obtener los versículos del capítulo específico
        # Convertimos num_capitulo a string porque las claves en JSON son strings
        versiculos = libro_data.get(str(num_capitulo), None)

        if versiculos:
            # Obtener el número total de capítulos para la navegación
            todos_los_capitulos = [cap for cap in libro_data.keys() if cap != 'info']
            total_capitulos = sorted(todos_los_capitulos, key=int)

            # Encontrar el índice del capítulo actual para calcular anterior/siguiente
            try:
                indice_actual = total_capitulos.index(str(num_capitulo))
                capitulo_anterior = total_capitulos[indice_actual - 1] if indice_actual > 0 else None
                capitulo_siguiente = total_capitulos[indice_actual + 1] if indice_actual < len(total_capitulos) - 1 else None
            except ValueError:
                capitulo_anterior = None
                capitulo_siguiente = None # El capítulo actual no se encontró en la lista ordenada, lo cual es inusual

            return render_template('ver_capitulo.html',
                                   libro_nombre=nombre_libro,
                                   num_capitulo=num_capitulo,
                                   versiculos=versiculos,
                                   capitulo_anterior=capitulo_anterior,
                                   capitulo_siguiente=capitulo_siguiente,
                                   total_capitulos=total_capitulos) # Pasar la lista completa de capítulos

        else:
            return "Capítulo no encontrado.", 404
    else:
        return "Libro no encontrado.", 404
    
# ... (tu código anterior)

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').strip()
    resultados = []

    if query:
        # Normalizar el término de búsqueda
        query_normalized = normalize_text(query)

        # --- DEBUG: Puedes imprimir esto para ver qué está buscando ---
        print(f"Buscando el término normalizado: '{query_normalized}'")
        # --- FIN DEBUG ---

        for libro_nombre, libro_contenido in biblia.get('biblia_data', {}).items():
            if libro_nombre == 'info':
                continue

            for num_capitulo, capitulo_versiculos in libro_contenido.items():
                if num_capitulo == 'info':
                    continue

                for num_versiculo, texto_versiculo in capitulo_versiculos.items():
                    # Normalizar el texto del versículo para la comparación
                    texto_normalized = normalize_text(texto_versiculo)

                    if query_normalized in texto_normalized:
                        resultados.append({
                            'libro': libro_nombre,
                            'capitulo': num_capitulo,
                            'versiculo_num': num_versiculo,
                            'texto': texto_versiculo # Guardar el texto original para mostrar
                        })

        # --- DEBUG: Puedes imprimir esto para ver qué resultados se encuentran ---
        print(f"Se encontraron {len(resultados)} resultados.")
        # --- FIN DEBUG ---

    resultados_ordenados = sorted(resultados, key=lambda x: (x['libro'], int(x['capitulo']), int(x['versiculo_num'])))

    return render_template('resultados_busqueda.html',
                           query=query, # Pasar el query original para mostrar
                           resultados=resultados_ordenados)
    


@app.route('/favoritos')
def mostrar_favoritos():
    return render_template('favoritos.html')




if __name__ == '__main__':
 app.run(debug=True)