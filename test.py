#!venv/bin/python
import unittest
from app import app, db
from app.model import User, UserPost
from datetime import datetime, timedelta

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['TESTING']= True 
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/usertest'
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_follow_posts(self):
		u1=User(account_name='sean',firstname='sean',lastname='scott',email='sean@hotmail.com',password='Zx199177624')
		u2=User(account_name='jason',firstname='jason',lastname='zheng',email='jasonlocal@hotmail.com',password='Zx199177624')
		u3=User(account_name='mary',firstname='mary',lastname='chen',email='mary@hotmail.com',password='Zx199177624')
		u4=User(account_name='lucy',firstname='lucy',lastname='wang',email='lucy@hotmail.com',password='Zx199177624')
		db.session.add(u1)
		db.session.add(u2)
		db.session.add(u3)
		db.session.add(u4)
		utcnow=datetime.utcnow()
		p1=UserPost(body='post from sean',author=u1,timestamp=utcnow+timedelta(seconds=1))
		p2=UserPost(body='post from jason',author=u2,timestamp=utcnow+timedelta(seconds=2))
		p3=UserPost(body='post from mary',author=u3,timestamp=utcnow+timedelta(seconds=3))
		p4=UserPost(body='post from lucy',author=u4,timestamp=utcnow+timedelta(seconds=4))
		u1.follow(u1)
		u1.follow(u2)
		u1.follow(u4)
		u2.follow(u2)
		u2.follow(u3)
		u3.follow(u3)
		u3.follow(u4)
		u4.follow(u4)

		db.session.add(u1)
		db.session.add(u2)
		db.session.add(u3)
		db.session.add(u4)
		db.session.commit()

		#check followed post of each user 
		f1=u1.followed_posts().all()
		f2=u2.followed_posts().all()
		f3=u3.followed_posts().all()
		f4=u4.followed_posts().all()
		assert len(f1) == 3
		assert len(f2) == 2
		assert len(f3) == 2
		assert len(f4) == 1
		assert f1 == [p4, p2, p1]
		assert f2 == [p3, p2]
		assert f3 == [p4, p3]
		assert f4 == [p4]

	
	def test_make_unique_account_name(self):
		u=User(account_name='sean',firstname='sean',lastname='scott',email='sean@hotmail.com',password='Zx199177624')
		db.session.add(u)
		db.session.commit()
		account_name = User.make_unique_account_name('sean')
		assert account_name !='sean'
		u=User(account_name=account_name,firstname='sean1',lastname='scott1',email='sean1@hotmail.com',password='Zx199177624')
		db.session.add(u)
		db.session.commit()
		account_name2=User.make_unique_account_name('sean')
		assert account_name2 !='sean'
		assert account_name2 != account_name

	def test_follow(self):
		u1= User(account_name='sean',firstname='sean',lastname='scott',email='sean@hotmail.com',password='Zx199177624')
		u2=User(account_name='jason',firstname='jason',lastname='zheng',email='jasonlocal@hotmail.com',password='Zx199177624')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		assert u1.unfollow(u2) is None
		u=u1.follow(u2)
		db.session.add(u)
		db.session.commit()
		assert u1.follow(u2) is None 
		assert u1.is_following(u2)
		assert u1.followed.count()==1
		assert u1.followed.first().account_name=='jason'
		assert u1.followers.count() ==0
		assert u2.followers.count() ==1
		assert u2.followers.first().account_name=='sean'
		u=u1.unfollow(u2)
		assert u is not None
		db.session.add(u)
		db.session.commit()
		assert not u1.is_following(u2)
		assert u1.followed.count()==0
		assert u2.followers.count()==0
	


		
if __name__ =='__main__':
	unittest.main()