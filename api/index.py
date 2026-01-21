import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from barbershop.app import app as fastapi_app

handler = fastapi_app
