from flask import Flask, render_template, request,session,redirect,url_for
from model import db, User,Place
from forms import SignupForm,LoginForm,AddressForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://localhost/userlogin'
db.init_app(app)

app.secret_key="development-key" 

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")
  

@app.route("/user_info")
def user_info():
	return render_template("user_info.html")



@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if('email' in session):
		return redirect(url_for('home'))
	form = SignupForm() #instantiate singupForm object
	if request.method == 'POST':
		if form.validate() == False:
			return render_template("signup.html",form=form)
		else:
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser) #add returned data to user table in the database 
			db.session.commit()

			session['email']=newuser.email
			return redirect(url_for('home'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form) #pass form to signup.html  

@app.route("/login",methods=['GET','POST'])
def login():
	if('email' in session):
		return redirect(url_for('home')) # if a user has already logged in, then he can't access to login or sigup page
	form=LoginForm()
	if request.method=='POST':
		if form.validate()==False:
			return render_template('login.html',form=form)
		else:
			email=form.email.data
			password=form.password.data
			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				session['email'] =form.email.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))

	elif request.method=='GET':
		return render_template('login.html', form=form)



@app.route("/home",methods=['GET','POST'])
def home():
	if 'email' not in session: # make sure if user is not logged in, he cant access to the home page 
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

@app.route("/logout")
def logout():
	session.pop('email',None) 
	return redirect(url_for('index'))
if __name__ == "__main__":
  app.run(debug=True)


