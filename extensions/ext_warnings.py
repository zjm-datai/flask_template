from flask import Flask

def init_app(app: Flask):
    import warnings

    warnings.simplefilter("ignore", ResourceWarning)
