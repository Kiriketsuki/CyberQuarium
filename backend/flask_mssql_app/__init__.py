from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt import JWT, jwt_required
from your_user_module import authenticate, identity

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kiri:kiri@KIROG@db/cyberquarium_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://kiri:kiri@KIROG\SQLEXPRESS/cyberquarium_db?driver=ODBC+Driver+17+for+SQL+Server'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberquarium_db.db' 

    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    app.config['JWT_AUTH_URL_RULE'] = '/login'

    jwt = JWT(app, authenticate, identity)
    db.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()
        try:
            escrow_user = User(username="ESCROW", email = "escrow@admin.com", coins = 9999999)
            db.session.add(escrow_user)
            db.session.commit()
        except:
            print("db already created")
        print("DB created")
    # enable CORS
    CORS(app, supports_credentials=True)
    # app.wsgi_app = log_request(app)

    # register routes
    from .routes import main
    app.register_blueprint(main)

    return app