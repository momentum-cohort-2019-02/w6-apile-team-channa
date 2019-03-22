from apile.settings import *
import os

import django_heroku

DEBUG = True

# clintion fix:
# DEBUG = os.getenv('DEBUG', False)

django_heroku.settings(locals())