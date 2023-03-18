from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://kiri:kiri@KIROG\SQLEXPRESS/cyberquarium_db?driver=ODBC+Driver+17+for+SQL+Server'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app