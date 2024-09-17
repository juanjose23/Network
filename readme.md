# Projects 4 network

## Descripción

Este proyecto es una red social simple que permite a los usuarios:
- Crear nuevas publicaciones.
- Ver todas las publicaciones.
- Ver perfiles de usuarios.
- Seguir/dejar de seguir a otros usuarios.
- Ver publicaciones de usuarios seguidos.
- Editar sus propias publicaciones.
- Dar "me gusta" o "no me gusta" a publicaciones.

La aplicación está construida usando Python (Django), JavaScript, HTML y CSS.

## Funcionalidades

### 1. Nueva Publicación

- **Descripción**: Los usuarios que han iniciado sesión pueden crear nuevas publicaciones ingresando texto en un área de texto y haciendo clic en un botón para enviar la publicación.
- **Implementación**: Los usuarios pueden hacer nuevas publicaciones desde un formulario ubicado en la página principal o en una página separada.

### 2. Ver Todas las Publicaciones

- **Descripción**: Los usuarios pueden ver todas las publicaciones de todos los usuarios, ordenadas por las más recientes primero.
- **Implementación**: Las publicaciones se muestran en una página con paginación. Cada publicación muestra el nombre de usuario, el contenido, la fecha y hora de la publicación, y el número de "me gusta".

### 3. Página de Perfil

- **Descripción**: Los usuarios pueden ver la página de perfil de otros usuarios, que muestra:
  - Número de seguidores.
  - Número de personas a las que sigue.
  - Todas las publicaciones de ese usuario, en orden cronológico inverso.
  - Un botón de "Seguir" o "Dejar de seguir" si el usuario no está viendo su propio perfil.
- **Implementación**: Al hacer clic en un nombre de usuario se accede a su página de perfil.

### 4. Seguir

- **Descripción**: Los usuarios pueden ver publicaciones de los usuarios que siguen.
- **Implementación**: Una página de "Siguiendo" muestra publicaciones de los usuarios seguidos solamente, con paginación.

### 5. Paginación

- **Descripción**: Las publicaciones están paginadas para mostrar 10 publicaciones por página, con botones de "Siguiente" y "Anterior" para navegar entre páginas.
- **Implementación**: Los controles de paginación aparecen si hay más de 10 publicaciones.

### 6. Editar Publicación

- **Descripción**: Los usuarios pueden editar sus propias publicaciones usando un modal con un área de texto. Los cambios se guardan de forma asincrónica.
- **Implementación**: Los usuarios pueden hacer clic en un botón "Editar" en sus propias publicaciones para abrir un modal, editar el contenido y guardar los cambios sin recargar la página.

### 7. Dar "Me Gusta"/"No Me Gusta"

- **Descripción**: Los usuarios pueden alternar los "me gusta" en las publicaciones.
- **Implementación**: Los usuarios pueden hacer clic en un botón de "Me gusta" o "No me gusta", y el recuento de "me gusta" se actualiza de forma asincrónica.

## Tecnologías Utilizadas

- **Backend**: Python con Django
- **Frontend**: HTML, CSS, JavaScript
- **Base de Datos**: SQLite (o cualquier otra base de datos preferida)
- **AJAX**: Para solicitudes asincrónicas

## Instalación

1. **Clonar el Repositorio**

    ```bash
    git clone https://github.com/tuusuario/red-social.git
    cd red-social
    ```

2. **Configurar el Entorno Virtual**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instalar Dependencias**

    ```bash
    pip install -r requirements.txt
    ```

4. **Aplicar Migraciones**

    ```bash
    python manage.py migrate
    ```
5. **Ejecutar el Servidor de Desarrollo**

    ```bash
    python manage.py runserver
    ```

6. **Acceder a la Aplicación**

    Abre un navegador web y navega a `http://127.0.0.1:8000/`.

## Uso

1. **Crear una Nueva Publicación**: Usa el formulario para enviar nuevas publicaciones.
2. **Ver Todas las Publicaciones**: Haz clic en "Todas las publicaciones" para ver un feed de todas las publicaciones.
3. **Ver Perfil**: Haz clic en un nombre de usuario para visitar su página de perfil.
4. **Seguir/Dejar de Seguir**: Alterna el estado de seguimiento desde la página de perfil de un usuario.
5. **Ver Publicaciones de Seguidos**: Accede a la página de "Siguiendo" para ver publicaciones de los usuarios que sigues.
6. **Editar Publicaciones**: Haz clic en "Editar" en tus publicaciones para modificar y guardar cambios.
7. **Dar "Me Gusta"/"No Me Gusta"**: Usa el botón de "Me gusta" para dar o quitar "me gusta" a publicaciones.

## Contribuciones

Siéntete libre de bifurcar el repositorio y enviar solicitudes de extracción para mejoras o correcciones de errores.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
