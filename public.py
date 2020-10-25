from flask import *
from database import *
public=Blueprint('public',__name__)
@public.route('/',methods=['get','post'])
def home():
	return render_template('index.html')

@public.route('/login',methods=['get','post'])
def login():
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'"%(username,password)
		res=select(q)
		if res:
			session['log_id']=res[0]['login_id']
			if res[0]['usertype']=="admin":
				return redirect(url_for('admin.adminhome'))
				flash("Login Successfully")
		else:
			flash("Invalid username and password")							
	return render_template('login.html')	