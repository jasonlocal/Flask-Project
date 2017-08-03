from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
app = Flask(__name__)
#app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://localhost/userlogin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
migrate=Migrate(app,db)

from app import routes,model