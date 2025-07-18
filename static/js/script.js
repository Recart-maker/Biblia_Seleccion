document.addEventListener('DOMContentLoaded', () => {
    const favoriteButtons = document.querySelectorAll('.favorite-button');
    const versiculoItems = document.querySelectorAll('.versiculo-item');

    // Función para obtener los favoritos de localStorage
    function getFavorites() {
        const favorites = localStorage.getItem('bibleFavorites');
        return favorites ? JSON.parse(favorites) : {};
    }

    // Función para guardar los favoritos en localStorage
    function saveFavorites(favorites) {
        localStorage.setItem('bibleFavorites', JSON.stringify(favorites));
    }

    // Función para generar una clave única para cada versículo
    function getVerseKey(libro, capitulo, versiculo) {
        return `${libro}|${capitulo}|${versiculo}`;
    }

    // Función para actualizar el estado visual del botón de favorito
    function updateFavoriteButtonState(button, isFavorite) {
        if (isFavorite) {
            button.textContent = '❤️'; // Corazón lleno
            button.classList.add('is-favorite');
            button.setAttribute('aria-label', 'Eliminar de favoritos');
        } else {
            button.textContent = '⭐'; // Estrella vacía
            button.classList.remove('is-favorite');
            button.setAttribute('aria-label', 'Añadir a favoritos');
        }
    }

    // Inicializar el estado de los botones al cargar la página
    versiculoItems.forEach(item => {
        const libro = item.dataset.libro;
        const capitulo = item.dataset.capitulo;
        const versiculo = item.dataset.versiculo;
        const key = getVerseKey(libro, capitulo, versiculo);
        const favorites = getFavorites();
        const button = item.querySelector('.favorite-button');

        if (button) {
            updateFavoriteButtonState(button, favorites[key]);
        }
    });

    // Añadir el evento click a cada botón de favorito
    favoriteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation(); // Evitar que el click se propague a otros elementos si los hubiera
            const item = event.target.closest('.versiculo-item');
            if (!item) return; // Asegurarse de que el elemento padre exista

            const libro = item.dataset.libro;
            const capitulo = item.dataset.capitulo;
            const versiculo = item.dataset.versiculo;
            const key = getVerseKey(libro, capitulo, versiculo);

            let favorites = getFavorites();

            if (favorites[key]) {
                // Si ya es favorito, lo eliminamos
                delete favorites[key];
                updateFavoriteButtonState(button, false);
                console.log(`Versículo ${key} eliminado de favoritos.`);
            } else {
                // Si no es favorito, lo añadimos
                favorites[key] = {
                    libro: libro,
                    capitulo: capitulo,
                    versiculo: versiculo,
                    texto: item.textContent.trim().split('. ')[1] // Capturar solo el texto del versículo
                };
                updateFavoriteButtonState(button, true);
                console.log(`Versículo ${key} añadido a favoritos.`);
            }
            saveFavorites(favorites);
        });
    });

    // ... (Todo el código existente de favoritos, getFavorites, saveFavorites, etc. dentro del DOMContentLoaded) ...

    // --- Funcionalidad para mostrar los favoritos en la página /favoritos ---
    if (window.location.pathname === '/favoritos') {
        const favoritesDisplay = document.getElementById('favorites-list');
        const noFavoritesMessage = document.getElementById('no-favoritos-message');
        const clearFavoritesBtn = document.getElementById('clear-favorites-btn');
        const allFavorites = getFavorites(); // Reutilizamos la función getFavorites()

        function renderFavorites() {
            // Limpiar la lista actual
            favoritesDisplay.innerHTML = ''; 

            const favKeys = Object.keys(allFavorites);

            if (favKeys.length === 0) {
                noFavoritesMessage.style.display = 'block'; // Mostrar mensaje si no hay favoritos
                clearFavoritesBtn.style.display = 'none'; // Ocultar botón de limpiar
            } else {
                noFavoritesMessage.style.display = 'none'; // Ocultar mensaje si hay favoritos
                clearFavoritesBtn.style.display = 'block'; // Mostrar botón de limpiar
                
                // Convertir el objeto de favoritos en un array y ordenar por libro, capítulo, versículo
                const sortedFavorites = favKeys.map(key => allFavorites[key]).sort((a, b) => {
                    // Criterio de ordenación: primero por libro, luego por capítulo, luego por versículo
                    if (a.libro !== b.libro) {
                        return a.libro.localeCompare(b.libro); // Ordenar alfabéticamente por libro
                    }
                    if (parseInt(a.capitulo) !== parseInt(b.capitulo)) {
                        return parseInt(a.capitulo) - parseInt(b.capitulo); // Ordenar numéricamente por capítulo
                    }
                    return parseInt(a.versiculo) - parseInt(b.versiculo); // Ordenar numéricamente por versículo
                });

                sortedFavorites.forEach(fav => {
                    const p = document.createElement('p');
                    p.classList.add('favorite-verse-item'); // Añadir una clase para estilizar
                    p.innerHTML = `<a href="/libro/${fav.libro}/capitulo/${fav.capitulo}"><strong>${fav.libro} ${fav.capitulo}:${fav.versiculo}.</strong></a> ${fav.texto}`;
                    
                    // Añadir un botón para eliminar el favorito individualmente
                    const deleteButton = document.createElement('span');
                    deleteButton.classList.add('delete-favorite-button');
                    deleteButton.textContent = '❌'; // Icono de X para eliminar
                    deleteButton.setAttribute('role', 'button');
                    deleteButton.setAttribute('aria-label', `Eliminar ${fav.libro} ${fav.capitulo}:${fav.versiculo} de favoritos`);
                    deleteButton.dataset.key = getVerseKey(fav.libro, fav.capitulo, fav.versiculo); // Guardar la clave del favorito
                    
                    deleteButton.addEventListener('click', () => {
                        let currentFavorites = getFavorites();
                        delete currentFavorites[deleteButton.dataset.key];
                        saveFavorites(currentFavorites);
                        // Re-renderizar la lista después de eliminar
                        Object.assign(allFavorites, currentFavorites); // Actualizar allFavorites
                        renderFavorites();
                    });

                    p.appendChild(deleteButton);
                    favoritesDisplay.appendChild(p);
                });
            }
        }

        // Cargar y mostrar favoritos al cargar la página
        renderFavorites();

        // Añadir el evento al botón de limpiar todos los favoritos
        clearFavoritesBtn.addEventListener('click', () => {
            if (confirm('¿Estás seguro de que quieres limpiar todos tus versículos favoritos?')) {
                localStorage.removeItem('bibleFavorites'); // Eliminar todos
                Object.assign(allFavorites, {}); // Vaciar allFavorites en memoria
                renderFavorites(); // Volver a renderizar (ahora estará vacío)
                console.log('Todos los favoritos han sido eliminados.');
            }
        });
    }
});
