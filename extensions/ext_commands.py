
from flask import Flask 

def init_app(app: Flask):
    
    
    cmds_to_register = [
        
    ]
    
    for cmd in cmds_to_register:
        app.cli.add_command(cmd)