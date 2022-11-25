# Aplicacion de Flask
### Python 3.10 > 
## Crea tu entorno Virtual

```bash
python3 -m venv env
```


## Activar el entorno Virtual en Windows

```bash
env\Scripts\activate.bat
```

## Instalar los Requisitos

```bash
pip install -r requirements.txt
```

## Varaible de entorno .env
### Creamos el nombre de la BASE de DATOS

```bash
SECRET_KEY="myclavesecreta"
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_ENV=FLASK_DEVELOPMENT
SQLALCHEMY_DATABASE_URI=mysql://root@localhost/login_aula1
SQLALCHEMY_TRACK_MODIFICATIONS=False 
```
## Arrancamos la App

```bash
flask run
```


## Migraciones en la base de datos
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

## Crear los roles
### Ingresar a la shell de Flask

```bash
flask shell
```
### Insertamos Roles
```bash
>> Role.insert_roles()
```

## Insertar Usuario
En la linea p103 de "main.py" Cambiamos el Usuario que vamos a insertar

### Para Insertar usuario
www.127.0.0.1/insert
