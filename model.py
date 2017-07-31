from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder 
import urllib2
import json


db=SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid= db.Column(db.Integer, primary_key=True)
	firstname= db.Column(db.String(100))
	lastname= db.Column(db.String(100))
	email= db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))

	def __init__(self, firstname, lastname, email, password):
		self.firstname=firstname.title() # title() preserves capitanle of first letter
		self.lastname=lastname.title()
		self.email=email.lower() # map every char to lower case 
		self.set_password(password) #

	def set_password(self,password):
		self.pwdhash=generate_password_hash(password)
	def check_password(self,password):
		return check_password_hash(self.pwdhash, password)


class UserPost(db.Model):
  """Represent userpost table, need to finish the implementaiton 
     need to create table in database """
  __tablename__='userpost'
  id= db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp=db.Column(db.DateTime)
  user_id = db.Column(db.Integer,db.ForeignKey('user.id'))



class UserInfo(db.Model):
  """represent UserInfo table in the database"""
  __tablename__='userinfo'
  uid = db.Column(db.Integer,primary_key=True) #primary key is required with salAlchemy
  nickname=db.Column(db.String(100))
  email=db.Column(db.String(120))
  phone=db.Column(db.String(15))
  city=db.Column(db.String(100))
  state=db.Column(db.String(100))
  zipcode=db.Column(db.String(10))
  education=db.Column(db.String(100))
  sports=db.Column(db.Boolean)
  arts=db.Column(db.Boolean)
  travel=db.Column(db.Boolean)
  music=db.Column(db.Boolean)
  reading=db.Column(db.Boolean)
  gardening=db.Column(db.Boolean)
  nature=db.Column(db.Boolean)
  snowboard=db.Column(db.Boolean)
  food=db.Column(db.Boolean)
  def __init__(self, nickname,email,phone,city,state,zipcode,education,sports,arts,travel,music,reading,gardening,nature,snowboard,food):
    self.nickname=nickname
    self.email=email
    self.phone=phone
    self.city=city
    self.state=state
    self.zipcode=zipcode
    self.education=education
    self.sports=sports
    self.arts=arts
    self.travel=travel
    self.music=music
    self.reading=reading
    self.gardening=gardening
    self.nature=nature
    self.snowboard=snowboard
    self.food=food





# p = Place()
# places = p.query("1600 Amphitheater Parkway Mountain View CA")
class Place(object):
  def meters_to_walking_time(self, meters):
    # 80 meters is one minute walking time
    return int(meters / 80)  

  def wiki_path(self, slug):
    return urllib2.urlparse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))
  
  def address_to_latlng(self, address):
    g = geocoder.google(address)
    return (g.lat, g.lng)

  def query(self, address):
    lat, lng = self.address_to_latlng(address)
    
    query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
    g = urllib2.urlopen(query_url)
    results = g.read()
    g.close()

    data = json.loads(results)
    
    places = []
    for place in data['query']['geosearch']:
      name = place['title']
      meters = place['dist']
      lat = place['lat']
      lng = place['lon']

      wiki_url = self.wiki_path(name)
      walking_time = self.meters_to_walking_time(meters) # convert the distance to walking time 

      d = {
        'name': name,
        'url': wiki_url,
        'time': walking_time,
        'lat': lat,
        'lng': lng
      }

      places.append(d)

    return places