from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Database import db
import secrets



app = Flask(__name__,template_folder='template')
app.secret_key = secrets.token_hex(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/song_generator'
db.init_app(app)

from Account_setup.Routes import account_setup_bp
from Review.Routes import review_bp
from Show_list.Routes import showlist_bp
from Song.Routes import song_bp
from Poetry.Routes import poetry_bp
from Language.Routes import language_manipulation_bp

app.register_blueprint(account_setup_bp)
app.register_blueprint(review_bp)
app.register_blueprint(showlist_bp)
app.register_blueprint(song_bp)
app.register_blueprint(poetry_bp)
app.register_blueprint(language_manipulation_bp)

if __name__ == '__main__':
    app.run(debug=True)
