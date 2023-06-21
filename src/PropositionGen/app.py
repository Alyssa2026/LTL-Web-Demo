from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    from .Proposition import main
    app.register_blueprint(main)

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)