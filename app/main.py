from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)

    api = Api(
        app,
        title="My REST API",
        version="1.0",
        description="RESTful API for users"
    )

    from app.routes import api_ns
    api.add_namespace(api_ns)

    return app
