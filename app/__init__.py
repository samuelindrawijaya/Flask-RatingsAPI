from flask import Flask
from flask_migrate import Migrate
from app.config.connector import db, migrate, jwt, login_manager  # Import extensions
from app.config.config import Config
from app.models.userRoleModel import User
from app.seeds.seeds import seed_data
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    Swagger(app, 
    template={
            "swagger": "2.0",
            "info": {
                "title": "RATINGS API",
                "description": "RATINGS Restfull API made by Flask and MySQL",
                "contact": {
                "responsibleOrganization": "ME",
                "responsibleDeveloper": "Me",
                "email": "me@me.com",
                "url": "www.me.com",
                }
            },
            "securityDefinitions": {
                "bearerAuth": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
                }
            },
            "security": [
                {"bearerAuth": []}
            ],
        }
    )
    
    # Register Blueprints
    from app.routes.api import user_bp, role_bp, auth_bp, review_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(role_bp, url_prefix='/api/roles')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(review_bp, url_prefix='/api/review')
    
    # Define basic routes for DB creation and seeding
    @app.route('/')
    def index():
        return 'hello'
    
    @app.route('/create-all-db')
    def create_all_db():
        db.create_all()  # No need to return anything here
        return 'Database tables created successfully!'
    
    @app.route('/create-all-seed')
    def create_seed():
        seed_data()
        return 'Database seeded successfully!'

    return app
