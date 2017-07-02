from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField
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