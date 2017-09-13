from flask import Flask 
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME,MAIL_PASSWORD
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
mail=Mail(app) # this is the object that connects to SMTP server 

"""create log file in tmp dir, set upper bound of file size to 1mg, and upper bound of file 
	back ups to 10"""
if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler=RotatingFileHandler('tmp/invite.log','a',1*1024*1024,10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('Invite Startup')

"""send exceptions to the specified email"""
if not app.debug:
	import logging
	from logging.handlers import SMTPHandler
	credentials = None
	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials=(MAIL_USERNAME,MAIL_PASSWORD)
	mail_handler=SMTPHandler((MAIL_SERVER,MAIL_PORT),'no-reply@' + MAIL_SERVER,ADMINS,'invite faliure',credentials)
	mail_handler.setLevel(logging.ERROR)
	app.logger.addHandler(mail_handler)

#app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://localhost/userlogin'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
migrate=Migrate(app,db)

lm = LoginManager()
lm.init_app(app)

from app import routes,model