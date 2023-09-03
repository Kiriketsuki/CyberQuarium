from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootpassword@mysql_db:3306/cyberquarium_db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kiri:kiriKIROG@mysql_db:3306/cyberquarium_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://kiri:kiri@KIROG\SQLEXPRESS/cyberquarium_db?driver=ODBC+Driver+17+for+SQL+Server'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberquarium_db.db' 


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