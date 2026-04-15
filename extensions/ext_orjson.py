
from flask import Flask
from flask_orjson import OrjsonProvider

def init_app(app: Flask):
    
    app.json = OrjsonProvider(app)