from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://kiri:kiri@10.20.21.57/cyberquarium_db?driver=ODBC+Driver+17+for+SQL+Server'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # enable CORS
    CORS(app, supports_credentials=True)
    # app.wsgi_app = log_request(app)

    # register routes
    from .routes import main
    app.register_blueprint(main)

    return app