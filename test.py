
import unittest
from app import app, db
from app.model import User

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

	def 

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

if __name__ =='__main__':
	unittest.main()