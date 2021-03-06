import os 
basedir= os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/userlogin'#'postgresql:///' + os.path.join(basedir,'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS= True
MAX_SEARCH_RESULTS=50

# mial server settings for logging 
MAIL_SERVER='smtp.googlemail.com'
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
#pagination
POSTS_PER_PAGE=3 
#administrator list
ADMINS=['zheng.xun@husky.neu.edu']

# -*- coding: utf-8 -*-
# ...
# available languages
LANGUAGES= {
	'en' : 'English',
	'zh_Hans' : 'Chinese'
}