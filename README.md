# 🚀 Backend Flask - Proyecto Base

![Python](https://img.shields.io/badge/python-3.12+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-microframework-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

Plantilla base de **backend REST** con **Flask**, **PostgreSQL**, **SQLAlchemy/Flask-Migrate** y **JWT** para autenticación.

---

## 📑 Contenidos
- [🛠️ Tecnologías](#️-tecnologías)
- [⚠️ Observaciones](#️-observaciones)
- [📦 Instalación](#-instalación)
- [📄 Variables de entorno (.env)](#-variables-de-entorno-env)
- [🗄️ Migraciones de base de datos](#️-migraciones-de-base-de-datos)
- [▶️ Ejecutar el servidor](#️-ejecutar-el-servidor)
- [📡 Endpoints principales](#-endpoints-principales)
- [🔑 Seguridad con JWT](#-seguridad-con-jwt)
- [📂 Estructura del proyecto](#-estructura-del-proyecto)
- [✅ Recomendaciones](#-recomendaciones)

---

## 🛠️ Tecnologías
- **Python 3.12+**
- **Flask**
- **Flask-SQLAlchemy**
- **Flask-Migrate** (Alembic)
- **Flask-JWT-Extended / PyJWT**
- **PostgreSQL**
- **psycopg2 / psycopg2-binary**
- **python-dotenv**

---

## ⚠️ Observaciones
- En **Windows**, para compilar/instalar `psycopg2` puede requerirse **Microsoft C++ Build Tools** (o un compilador C instalado).
- Proyecto orientado a **API REST (servicios)**. Aunque la estructura soporta templates, **no** se recomienda usarla para frontend aquí.
- Asegura un `.env` correcto para claves y conexión a BD.

---

## 📦 Instalación
```bash
# 1) Clonar
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# 2) Entorno virtual
python -m venv venv

# 3) Activar entorno
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4) Dependencias
pip install -r requirements.txt

```
## 📄 Variables de entorno (.env)

- Crea un archivo .env en la raíz con:

- **SECRET_KEY=tu_clave_secreta**
- **JWT_SECRET_KEY=tu_clave_jwt**

- **DEV_DATABASE_URL=postgresql://usuario:password@localhost/nombre_bd_dev**
- **TEST_DATABASE_URL=postgresql://usuario:password@localhost/nombre_bd_test**
- **DATABASE_URL=postgresql://usuario:password@localhost/nombre_bd_prod**

⚠️ Reemplaza usuario, password y nombre_bd_* por tus valores reales de PostgreSQL.

---

## 🗄️ Migraciones de base de datos
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask init-data
```
---

## ▶️ Ejecutar el servidor
```bash
python run.py
py run.py #Tambien funciona
```

La aplicación estará disponible en:
- 👉 http://127.0.0.1:5000

---

## 📡 Endpoints principales

### 🔐 Autenticación
| Método | Endpoint         | Descripción                               |
|--------|------------------|-------------------------------------------|
| POST   | `/auth/register` | Registro de usuario                       |
| POST   | `/auth/login`    | Inicio de sesión y generación de token    |
| GET    | `/auth/logout`   | Cierre de sesión *(pendiente revocación)* |

---

## 🔑 Seguridad con JWT

El login devuelve un **token JWT**.  
Ese token debe enviarse en el header de cada petición protegida:

```http
Authorization: Bearer <tu_token>
```

---

## 📂 Estructura del proyecto
```bash
BackendFlask/
│── app/
│   ├── __init__.py        # Inicialización de la app Flask
│   ├── extensions.py      # Extensiones (db, migrate, jwt)
│   ├── models/            # Modelos de la BD
│   ├── routes/            # Blueprints (ej: auth)
│   └── services/          # Lógica de negocio (ej: auth_service)
│── migrations/            # Migraciones Alembic
│── config.py              # Configuración de entornos
│── run.py                 # Punto de entrada de la aplicación
│── requirements.txt       # Dependencias del proyecto
│── .env                   # Variables de entorno (ignorado en git)
```
---

## ✅ Recomendaciones

- **Usa Postman o Insomnia para probar endpoints.**

- **Nunca subas tu .env al repositorio.**