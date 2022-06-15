from feeder.settings.base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [host for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "DISABLE_SERVER_SIDE_CURSORS": True,
    },
}
