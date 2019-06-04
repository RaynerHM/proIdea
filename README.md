1. #### Crear virtualenv:
	> virtualenv -p python3.5 envIdeas

2. #### Activar virtualenv:
	> source envIdeas/bin/activate


3. #### Descargar projecto desde GitLab:
	> git clone <<Repositorio>>

4. #### Instalar dependencias:
	> cd projectideas
	> pip install -r requeriments.txt


5. #### Cargar variables de entorno, en el virtualenv:
	1. ##### Crear un varchivo con el nombre que quieras, ejemplo, **variables**. En este se guardaran todas las variables de entorno:
		``` python
		# Extablecer credenciales de la Base de Datos PostgreSQL:
		export BD_NAME='Cambiar'
		export BD_USER='Cambiar'
		export BD_PASS='Cambiar'
		export BD_HOST='Cambiar'
		export BD_PORT='Cambiar'

		# Extablecer la ruta y el nombre para el archivo log:
		export RUTA_LOG='Cambiar'

		# Extablecer contraseña para asignarle a los usuarios sincronizados desde LDAP
		export PASS_LDAP='Cambiar'

		# Extablecer credenciales del servidor LDAP
		export LDAP_DOMAIN='Cambiar'
		export LDAP_SERVER='Cambiar'
		export LDAP_PASS_SERVER='Cambiar'
		export LDAP_BASE_SEARCH='Cambiar'
		export LDAP_CONNECTION_USERNAME='Cambiar'

		```
	2. ##### Donde dice *'Cambiar'*, poner los data correspondientes. Ejemplo:
		``` python
		# Credenciales Base de Datos PostgreSQL
		export BD_NAME='bd_ideas'
		export BD_USER='ideas'
		export BD_PASS='123456789'
		export BD_HOST='127.0.0.1'
		export BD_PORT='5432'

		#Ruta para archivo log
		export RUTA_LOG='/var/log/ideas/log_ideas.log'

		#Contraseña para asignarle a los usuarios sincronizados desde LDAP
		export PASS_LDAP='123456789'

		# Credenciales del servidor LDAP
		export LDAP_DOMAIN='example.com'
		export LDAP_SERVER='ldap://0.0.0.0:0000'
		export LDAP_PASS_SERVER='123456789'
		export LDAP_BASE_SEARCH='OU="" Usuarios,DC="",DC=com'
		export LDAP_CONNECTION_USERNAME='CN=servicios,CN=Users,DC="",DC=com'
		```
	3. ##### Y por ultimo, ejecutar en la terminar:
		> source variable

6. Modificar el archivo settings.py:
	Todas las indentaciones esta hechas con tab de 4 espacios  

	1. ##### Importar las variables de entorno:
		``` python
		BD_NAME = os.environ.get('BD_NAME')
		BD_USER = os.environ.get('BD_USER')
		BD_PASS = os.environ.get('BD_PASS')
		BD_HOST = os.environ.get('BD_HOST')
		BD_PORT = os.environ.get('BD_PORT')
		RUTA_LOG = os.environ.get('RUTA_LOG')
		PASS_LDAP = os.environ.get('PASS_LDAP')
		LDAP_SERVER = os.environ.get('LDAP_SERVER')
		LDAP_DOMAIN = os.environ.get('LDAP_DOMAIN')
		LDAP_PASS_SERVER = os.environ.get('LDAP_PASS_SERVER')
		LDAP_BASE_SEARCH = os.environ.get('LDAP_BASE_SEARCH')
		LDAP_CONNECTION_USERNAME = os.environ.get('LDAP_CONNECTION_USERNAME')
		```
	2. ##### Agregar las siguientes Apps:
		``` python
		INSTALLED_APPS = [
			...
			'appIdeas',
			'django_python3_ldap',
			'django_extensions',
		]
		```
	3. ##### Credenciales de la Base de Datos:
		``` python
		DATABASES = {
			'default': {
				'ENGINE': 'django.db.backends.postgresql_psycopg2',
				'NAME': BD_NAME,
				'USER': BD_USER,
				'PASSWORD': BD_PASS,
				'HOST': BD_HOST,
				'PORT': BD_PORT,
			},
		}
		```
	4. ##### Varibles de Internacionalización:
		``` python
		LANGUAGE_CODE = 'es-DO'
		TIME_ZONE = 'America/Santo_Domingo'
		USE_I18N = True
		USE_L10N = True
		USE_TZ = True
		```
	5. ##### Varibles para los archivos estaticos
		``` python
		STATIC_URL = '/static/'
		STATICFILES_DIRS = (
			os.path.join(BASE_DIR, 'static'),
			os.path.join(BASE_DIR, 'static/media'),
		)
		STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
		MEDIA_URL = '/static/media/'
		MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')
		```	
	6. ##### Variable para la url del login:
		``` python
		LOGIN_URL = "/login"
		```
	7. ##### Variables para las configuraciones de LDAP:
		``` python
		# ************************** AUTENTICACION USUARIOS **************************
		AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

		DOMAIN = LDAP_DOMAIN
		AD_LDAP_URL = LDAP_SERVER
		AD_SEARCH_DN = LDAP_BASE_SEARCH
		AD_SEARCH_FIELDS = [
			'displayname',
			'mail',
			'mailnickname',
			'title'
		]
		# ************************ FIN AUTENTICACION USUARIOS ************************

		# *************************** SINCRONIZAR USUARIOS ***************************
		LDAP_AUTH_URL = LDAP_SERVER
		LDAP_AUTH_USE_TLS = False
		LDAP_AUTH_SEARCH_BASE = LDAP_BASE_SEARCH
		LDAP_AUTH_USER_FIELDS = {
			"username": "sAMAccountName",
			"first_name": "givenName",
			"last_name": "sn",
			"email": "mail",
		}

		LDAP_AUTH_OBJECT_CLASS = "user"
		LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)
		LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
		LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"
		LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"
		LDAP_AUTH_CONNECTION_USERNAME = LDAP_CONNECTION_USERNAME
		LDAP_AUTH_CONNECTION_PASSWORD = LDAP_PASS_SERVER
		LDAP_AUTH_CONNECT_TIMEOUT = None
		LDAP_AUTH_RECEIVE_TIMEOUT = None
		LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"
		# ************************* FIN SINCRONIZAR USUARIOS *************************
		```

7. #### Migragar modelos:
	> python manage.py makemigrations
	> python manage.py migrate

8. #### Cargar Datos:
	> python manage.py loaddata fixtures/fixtures.json


9. #### Correr servidor:
	> python manage.py runserver



#### Crear crontab para sincronizar los usuarios de LDAP, en el modelo User de Django
``` python
*/5 * * * * <<Ruta absoluta del projecto\>>/projectIdeas/synchronize_users/prod/synchronize_users.sh
#El crontab se ejecutara cada 5 minutos
```

Ejemplo:
``` python
*/5 * * * * /home/rhernandez/projectIdeas/synchronize_users/prod/synchronize_users.sh
```
