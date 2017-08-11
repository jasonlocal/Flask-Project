from flask import Flask, render_template, request,session,redirect,url_for,flash,g,request,abort
from model import User,Place,UserInfo
from forms import SignupForm,LoginForm,AddressForm,UserInfoForm
from app import app, db,lm
from flask_login import login_user,logout_user,current_user,login_required


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
def is_loggedin():
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
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser) #add returned data to user table in the database 
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

@app.route("/profile/<firstname>")
def profile(firstname):
	if not is_loggedin():
		return redirect(url_for('login'))
	user= User.query.filter_by(firstname=firstname).first()
	if user == None:
		flash('User %s not foound.' % firstname)
		return redirect(url_for('home'))
	posts=[
	{'author': user, 'body' : 'Test post #1'},
	{'author': user, 'body' : 'Test post #2'}
	]
	return render_template('profile.html',
							user=user,
							posts=posts)


@app.route("/logout")
def logout():
	if not is_loggedin():
		return redirect(url_for('login'))
	logout_user()
	#session.pop('email',None) 
	return redirect(url_for('index'))
#if __name__ == "__main__":
  #app.run(debug=True)


