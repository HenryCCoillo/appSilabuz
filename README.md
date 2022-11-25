# Crea tu entorno Virtual
python3 -m venv env

#Activar el entorno Virtual en Windows
env\Scripts\activate.bat

#Instalar los Requisitos
pip install -r requirements.txt

#Varaible de entorno .env
#Creamos el nombre de la BASE de DAATOS
SECRET_KEY="myclavesecreta"
FLASK_APP=app.py
FLASK_DEBUG=1
FLASK_ENV=FLASK_DEVELOPMENT
SQLALCHEMY_DATABASE_URI=mysql://root@localhost/login_aula1
SQLALCHEMY_TRACK_MODIFICATIONS=False 

#Arrancamos la App
flask run

#Migraciones en la base de datos
flask db init
flask db migrate -m "Initial migration."
flask db upgrade

#Crear los roles
Ingresar a la shell de Flask

flask shell
 >> Role.insert_roles()

#Insertar Usuario
En la linea p103 de "main.py" Cambiamos el Usuario que vamos a insertar

#Para Insertar usuario
www.127.0.0.1/insert
