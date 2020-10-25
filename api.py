from flask import Blueprint,request
from database import *
import demjson
import uuid

api=Blueprint('api',__name__)

@api.route('/login/',methods=['get','post'])
def login():
	data={}
	username=request.args['username']
	password=request.args['password']
	q="select * from login where  username='%s' and password='%s'" %(username,password)
	res=select(q)
	if res:
		if res[0]['usertype']=="staff":
			q1="select * from staff where status='Accept' and login_id='%s'" %(res[0]['login_id'])
			res1=select(q1)
			data['data']=res
			data['status']="success"
		elif res[0]['usertype']=="student":
			q1="select * from student where status='Accept' and login_id='%s'" %(res[0]['login_id'])
			res1=select(q1)
			data['data']=res
			data['status']="success"
		else:
			data['status']="NA"

	else:
		data['status']="failed"
	return  demjson.encode(data)

@api.route('/viewdepart/',methods=['get','post'])
def viewdepart():
	data={}
	q="select * from department"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewdepart"
	return  demjson.encode(data)

@api.route('/addteacher/',methods=['get','post'])
def addteacher():
	data={}
	did=request.args['dept']
	fname=request.args['fname']
	lname=request.args['lname']
	hname=request.args['hname']
	place=request.args['place']
	gender=request.args['gender']
	contact=request.args['contact']
	email=request.args['email']
	qualification=request.args['quali']
	username=request.args['username']
	password=request.args['password']
	q="select * from login where username='%s' and password='%s'" %(username,password)
	print(q)
	result=select(q)
	if len(result)>0:
		data['status'] ="ae"
	else:
		q="insert into login values(null,'%s','%s','pending')"%(username,password)
		res=insert(q)
		q="insert into staff values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','pending')"%(res,did,fname,lname,hname,place,gender,contact,email,qualification)
		insert(q)
		data['status'] ="success"
	
	data['method']="addteacher"
	return demjson.encode(data)

@api.route('/tviewstudents/',methods=['get','post'])
def tviewstudents():
	data={}
	types=request.args['type']
	q="select *,concat(fname,' ',lname)as NAME from student inner join course using(course_id) where status='%s'" %(types)
	res=select(q)
	data['status'] ="success"
	data['data']=res
	data['method']="tviewstudents"
	return demjson.encode(data)

@api.route('/taorrstudent/',methods=['get','post'])
def taorrstudent():
	data={}
	action=request.args['type']
	id=request.args['id']

	if action=="accept":
		q="update student set status='accept' where student_id='%s'" %(id)
		update(q)
		q="update login set usertype='student' where login_id=(select login_id from student where student_id='%s')" %(id)
		update(q)

	if action=="reject":
		q="update student set status='reject' where student_id='%s'" %(id)
		update(q)
		q="update login set usertype='pending' where login_id=(select login_id from student where student_id='%s')" %(id)
		update(q)
		
	data['status'] ="success"
	data['method']="taorrstudent"
	return demjson.encode(data)
	

@api.route('/viewcourse/',methods=['get','post'])
def viewcourse():
	data={}
	q="select * from course"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewcourse"
	return  demjson.encode(data)

@api.route('/addstudent/',methods=['get','post'])
def addstudent():
	data={}
	cid=request.args['course']
	fname=request.args['fname']
	lname=request.args['lname']
	hname=request.args['hname']
	place=request.args['place']
	gender=request.args['gender']
	contact=request.args['contact']
	email=request.args['email']
	username=request.args['username']
	password=request.args['password']
	q="select * from login where username='%s' and password='%s'" %(username,password)
	print(q)
	result=select(q)
	if len(result)>0:
		data['status'] ="ae"
	else:
		q="insert into login values(null,'%s','%s','pending')"%(username,password)
		res=insert(q)
		q="insert into student values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','pending')"%(res,cid,fname,lname,hname,place,gender,contact,email)
		insert(q)
		data['status'] ="success"
	data['method'] ="addstudent"
	return demjson.encode(data)

@api.route('/tviewleacturenote/',methods=['get','post'])
def tviewleacturenote():
	data={}
	logid=request.args['logid']
	
	q="select * from voice_notes where staff_id=(select staff_id from staff where login_id='%s')" %(logid)
	res=select(q)
	print(res)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="tviewleacturenote"
	return  demjson.encode(data)



@api.route('/insertAudio/',methods=['get','post'])
def insertAudio():
	data={}
	
	sub = request.args['sub']
	name = request.args['name']
	text = request.args['text']
	uid = request.args['uid'] 	

	
	q = "insert into voice_notes values(null,(select staff_id from staff where login_id='%s'),'%s','%s','0',curdate())" % (uid,sub,text)
	insert(q)
	
	data['status'] ="success"
	data['method']="insertAudio"
	return demjson.encode(data)

@api.route('/updatenote/',methods=['get','post'])
def updatenote():
	data={}
	
	subject = request.args['subject']
	note = request.args['note']
	nid = request.args['nid']
	
	q = "update voice_notes set title='%s',notes='%s' where voice_note_id='%s'" % (subject,note,nid)
	
	print(q)
	update(q)
	
	data['status'] ="success"
	data['method']="updatenote"
	return demjson.encode(data)



@api.route('/uploadfile/',methods=['get','post'])
def uploadfile():
	data={}
	image = request.files['image']
	document = request.form['document']
	logid = request.form['logid']

	path="static/uploads/"+str(uuid.uuid4())+image.filename
	image.save(path)
	q = "insert into documents values(null,(select staff_id from staff where login_id='%s'),'%s','%s','0',curdate())" % (logid,document,path)
	print(q)
	login_id = insert(q)
	data['status'] = 'success'
	data['method']="uploadfile"
	return demjson.encode(data)

@api.route('/tviewnotification/',methods=['get','post'])
def tviewnotification():
	data={}
	logid=request.args['logid']
	
	q="select * from notification where staff_id=(select staff_id from staff where login_id='%s')" %(logid)
	res=select(q)
	print(res)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="tviewnotification"
	return  demjson.encode(data)

@api.route('/addnotification/',methods=['get','post'])
def addnotification():
	data={}
	
	subject = request.args['subject']
	content = request.args['content']
	logid = request.args['logid'] 
	
	q = "insert into notification values(null,(select staff_id from staff where login_id='%s'),'%s','%s',curdate())" % (logid,subject,content)
	insert(q)
	
	data['status'] ="success"
	data['method']="addnotification"
	return demjson.encode(data)

@api.route('/tvqueries/',methods=['get','post'])
def tvqueries():
	data={}
	logid=request.args['logid']
	
	q="select *,concat(fname,' ',lname)as stname from enquiry inner join student using(student_id) where staff_id=(select staff_id from staff where login_id='%s')" %(logid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="tvqueries"
	return  demjson.encode(data)


@api.route('/tansqueries/',methods=['get','post'])
def tansqueries():
	data={}
	
	answers = request.args['answers']
	enqid = request.args['enqid']
	
	q = "update enquiry set answer='%s' where enquiry_id='%s'" % (answers,enqid)
	update(q)
	
	data['status'] ="success"
	data['method']="tansqueries"
	return demjson.encode(data)

@api.route('/sviewleacturenote/',methods=['get','post'])
def sviewleacturenote():
	data={}
	
	q="select *,concat(fname,' ',lname)as sname from voice_notes inne join staff using(staff_id)"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="sviewleacturenote"
	return  demjson.encode(data)

@api.route('/sviewleacturenotes/',methods=['get','post'])
def sviewleacturenotes():
	data={}
	search=request.args['search']
	search=search+"%"
	q="select *,concat(fname,' ',lname)as sname from voice_notes inne join staff using(staff_id) where title like '%s'" %(search)
	print(q)
	res=select(q)
	print(res)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="sviewleacturenotes"
	return  demjson.encode(data)

@api.route('/viewteacher/',methods=['get','post'])
def viewteacher():
	data={}
	
	q="select *,concat(fname,' ',lname)as sname from staff inner join department on staff.deptid=department.department_id"
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewteacher"
	return  demjson.encode(data)

@api.route('/viewteachers/',methods=['get','post'])
def viewteachers():
	data={}
	search=request.args['search']
	search=search+"%"
	q="select *,concat(fname,' ',lname)as sname from staff inner join department on staff.deptid=department.department_id where fname like '%s'" %(search)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewteachers"
	return  demjson.encode(data)

@api.route('/viewqueries/',methods=['get','post'])
def viewqueries():
	data={}
	sid=request.args['sid']
	logid=request.args['logid']
	q="select * from enquiry where staff_id='%s' and student_id=(select student_id from student where login_id='%s')" %(sid,logid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewqueries"
	return  demjson.encode(data)

@api.route('/addqueries/',methods=['get','post'])
def addqueries():
	data={}
	
	query = request.args['query']
	sid=request.args['sid']
	logid=request.args['logid']
	
	q = "insert into enquiry values(null,(select student_id from student where login_id='%s'),'%s','%s','pending',curdate())" % (logid,sid,query)
	insert(q)
	
	data['status'] ="success"
	data['method']="addqueries"
	return demjson.encode(data)

@api.route('/sviewnotification/',methods=['get','post'])
def sviewnotification():
	data={}
	logid=request.args['logid']
	
	q="select *,concat(fname,' ',lname)as sname from notification inner join staff using(staff_id) "
	res=select(q)
	print(res)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="sviewnotification"
	return  demjson.encode(data)


@api.route('/viewfeedback/',methods=['get','post'])
def viewfeedback():
	data={}
	sid=request.args['sid']
	logid=request.args['logid']
	q="select * from feedbacks where staff_id='%s' and student_id=(select student_id from student where login_id='%s')" %(sid,logid)
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewfeedback"
	return  demjson.encode(data)

@api.route('/addfeedback/',methods=['get','post'])
def addfeedback():
	data={}
	
	query = request.args['query']
	sid=request.args['sid']
	logid=request.args['logid']
	
	q = "insert into feedbacks values(null,(select student_id from student where login_id='%s'),'%s','%s',curdate())" % (logid,sid,query)
	insert(q)
	
	data['status'] ="success"
	data['method']="addfeedback"
	return demjson.encode(data)


@api.route('/viewdmaterials/',methods=['get','post'])
def viewdmaterials():
	data={}
	uid=request.args['logid']
	q="select *,concat(fname,' ',lname)as sname from documents inner join staff using(staff_id)" 
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewdmaterials"
	return  demjson.encode(data)


@api.route('/noofdocdownload/',methods=['get','post'])
def noofdocdownload():
	data={}
	
	doc_id = request.args['doc_id']
	
	q = "update documents set download_count=download_count+1 where document_id='%s'" % (doc_id)
	update(q)
	
	data['status'] ="success"
	data['method']="noofdocdownload"
	return demjson.encode(data)


@api.route('/studentrate/',methods=['get','post'])
def studentrate():
	data={}
	
	rate = request.args['rate']
	nid=request.args['nid']
	logid=request.args['logid']
	
	q="update voice_notes set count=count+1 where voice_note_id='%s'" % (nid)
	update(q)
	q = "insert into rating values(null,(select student_id from student where login_id='%s'),'%s','%s',curdate())" % (logid,nid,rate)
	insert(q)
	
	data['status'] ="success"
	data['method']="studentrate"
	return demjson.encode(data)

@api.route('/chat/',methods=['get','post'])
def chat():
	data={}
	
	sid = request.args['sid']
	rid = request.args['rid']
	chat = request.args['chat']
	types = request.args['type']

	if types=="student":
		q = "insert into chat values(null,'%s',(select login_id from staff where staff_id='%s'),'%s',curdate())" % (sid,rid,chat)
		login_id = insert(q)
	elif types=="staff":
		q = "insert into chat values(null,'%s',(select login_id from student where student_id='%s'),'%s',curdate())" % (sid,rid,chat)
		login_id = insert(q)
	
	data['status'] = 'success'
	data['method']="chat"
	return demjson.encode(data)

@api.route('/viewchat/',methods=['get','post'])
def viewchat():
	data={}
	
	sid = request.args['sid']
	rid = request.args['rid']
	types = request.args['type']

	if types=="student":
		q="SELECT * FROM chat WHERE sender_id='%s' AND receiver_id=(select login_id from staff where staff_id='%s') OR sender_id=(select login_id from staff where staff_id='%s') AND receiver_id='%s'" %(sid,rid,rid,sid)
		res=select(q)
	elif types=="staff":
		q="SELECT * FROM chat WHERE sender_id='%s' AND receiver_id=(select login_id from student where student_id='%s') OR sender_id=(select login_id from student where student_id='%s') AND receiver_id='%s'" %(sid,rid,rid,sid)
		res=select(q)
	print(res)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="viewchat"
	return  demjson.encode(data)


@api.route('/Viewstudents/',methods=['get','post'])
def Viewstudents():
	data={}
	
	logid=request.args['logid']
	q="SELECT  *,concat(fname,' ',lname) as sname FROM  student "
	res=select(q)
	print(res)
	if res:
		data['status']="success"
		data['data']=res
	else:
		data['status']="failed"
	data['method']="Viewstudents"
	return  demjson.encode(data)


