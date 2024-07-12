from pathlib import Path
import os
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ['true', '1', 't']


ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'jlbs_app',
    'django.contrib.admin',
    'django.contrib.auth',
    'axes',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware'
]

ROOT_URLCONF = 'id_logistics_unilever.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'id_logistics_unilever.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'id_logistics_proyect_1'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'jlbs_app/static'),
]

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# Session settings
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True

# CSRF settings
CSRF_COOKIE_SECURE = not DEBUG

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Añadir AxesStandaloneBackend como primer backend
    'django.contrib.auth.backends.ModelBackend',  # Django ModelBackend es el backend de autenticación predeterminado
]

AXES_FAILURE_LIMIT = 3
AXES_COOLOFF_TIME = 24  # En horas
AXES_LOCKOUT_URL = '/lockout/'  # URL a la que redireccionar en caso de bloqueo
AXES_LOCKOUT_PARAMETERS = ["username"]
AXES_CLIENT_IP_CALLABLE = lambda x: None
AXES_CACHE = 'default'

# Configuración de caché
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

#Configuración de Servicio SFTP
SFTP_HOST = os.getenv('SFTP_HOST', 'localhost')
SFTP_PORT = int(os.getenv('SFTP_PORT', 2222))
SFTP_USER = os.getenv('SFTP_USER', 'sftpuser')
SFTP_PASS = os.getenv('SFTP_PASS', 'password')



#Puntos para Subir al ambiente de desarrollo
#Generar un nuevo secret key
#debug = false
#configurar allowed_hosts
#Configuracion de Cookies CSRF Seguras
#CSRF_COOKIE_SECURE = True asegura que la cookie solo se envie a través de conexiones https
#CSRF_COOKIE_HTTPOnly = True asegura que la cookie no sea accesible através de JavaScript
#CSRF_USE_SESSIONS almacena el token CSRF en la sesion del usuario en lugar de en una cookie separada.
#SESSION_COOKIE_SECURE = asegura que las cookies de sesion solo se transmitan a través de HTTPS.
#SESSION_COOKIE_HTTPONLY = Evita que las cookies de sesion sean accesibles a traves de JavaScript
#Secure_Browser_Xss_Filter = habilita el filtro xss del navegador para mitigar ataques XSS.
#Secure_Content_Type_Nosniff = evita que el navegador intente adivinar el tipo de contenido de los archivos, reduciendo el riesgo de ciertos tipos de ataques.
#Secure_Hsts_Seconds = habilita http strict transport security para obligar a los navegadores a usar solo HTTPS durante un año
#Secure_hsts_include_subdomains = aplica hsts a todos los subdominios
#Secure_Hsts_Preload = permite que el dominio sea incluido en la lista de precarga hsts
#Secure_SSL_Redirect = redirige todas las solicitudes http a https, asegurando que todas las comunicacione sean seguras.
#Estar seguro que la aplicación funciona en https
#Obtener Certificado SSL/TLS
#Configurar el servidor Web
#Configurar Django para https
#Configurar Redirección a Https
