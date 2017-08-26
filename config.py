import os 
basedir= os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/userlogin'#'postgresql:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS= True

# mial server settings for logging 
MAIL_SERVER='localhost'
MAIL_PORT=25
MAIL_USERNAME=None 
MAIL_PASSWORD=None 

#administrator list
ADMINS=['zheng.xun@husky.neu.edu']