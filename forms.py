from flask_wtf import Form 
from wtforms import StringField, IntegerField, PasswordField, SubmitField,SelectField,TextAreaField,BooleanField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	first_name=StringField('First name',validators=[DataRequired("Please enter your first name.")]) # validator checks wheter the field is empty or not
	last_name = StringField('Last name',validators=[DataRequired("Please enter your last name.")])
	email=StringField('Email',validators=[DataRequired("Please enter email address."), Email("Please enter valid email")])
	password=PasswordField('Password',validators=[DataRequired("Please enter password."),Length(min=8,message="password must be 8 characters or more")])
	submit= SubmitField('Sign up')

class LoginForm(Form):
	email=StringField('Email', validators=[DataRequired('this field can not be empty'), Email("Please enter valid email address")])
	password =PasswordField('Password', validators=[DataRequired("password can not be empty")])
	submit=SubmitField("Log in")

class AddressForm(Form):
	address=StringField('Address',validators=[DataRequired('Please enter address')])
	submit=SubmitField("Submit")

class UserInfoForm(Form):
	nickName=StringField("Nick Name")
	email = StringField("Email")
	phone=IntegerField("Phone")
	city= StringField("City")
	state = SelectField("State", choices=[('Al','Alabama'),('AK','Alaska'),('AZ','Arizona')])
	zipcode= StringField("Zipcode")
	education=SelectField("College",choices=[('harvard','Harvard University'),('MIT','Massachusetts Institute of Technology'),('NEU','Northeastern University')])

	sports=BooleanField("Sports")
	arts=BooleanField("Arts")
	travel=BooleanField("Travel")
	music=BooleanField("Music")
	reading=BooleanField("Reading")
	gardening=BooleanField("Gardening")
	nature=BooleanField("Nature")
	snowboard=BooleanField("Snowboard")
	food=BooleanField("Food")
	comments=TextAreaField("Comments")