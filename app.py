from app_factory import create_app

app = create_app()

celery = app.extensions["celery"]

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5002)