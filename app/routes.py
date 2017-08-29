from flask import Flask, render_template, request,session,redirect,url_for,flash,g,request,abort
from model import User,Place,UserInfo,UserPost
from forms import SignupForm,LoginForm,AddressForm,UserInfoForm,EditForm,PostForm 
from app import app, db,lm
from flask_login import login_user,logout_user,current_user,login_required
from datetime import datetime 
from config import POSTS_PER_PAGE



#app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://localhost/userlogin'
#app.config.from_object('config')
#db.init_app(app)

app.secret_key="development-key" 


@lm.user_loader
def load_user(uid):
	""" load user from database by its id """
	return User.query.get(int(uid))

@app.before_request
def before_request():
	""" store user from current seesion to g global, for later aceess on user info """
	g.user = current_user 
	if g.user.is_authenticated:
		g.user.last_seen=datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

def is_loggedin():
	"""check if the user has already logged in """
	return g.user is not None and g.user.is_authenticated


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
	#if('email' in session):
		#return redirect(url_for('home'))
	if is_loggedin():
		return redirect(url_for('home'))

	form = SignupForm() #instantiate singupForm object
	if request.method == 'POST':
		if form.validate() == False:
			return render_template("signup.html",form=form)
		else:
			account_name=User.make_unique_account_name(form.account_name.data.strip()) # get unique account_name to eliminate the duplicate
			newuser = User(account_name, form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser) #add returned data to user table in the database 
			db.session.commit()
			# make user follow himself 
			db.session.add(newuser.follow(newuser))
			db.session.commit()

			#session['email']=newuser.email
			login_user(newuser)
			next = request.args.get('next')
			#if not is_safe_url(next):
				#return abort(400)

			return redirect(next or url_for('home'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form) #pass form to signup.html  

@app.route("/userInfo", methods=['GET','POST'])
def user_info():
	"""
		Grab user's profile information into the database
		user sign up page, user must log in successfully before getting to this page
	"""

	if not is_loggedin():
		return redirect(url_for('login'))
	form=UserInfoForm()
	if request.method=='POST':
		userInfo=UserInfo(form.nickName.data, form.email.data, form.phone.data, form.city.data, 
			form.state.data, form.zipcode.data, form.education.data, form.sports.data,form.arts.data,
			form.travel.data,form.music.data,form.reading.data,form.gardening.data, form.nature.data,
			form.snowboard.data,form.food.data)
		db.session.add(userInfo) #add returned data to user table in the database 
		db.session.commit()
		return redirect(url_for('home'))

	elif request.method=='GET':
		return render_template('user_info.html',form=form)
		

@app.route("/login",methods=['GET','POST'])
def login():
	#if('email' in session):
		#return redirect(url_for('home')) # if a user has already logged in, then he can't access to login or sigup page
	if is_loggedin():
		return redirect(url_for('home'))

	form=LoginForm()
	if request.method=='POST':
		if form.validate()==False:
			return render_template('login.html',form=form)
		else:
			email=form.email.data
			password=form.password.data
			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				login_user(user)
				#session['email'] =form.email.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))

	elif request.method=='GET':
		return render_template('login.html', form=form)



@app.route("/home",methods=['GET','POST'])
def home():
	#if 'email' not in session: # make sure if user is not logged in, he cant access to the home page 
		#return redirect(url_for('login'))
	if not is_loggedin():
		return redirect(url_for('login'))
	places=[]
	my_coordinates=(37.4221, -122.0844)
	form =AddressForm()
	if request.method=='POST':
		if form.validate()==False:
			return render_template('home.html',form=form)
		else:
			address=form.address.data
			p=Place()
			my_coordinates = p.address_to_latlng(address)
			places= p.query(address)

			return render_template("home.html", form=form, my_coordinates=my_coordinates,places=places)

	elif request.method=='GET':
		return render_template("home.html", form=form, my_coordinates=my_coordinates,places=places)

@app.route("/profile/<account_name>",methods=['GET','POST'])
@app.route('/profile/<account_name>/<int:page>',methods=['GET', 'POST'])
def profile(account_name,page=1):
	if not is_loggedin():
		return redirect(url_for('login'))
	user= User.query.filter_by(account_name=account_name).first()
	if user == None:
		flash('User %s not foound.' % account_name)
		return redirect(url_for('home'))

	form=PostForm()
	if request.method=='POST':
		if form.validate_on_submit():
			post= UserPost(body=form.post.data, timestamp=datetime.utcnow(),author=g.user)
			db.session.add(post)
			db.session.commit()
			flash('Your post is now live!')
			# to void dupicated POST request when refresh the page after previous POST request 
			return redirect(url_for('profile',account_name=g.user.account_name))
	else:
		posts= g.user.followed_posts().paginate(page,POSTS_PER_PAGE,False)
		return render_template('profile.html',
								user=user,
								posts=posts,
								form=form)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	if not is_loggedin():
		return redirect(url_for('login'))
	form=EditForm()
	if form.validate_on_submit():
		g.user.about_me=form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		return redirect(url_for('profile',account_name=g.user.account_name))
	else:
		form.about_me.data=g.user.about_me

	return render_template('edit.html', form=form)

@app.route('/follow/<account_name>')
def follow(account_name):
	if not is_loggedin():
		return redirect(url_for('login'))
	user= User.query.filter_by(account_name=account_name).first()
	if user is None:
		flash('User %s not found' % account_name)
		return redirect(url_for('profile',account_name=g.user.account_name))
	if user==g.user:
		flash('you can\'t follow your self')
		return redirect(url_for('profile',account_name=g.user.account_name))
	u=g.user.follow(user)
	if u is None:
		flash('Can\'t follow ' + account_name + '.')
		return redirect(url_for('profile', account_name=g.user.account_name))
	db.session.add(u)
	db.session.commit()
	flash(' You are now following ' + account_name + '!')
	return redirect(url_for('profile',account_name=account_name))

@app.route('/unfollow/<account_name>')
def unfollow(account_name):
	if not is_loggedin():
		return redirect(url_for('login'))
	user= User.query.filter_by(account_name=account_name).first()
	if user is None:
		flash('User %s not found' % account_name)
		return redirect(url_for('profile',account_name=g.user.account_name))
	if user==g.user:
		flash('you can\'t unfollow your self')
		return redirect(url_for('profile',account_name=g.user.account_name))
	u=g.user.unfollow(user)
	if u is None:
		flash('Can\'t unfollow ' + account_name + '.')
		return redirect(url_for('profile', account_name=g.user.account_name))
	db.session.add(u)
	db.session.commit()
	flash(' You are now unfollowing ' + account_name + '!')
	return redirect(url_for('profile',account_name=account_name))


@app.route("/logout")
def logout():
	if not is_loggedin():
		return redirect(url_for('login'))
	logout_user()
	#session.pop('email',None) 
	return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
	return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template("500.html"), 500






#if __name__ == "__main__":
  #app.run(debug=True)


