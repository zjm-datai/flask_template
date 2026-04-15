
from flask.app import Flask

def init_app(app: Flask):
    
    from controllers.service_api import bp as service_api_bp
    
    app.register_blueprint(service_api_bp)