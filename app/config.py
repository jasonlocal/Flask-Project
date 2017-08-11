import os 
basedir= os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/userlogin'#'postgresql:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS= True
