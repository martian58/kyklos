from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Update if using another database
    app.config['SECRET_KEY'] = 'FDSgosidfphgv8u0werghrv8w0eghdfsufdbgsfdjghsugthidzphgfaeieighiughvdfs'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))

    from routes import register_routes
    register_routes(app, db, bcrypt)

    return app
