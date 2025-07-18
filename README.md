# 📖 Mi Biblia App

Una aplicación web interactiva desarrollada con Flask que permite a los usuarios leer la Biblia, buscar versículos, guardar favoritos y compartir pasajes.

## ✨ Características

* **Navegación Completa:** Explora todos los libros, capítulos y versículos de la Biblia.
* **Versículo Aleatorio del Día:** Un versículo diferente aparece en la página de inicio en cada visita.
* **Funcionalidad de Búsqueda:** Busca palabras o frases específicas en toda la Biblia (soporta búsqueda insensible a acentos).
* **Versículos Favoritos:** Marca y guarda tus versículos preferidos para acceder a ellos rápidamente en una sección dedicada.
* **Compartir Versículos:** Copia el texto y la referencia de un versículo al portapapeles para compartirlo fácilmente.
* **Resúmenes de Libros:** Pequeños resúmenes de cada libro de la Biblia para una comprensión rápida.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, JavaScript
* **Gestión de Dependencias:** `pip`
* **Despliegue:** Vercel (opcional)

## 🚀 Configuración y Ejecución Local

Sigue estos pasos para poner la aplicación en marcha en tu máquina local:

### **Requisitos Previos**

Asegúrate de tener instalado:

* **Python 3.x**
* **pip** (el gestor de paquetes de Python)

### **Pasos**

1.  **Clona el Repositorio** (si lo tienes en Git) o descarga los archivos de tu proyecto:
    ```bash
    git clone [https://github.com/tu_usuario/tu_proyecto.git](https://github.com/tu_usuario/tu_proyecto.git)
    cd tu_proyecto
    ```
    (Reemplaza `https://github.com/tu_usuario/tu_proyecto.git` con la URL de tu repositorio si lo has subido a GitHub/GitLab/Bitbucket).

2.  **Instala las Dependencias:**
    Navega a la raíz de tu proyecto en la terminal y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```
    Asegúrate de tener un archivo `requirements.txt` en la raíz de tu proyecto con el contenido `Flask`.

3.  **Ejecuta la Aplicación:**
    Desde la raíz de tu proyecto en la terminal, ejecuta:
    ```bash
    python app.py
    ```
    La aplicación se iniciará en `http://127.0.0.1:5000/`.

## 🌐 Despliegue en Vercel (Opcional)

Esta aplicación puede ser fácilmente desplegada en Vercel. Asegúrate de tener los siguientes archivos en la raíz de tu proyecto antes de desplegar:

* `app.py`
* `requirements.txt` (con `Flask` dentro)
* `vercel.json` (con la configuración para Python/Flask)

**Contenido de `vercel.json` (ejemplo):**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}