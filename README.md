## Requisitos

- Python 3.10+
- pip
- MySQL (local o remoto)
- Virtualenv (recomendado)

---

## 🛠 Instalación paso a paso

1. Clona el repositorio:
git clone https:
```bash
//github.com/Elias-Garcias61349/proyecto1.0.git
cd proyecto1.0
```

2. Crea un entorno virtual y actívalo
```bash
python -m venv env
source env/bin/activate     # En Windows: env\Scripts\activate
```
3. Instala las dependencias
```bash
pip install -r requirements.txt
```

4. Configura la base de datos en .env (o desde settings.py)
env
```bash
DEBUG=True
SECRET_KEY=django-insecure-r-bi-2f5im403
DB_NAME=snake
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost       # o la IP de tu servidor de base de datos
DB_PORT=5433            # Puerto que estás usando
```
⚠️ Asegúrate de tener PostgreSQL corriendo y la base de datos creada con el nombre snake.

5. Aplica las migraciones
```bash
python manage.py migrate
```
6. Crea un superusuario (opcional pero recomendado)
```bash
python manage.py createsuperuser
```
7. Inicia el servidor (no salgas del entorno virtual)
```bash
python manage.py runserver 9090
```
