Backend Flask - Proyecto Base

Este proyecto implementa una plantilla base de backend con Flask, orientada a servicios RESTful.
Se utiliza PostgreSQL como base de datos, junto con SQLAlchemy y Flask-Migrate para la gestión de modelos y migraciones. La autenticación se maneja mediante JWT (JSON Web Tokens).

🛠️ Tecnologías utilizadas

Python 3.12+

Flask (micro-framework web)

Flask-SQLAlchemy (ORM para la base de datos)

Flask-Migrate (migraciones con Alembic)

Flask-JWT-Extended (autenticación con JWT)

PostgreSQL (motor de base de datos relacional)

psycopg2 (conector de Python para PostgreSQL)

python-dotenv (manejo de variables de entorno)

⚠️ Observaciones importantes

Para que psycopg2 funcione en Windows, es necesario tener instalado Microsoft C++ Build Tools o un compilador C disponible en el sistema.

El proyecto está orientado únicamente a servicios (API REST). Aunque la estructura podría extenderse para usar templates y renderizar vistas en frontend, no se recomienda para este caso.

La seguridad depende de configurar adecuadamente las variables de entorno en el archivo .env.

🚀 Instrucciones de instalación
1. Clonar el repositorio
git clone <url-del-repo>
cd BackendFlask

2. Crear entorno virtual
python -m venv venv


Activar el entorno virtual:

Windows:

venv\Scripts\activate


Linux/Mac:

source venv/bin/activate

3. Instalar dependencias
pip install -r requirements.txt

4. Crear archivo .env

En la raíz del proyecto, crea un archivo .env con las siguientes variables:

SECRET_KEY=tu_clave_secreta
JWT_SECRET_KEY=tu_clave_jwt
DEV_DATABASE_URL=postgresql://usuario:password@localhost/nombre_bd_dev
TEST_DATABASE_URL=postgresql://usuario:password@localhost/nombre_bd_test
DATABASE_URL=postgresql://usuario:password@localhost/nombre_bd_prod


⚠️ Reemplazar usuario, password y nombre_bd_* con tus datos reales de PostgreSQL.

5. Inicializar base de datos
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

6. Ejecutar el servidor
python run.py


La aplicación correrá en:
👉 http://127.0.0.1:5000

📡 Endpoints principales
Autenticación

POST /auth/register → Registro de usuario

POST /auth/login → Inicio de sesión y generación de token JWT

GET /auth/logout → Cierre de sesión (revocación de token - pendiente de implementación)

🔑 Seguridad con JWT

El login devuelve un token JWT.

Ese token debe enviarse en el header de cada petición protegida:

Authorization: Bearer <tu_token>

📂 Estructura del proyecto
BackendFlask/
│── app/
│   ├── __init__.py         # Inicialización de la aplicación Flask
│   ├── extensions.py       # Inicialización de extensiones (db, migrate, jwt)
│   ├── models/             # Modelos de la base de datos
│   ├── routes/             # Blueprints (ej: auth)
│   └── services/           # Servicios de lógica (ej: auth_service)
│── migrations/             # Migraciones de Alembic
│── config.py               # Configuración de entornos
│── run.py                  # Punto de entrada de la aplicación
│── requirements.txt        # Dependencias del proyecto
│── .env                    # Variables de entorno (ignorado en git)

✅ Recomendaciones adicionales

Usa Postman o Insomnia para probar los endpoints.

No subas nunca tu .env al repositorio.

En producción, asegúrate de:

Usar un JWT_SECRET_KEY robusto.

Configurar HTTPS para proteger los tokens.

Desactivar DEBUG = True.