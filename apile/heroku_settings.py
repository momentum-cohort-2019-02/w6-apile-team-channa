from apile.settings import *
import os

import django_heroku

DEBUG = os.getenv('DEBUG', False)

django_heroku.settings(locals())