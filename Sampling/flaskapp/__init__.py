from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c0115a8363cdd98b3c822c1adba5a7c9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskapp import routes


'''
Further learning:
- https://www.youtube.com/watch?v=u0oDDZrDz9U
- https://www.youtube.com/watch?v=Tu4vRU4lt6k --> attaching SQL database
- https://www.youtube.com/watch?v=ZwCIexvMOGM --> Radio Buttons and bootstrap
'''
