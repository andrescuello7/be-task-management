# Invera ToDo-List Challenge

ToDo-List Challenge de Invera! Este proyecto es una aplicación web sencilla desarrollada con Python y Django que permite a los usuarios gestionar sus tareas. El objetivo principal es proporcionar una API robusta para la creación, lectura, actualización y eliminación de tareas, junto con funcionalidades de autenticación y filtrado.

## Tabla de Contenidos

1.  [Descripción del Proyecto](#descripción-del-proyecto)
2.  [Características](#características)
3.  [Tecnologías Utilizadas](#tecnologías-utilizadas)
4.  [Configuración del Entorno](#configuración-del-entorno)
    *   [Requisitos Previos](#requisitos-previos)
    *   [Instalación](#instalación)
    *   [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
    *   [Creación de Superusuario](#creación-de-superusuario)
    *   [Ejecutar el Servidor](#ejecutar-el-servidor)
5.  [Uso de la API](#uso-de-la-api)
    *   [Autenticación](#autenticación)
    *   [Endpoints de Tareas](#endpoints-de-tareas)
        *   [Listar y Crear Tareas](#listar-y-crear-tareas)
        *   [Obtener, Actualizar y Eliminar Tarea por ID](#obtener-actualizar-y-eliminar-tarea-por-id)
        *   [Marcar Tarea como Completada](#marcar-tarea-como-completada)
        *   [Filtrar Tareas](#filtrar-tareas)
6.  [Bonus Implementados](#bonus-implementados)
7.  [Estructura del Proyecto](#estructura-del-proyecto)
8.  [Consideraciones de Diseño](#consideraciones-de-diseño)
9.  [Pruebas](#pruebas)
10. [Contacto](#contacto)
11. [Agradecimientos](#agradecimientos)

---

## 1. Descripción del Proyecto

Este repositorio contiene la solución al Invera ToDo-List Challenge, una aplicación backend que expone una API RESTful para la gestión de tareas. La aplicación permite a los usuarios autenticarse, crear, listar, modificar y eliminar tareas, así como marcarlas como completadas y filtrarlas por diversos criterios.

## 2. Características

*   **Autenticación de Usuarios:** Registro e inicio de sesión seguro.
*   **Gestión de Tareas (CRUD):**
    *   Crear nuevas tareas.
    *   Ver todas las tareas existentes.
    *   Ver detalles de una tarea específica.
    *   Actualizar información de una tarea.
    *   Eliminar tareas.
*   **Marcar como Completada:** Funcionalidad para cambiar el estado de una tarea a "completada".
*   **Filtrado y Búsqueda:**
    *   Filtrar tareas por fecha de creación.
    *   Filtrar tareas por contenido (búsqueda parcial).

## 3. Tecnologías Utilizadas

*   **Python 3.9+**
*   **Django 4.2+**
*   **Django REST Framework:** Para construir la API RESTful.
*   **SQLite:** Base de datos por defecto para desarrollo.
*   **PostgreSQL:** (Opcional, si se configura para producción o Docker)
*   **`django-filter`**: Para facilitar el filtrado de tareas.
*   **`drf-yasg`**: (Opcional) Para generación de documentación Swagger/OpenAPI.

## 4. Configuración del Entorno

Sigue estos pasos para levantar la aplicación en tu entorno local.

### Requisitos Previos

Asegúrate de tener instalado lo siguiente:

*   **Python 3.9+**
*   **pip** (gestor de paquetes de Python)

### Instalación

1.  **Clona este repositorio:**
    ```bash
    git clone https://github.com/andrescuello7/invera-todo-challenge
    cd invera-todo-challenge
    ```

2.  **Crea y activa un entorno virtual:**
    Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las dependencias del proyecto:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuración de la Base de Datos

Por defecto, el proyecto utiliza SQLite. Si deseas usar PostgreSQL, configura tu `settings.py` apropiadamente.

1.  **Aplica las migraciones de la base de datos:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Ejecutar el Servidor

Una vez completados los pasos anteriores, puedes iniciar el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

La API estará disponible en `http://127.0.0.1:8000/`.

## 5. Uso de la API

La API está diseñada para ser intuitiva y sigue los principios RESTful. A continuación, se detallan los principales endpoints.

### Autenticación

Para interactuar con la mayoría de los endpoints de tareas, necesitarás un token de autenticación.

#### 1. Registro de Usuario

*   **Endpoint:** `/api/user/create`
*   **Método:** `POST`
*   **Body (JSON):**
    ```json
    {
       "username": "andy.rynki",
       "email": "andy.rynki@gmail.com",
       "password": "admin1",
       "firstname": "Andres",
       "lastname": "Rynkiewich"
    }
    ```
*   **Respuesta Exitosa (201 Created):**
    ```json
    {
       "id": 2,
       "username": "deb.rynki",
       "email": "deb.rynki@gmail.com",
       "firstname": "Debora",
       "lastname": "Rynkiewich",
       "created_at": "2025-09-25T23:53:52.418313Z"
    }
    ```

#### 2. Obtener Token (Authentication)

*   **Endpoint:** `/api/user/auth`
*   **Método:** `POST`
*   **Body (JSON):**
    ```json
    {
       "username": "deb.rynki",
       "password": "admin1"
    }
    ```
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
       "token": "874fb401-b5b5-452d-ad57-c8364436da0e"
    }
    ```
    Guarda el `access` token. Lo usarás en el header `Authorization` para las solicitudes protegidas.


### Endpoints de Tareas

Todos los endpoints de tareas requieren autenticación. Incluye el token de acceso en el header `Authorization`: `Bearer <your_access_token>`.

#### Listar y Crear Tareas

*   **Endpoint:** `/api/task/getAll`
*   **Método:** `GET` (para listar)
    *   **Respuesta Exitosa (200 OK):** Una lista de todas las tareas del usuario autenticado.
        ```json
        [
             {
                 "id": 3,
                 "title": "Crear API-REST",
                 "description": "Crear task/ user/ para el servidor",
                 "status": "TODO",
                 "created_at": "2025-09-25T23:59:12.221967Z",
                 "author": {
                     "id": 2,
                     "username": "deb.rynki",
                     "email": "deb.rynki@gmail.com",
                     "firstname": "Debora",
                     "lastname": "Rynkiewich"
                 }
             },
             {
                 "id": 2,
                 "title": "Deploy API-REST",
                 "description": "Subir el servidor a Railway",
                 "status": "IN_PROGRESS",
                 "created_at": "2025-09-25T23:55:25.104795Z",
                 "author": {
                     "id": 2,
                     "username": "andy.cuello",
                     "email": "andy.cuello@gmail.com",
                     "firstname": "Andres",
                     "lastname": "Cuello"
                 }
             }
         ]
        ```

*   **Método:** `POST` (para crear)
    *   **Body (JSON):**
        ```json
         {
             "title": "Crear API-REST",
             "description": "Crear task/ user/ para el servidor",
             "status": "TODO"
         }
        ```
        *   `title` es obligatorio.
        *   `description` y `due_date` son opcionales.
    *   **Respuesta Exitosa (201 Created):**
        ```json
        {
          "id": 4,
          "title": "Crear API-REST",
          "description": "Crear task/ user/ para el servidor",
          "status": "TODO",
          "created_at": "2025-09-27T17:59:28.765680Z"
        }
        ```

#### Obtener, Actualizar y Eliminar Tarea por ID

*   **Endpoint:** `/api/task/find`

*   **Método:** `GET`
    *   **Respuesta Exitosa (200 OK):** Detalles de la tarea especificada.
        ```json
        {
            "date": "2025-09-25",
        }
        ```

*   **Método:** `PUT` (para actualización completa)
    *   **Body (JSON):**
        ```json
         {
             "id": 4,
             "title": "Deploy API-REST",
             "description": "Subir el servidor a Railway",
             "status": "IN_PROGRESS"
         }
        ```
    *   **Respuesta Exitosa (200 OK):** La tarea actualizada.

*   **Método:** `DELETE`
    *   **Respuesta Exitosa (204 No Content):** La tarea ha sido eliminada.


#### Filtrar Tareas

El endpoint `/api/tasks/` soporta filtrado por `created_at` y `title`.

*   **Filtrar por fecha de creación (rango):**
    *   `GET /api/tasks/?created_at_after=YYYY-MM-DD&created_at_before=YYYY-MM-DD`
    *   Ejemplo: `GET /api/tasks/?created_at_after=2023-10-01&created_at_before=2023-10-31`
        *   Filtra tareas creadas entre las fechas especificadas.

*   **Filtrar por contenido (búsqueda parcial en el título):**
    *   `GET /api/tasks/?search=palabra_clave`
    *   Ejemplo: `GET /api/tasks/?search=compra`
        *   Devuelve tareas cuyo título contenga "compra".

*   **Combinar filtros:**
    *   `GET /api/tasks/?search=revisar&created_at_after=2023-10-20`

## 6. Bonus Implementados

*   **Manejo de logs:** La aplicación está configurada para registrar eventos importantes y errores utilizando el sistema de logging de Python, guardando los logs en `logs/app.log`.
*   **Creación de tests (unitarias y de integración):** Se han incluido tests para los modelos y los endpoints de la API, asegurando la funcionalidad y estabilidad del código. Puedes ejecutarlos con:
    ```bash
    python manage.py test
    ```
*   **Dockerización:** La solución incluye un `Dockerfile` y un `docker-compose.yml` para facilitar la ejecución de la aplicación en cualquier entorno.
    *   **Para construir la imagen:**
        ```bash
        docker-compose build
        ```
    *   **Para levantar la aplicación (con PostgreSQL y Nginx/Gunicorn):**
        ```bash
        docker-compose up -d
        ```
        La aplicación estará disponible en `http://localhost:8000/`.

## 7. Estructura del Proyecto

```
.
├── invera-todo-challenge/
│   ├── manage.py
│   ├── README.md
│   ├── requirements.txt
│   ├── Dockerfile             # Para Docker
│   ├── docker-compose.yml     # Para Docker
│   ├── .env.example           # Ejemplo de variables de entorno
│   ├── config/                # Configuración global del proyecto
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/                  # Aplicación principal de tareas
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   ├── models.py          # Definición del modelo Task
│   │   ├── serializers.py     # Serializadores para DRF
│   │   ├── urls.py            # URLs de la aplicación core
│   │   └── views.py           # Vistas de la API (TaskViewSet)
│   ├── user/                 # Aplicación de usuarios y autenticación
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   ├── models.py          
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py           
│   ├── task/                 # Aplicación de tareas
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   ├── models.py          
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py           
```

## 8. Consideraciones de Diseño

*   **API RESTful:** Se ha priorizado una arquitectura RESTful clara para los endpoints.
*   **Modularidad:** El proyecto está dividido en aplicaciones (users, core) para una mejor organización y escalabilidad.
*   **Manejo de Errores:** La API devuelve respuestas con códigos de estado HTTP apropiados y mensajes de error descriptivos.
*   **Seguridad:** Se utiliza `djangorestframework-simplejwt` para la autenticación basada en tokens JWT.
*   **Filtrado Eficiente:** `django-filter` se utiliza para proporcionar una forma declarativa y eficiente de filtrar las tareas.

## 9. Pruebas

Para ejecutar las pruebas unitarias y de integración:

```bash
python manage.py test
```

Asegúrate de tener un entorno virtual activo y las dependencias instaladas.

## 10. Contacto

Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarme.

*   **Nombre:** Andres Cuello
*   **Email:** andrescuellotrabajo@gmail.com
*   **LinkedIn:** /andrescuello7
*   **Github:** /andrescuello7
