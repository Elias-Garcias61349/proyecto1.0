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

2. Crea un entorno virtual y actívalo:
---

```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

3. Instala las dependencias del proyecto:
```bash
pip install -r requirements.txt
```

4. Configura la conexión a la base de datos en .env o mediante variables de entorno:
```bash
DEBUG=True
SECRET_KEY=django-insecure-r-bi-2f5im403
DB_NAME=snake
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost  # A qui va tu ip de django
DB_PORT=5433  #y aqui va el pueto que vallas a utilizar 
```
5. Aplica migraciones:
```bash
python manage.py migrate
```

6. Ejecuta o avtiva el servidor, no deves de salir de tu entorno virtual 
```bash
python manage.py runserver 9090
```
