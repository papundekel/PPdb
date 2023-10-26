from json import dump as json_dump
from sys import stdout

from backend.app import app

json_dump(app.openapi(), stdout, indent=4)
