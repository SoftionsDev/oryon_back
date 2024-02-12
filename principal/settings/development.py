from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = [
    os.environ.get('FRONTEND_URL')
]

