from flask_mail import Message
from flask import render_template
from app import app,mail
from config import ADMINS
from .decorators import async

@async 
def send_async_email(app,msg):
	with app.app_context():
		mail.send(msg)


def send_mail(subject, sender, recipients,text_body,html_body):
	msg=Message(subject,sender=sender,recipients=recipients);
	msg.body=text_body
	msg.html=html_body
	send_async_email(app,msg)




def follower_notification(followed,follower):
	send_mail("[Invite] %s is now following you!" % follower.account_name,
		ADMINS[0],
		[followed.email],
		render_template("follower_email.txt", user=followed, follower=follower), #text body
		render_template("follower_email.html",user=followed,follower=follower)) #html body
