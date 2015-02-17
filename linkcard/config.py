from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://@card.cznxydiemfdo.us-west-2.rds.amazonaws.com/linkcard'
db = SQLAlchemy(app)


class User(db.Model):
	uid = db.Column(db.String(80), primary_key=True)
	uname = db.Column(db.String(80))
	pho_url = db.Column(db.String(500))
	temp_id = db.Column(db.Integer)
	email = db.Column(db.String(50))
	headline = db.Column(db.String(150))
	company = db.Column(db.String(200))
	linked_add = db.Column(db.String(100))


	def __init__(self, uid, uname, pho_url, temp_id, email, headline, company, linked_add):
		self.uname=uname
		self.uid = uid
		self.pho_url=pho_url
		self.temp_id=temp_id
		self.email = email
		self.headline=headline
		self.company=company
		self.linked_add=linked_add

	def __repr__(self):
		return '<User %s>' % self.uid



class Link(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	u_id = db.Column(db.String(80), db.ForeignKey('user.uid'))
	User = db.relationship('User', backref =db.backref('link',lazy='dynamic'))
	fri_id = db.Column(db.String(80))
	Friend = db.relationship('User')
	fri_pho = db.Column(db.String(500))


	def __init__(self, user, friend):
		self.user = user
		self.u_id = user.uid
		self.friend = friend
		self.fri_id = friend.uid
		self.fri_pho = friend.pho_url

	def __repr__(self):
		return '<Linkid %s>' % self.id




