# RETO OMNILATAM

## Introducción

+ [Python 3.7.6](https://www.python.org/downloads/release/python-376/).
+ Se utilizo el framework [Django](https://pypi.org/project/Django/).
+ Para las pruebas unitarias se utilizo la libreria [Unittest Django Rest Framework] y la aplicación Postman.    

## Prerequisitos

+ Instalar [Python 3.7.6](https://www.python.org/downloads/release/python-376/)

Habilitar entorno virtual de 
Python y luego instalar las dependencias del proyecto.

```commandline
python -m venv venv
.\venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py makemigrations api
python manage.py migrate
python manage.py runserver

Test:
python manage.py test
```

## Diagrama Entidad Relación Ecommerce Omnilatam. 

![alt text](https://github.com/jmelo77/Reto_Omnilatam/blob/main/Diagrama_Entidad_Relacion.png)