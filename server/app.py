# app.py
from flask import Flask
from models.models import db, User
from werkzeug.security import generate_password_hash
from flask_cors import CORS

app = None
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
    app.debug = True

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    app.app_context().push()

    return app

app = create_app()

from controllers.auth import *
from  controllers.parking import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(email='admin@gmail.com', password=generate_password_hash('123'), name='Admin', address='Home', pin_code='123456', role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run()