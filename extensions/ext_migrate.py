

from flask import Flask


def init_app(app: Flask):
    import flask_migrate
    
    from extensions.ext_database import db  
    
    flask_migrate.Migrate(app, db)