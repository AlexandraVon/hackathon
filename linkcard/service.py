from flask import Flask, jsonify,flash, request, redirect, url_for
from config import db, User, Link
import json
from rauth.service import OAuth2Service


try:
	from flask.ext.cors import CORS
except ImportError:
	import os
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	os.sys.path.insert(0, parentdir)

	from flask.ext.cors import CORS
	from flask import request, url_for

CONSUMER_KEY = '752f0vrdqznviu'
CONSUMER_SECRET = 'wEJ809EaoYFgzA2w'
CORS_ALLOW_HEADERS = "Content-Type"
CORS_RESOURCES = {r"/*":{"origins":"*"}}

app = Flask(__name__)
app.config.from_object(__name__)

#app.config['CORS_ALLOW_HEADERS']="Content-Type"
#app.config['CORS_RESOURCES']={r"/cors/*":{"origins":"*"}}

cors = CORS(app)

# rauth OAuth 2.0 service wrapper
linkedin = OAuth2Service(name='linkedin', 
				access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
				authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
				client_id=app.config['CONSUMER_KEY'],
				client_secret=app.config['CONSUMER_SECRET'],
				base_url='https://api.linkedin.com/v1/')

@app.route('/login')
def loginbylinkedIn():
	redirect_uri = url_for('authorized', _external=True)
	params = {'redirect_uri': redirect_uri,'response_type': 'code', 'state':'DCEEFWF45453sdffef424'}
	return redirect(linkedin.get_authorize_url(**params))

@app.route('/authorized')
def authorized():
	# check to make sure the user authorized the request
	if not 'code' in request.args:
		flash('You did not authorize the request')
		return redirect(url_for('index'))
	# make a request for the access token credentials using code
	redirect_uri = url_for('authorized', _external=True)
	data={'code':request.args['code'], 'redirect_uri':redirect_uri
		,'grant_type':'authorization_code'}
	session = linkedin.get_auth_session(data=data, decoder=json.loads)
	r = session.get('people/~',params={'format': 'json'}).content
	userid=json.loads(r)['id']

	user = User.query.filter_by(uid=userid).first()
	if user == None:
		tmp=session.get('people/id='+userid+\
		':(first-name,last-name,headline,picture-url,positions)',params={'format': 'json'}).content
		tmpx=json.loads(tmp)
		username=tmpx['firstName']+" "+tmpx['lastName']
		headline=tmpx['headline']
		pic=tmpx['pictureUrl']
		company =parsecompany(tmpx['positions'])
		a=User(userid,username,pic,None,None,headline,company,None)
		db.session.add(a)
		db.session.commit()
		uu ={  	 'user_id'		:userid
				,'user_name'	:username
				,'template_id'	:None
				,'photo_url'	:pic
				,'email'		:None
				,'headline'		:headline
				,'company'		:company
				,'linkedin_add'	:None
			}
		data = { 'user': uu
				,'friends':{}
				,'exist':False
			}		
		print data
	else:
		data = getuserdata(user)
	return jsonify(data=data)


def parsecompany(positions):
	return None	

def getjson(request):
	text= request.json
	content = json.loads(text)
	return content




@app.route('/addfriends',methods=['POST'])
def addfri():
	content = getjson(request)
	userid=content['user_id']
	friid=content['friend_id']
	if userid==None or friid==None:
		return jsonify(status=False)
	user = User.query.filter_by(uid=userid).first()
	friend = User.query.filter_by(uid=friid).first()
	if user==None or friend ==None:
		return jsonify(status=False)
	l = Link(user, friend)
	db.session.add(l)
	db.session.commit()
	return jsonify(status=True)

@app.route('/saveme',methods=['POST'])
def saveme():
	content= getjson(request)
	userid = content['user_id']
	tempid = content['template_id']
	if userid ==None or tempid==None:
		return jsonify(status=False)
	user = User.query.filter_by(uid=userid).first()
	if user == None:
		return jsonify(state=False)
	user.temp_id = int(tempid)
	db.session.commit()
	return jsonify(state=True)


@app.route('/seefriends',methods=['POST'])
def seefri():
	content= getjson(request)
	userid=content['user_id']
	friid=content['friend_id']
	check = Link.query.filter_by(u_id=userid, fri_id=friid).all()
	if check !=None:	
		userdata = User.query.filter_by(uid=userid).first()
		data={'user' :{
		 	 'user_id'      :userdata.uid
            ,'user_name'    :userdata.uname
            ,'template_id'  :userdata.temp_id
            ,'photo_url'    :userdata.pho_url
            ,'email'        :userdata.email
            ,'headline'     :userdata.headline
            ,'company'      :userdata.company
            ,'linkedin_add' :userdata.linked_add
			}}
		return jsonify(data=data)
	else:
		return jsonify(data={})

@app.route('/seeme', methods=['POST'])
def seeme():
	content = getjson(request)
	userid =content['user_id']
	userdata = User.query.filter_by(uid=userid).first()
	if userdata == None:
		return jsonify(data={})
	data = getuserdata(userdata)
	return jsonify(data=data)

def getuserdata(userdata):
	userfri = Link.query.filter_by(u_id=userdata.uid).all()
	fris = {}
	for fri in userfri:
		fris['content']={'friend_id'	:fri.fri_id
				,'friend_photo'	:fri.fri_pho
		}

	data ={'user' :{
		 	 'user_id'      :userdata.uid
            ,'user_name'    :userdata.uname
            ,'template_id'  :userdata.temp_id
            ,'photo_url'    :userdata.pho_url
            ,'email'        :userdata.email
            ,'headline'     :userdata.headline
            ,'company'      :userdata.company
            ,'linkedin_add' :userdata.linked_add
			},
			'friends': fris,
			'exist':True
	}
	return data

#@app.route('/login')
#def login():
	'''
		login method
	'''
#	return "add login method"

@app.route('/')
def hello():
	return "Hello cors"

if __name__=="__main__":
	app.run(host='0.0.0.0',debug=True)

