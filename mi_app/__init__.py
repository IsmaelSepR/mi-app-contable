import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Redirige a esta vista si el usuario no est� logueado
login_manager.login_message = 'Por favor, inicia sesion para acceder a esta pagina.'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configurar la aplicaci�n
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    # Usar una base de datos en la carpeta 'instance' para mantener el proyecto limpio
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', f"sqlite:///{os.path.join(app.instance_path, 'database.db')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Asegurarse de que la carpeta de instancia exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        # Registrar Blueprints
        from . import auth
        app.register_blueprint(auth.auth_bp)

        from . import main
        app.register_blueprint(main.main_bp)

        # Cargar el modelo de usuario para Flask-Login
        from . import models

    return app
