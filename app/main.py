from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy


# Create SQLAlchemy instance (no app yet)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://lib_admin:1qaz!QAZ@localhost/Library"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize db with app
    db.init_app(app)


    api = Api(
        app,
        title="Library Project",
        version="1.0",
        description="",
        doc="/swagger"
    )

    # import namespaces
    from app.users.routes import users_ns
    from app.books.routes import books_ns

    # register namespaces
    api.add_namespace(users_ns, path="/api/users")
    api.add_namespace(books_ns, path="/api/books")


    return app
