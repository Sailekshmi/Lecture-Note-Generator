from flask import *
from database import *
admin=Blueprint('admin',__name__)
@admin.route('/adminhome',methods=['get','post'])
def adminhome():
	return render_template('adminhome.html')

@admin.route('/admanagedep',methods=['get','post'])
def admanagedep():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=="update":
		q="select * from department where department_id='%s'" %(id)
		res=select(q)
		data['updepartment']=res
	if action=="delete":
		q="delete from department where department_id='%s'" %(id)
		delete(q)
		return redirect(url_for('admin.admanagedep'))
	if 'submit' in request.form:
		depname=request.form['dep']
		q="insert into department values(null,'%s')"%(depname)
		insert(q)
		return redirect(url_for('admin.admanagedep'))
	if 'update' in request.form:
		depname=request.form['dep']
		q="update department set department_name='%s' where department_id='%s'"%(depname,id)
		update(q)
		return redirect(url_for('admin.admanagedep'))
	q="select * from department"
	res=select(q)
	data['deps']=res	
	return render_template('admanagedepartment.html',data=data)	

@admin.route('/admanagecourse',methods=['get','post'])
def admanagecourse():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None
	if action=="update":
		q="select * from course where course_id='%s'" %(id)
		res=select(q)
		data['upcourse']=res
		q="SELECT department_id,department_name,(department_id='%s') AS sel FROM department ORDER BY sel DESC, department_id  ASC " %(res[0]['department_id'])
		res=select(q)
		data['udepart']=res
	if action=="delete":
		q="delete from course where course_id='%s'" %(id)
		delete(q)
		return redirect(url_for('admin.admanagecourse'))
	if 'submit' in request.form:
		did=request.form['dept']
		course=request.form['course']
		noofseats=request.form['noofseats']
		duration=request.form['duration']
		q="insert into course values(null,'%s','%s','%s','%s')"%(did,course,noofseats,duration)
		insert(q)
		return redirect(url_for('admin.admanagecourse'))
	if 'update' in request.form:
		did=request.form['dept']
		course=request.form['course']
		noofseats=request.form['noofseats']
		duration=request.form['duration']
		q="update course set department_id='%s',course_name='%s',noofseats='%s',duration='%s' where course_id='%s'"%(did,course,noofseats,duration,id)
		update(q)
		return redirect(url_for('admin.admanagecourse'))
	q="SELECT * FROM department"
	res=select(q)
	data['depart']=res
	q="select * from course inner join department using(department_id)"
	res=select(q)
	data['course']=res	
	return render_template('admangecourse.html',data=data)	

@admin.route('/adviewstaff',methods=['get','post'])
def adviewstaff():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		id=request.args['id']
	else:
		action=None

	if action=="accept":
		q="update staff set status='accept' where staff_id='%s'" %(id)
		update(q)
		q="update login set usertype='staff' where login_id=(select login_id from staff where staff_id='%s')" %(id)
		update(q)
		return redirect(url_for('admin.adviewstaff'))

	if action=="reject":
		q="update staff set status='reject' where staff_id='%s'" %(id)
		update(q)
		q="update login set usertype='pending' where login_id=(select login_id from staff where staff_id='%s')" %(id)
		update(q)
		return redirect(url_for('admin.adviewstaff'))


	q="select *,concat(fname,' ',lname)as NAME from staff inner join department on deptid=department_id"
	res=select(q)
	data['teachers']=res
	return render_template('adviewstaff.html',data=data)

@admin.route('/adviewstudent',methods=['get','post'])
def adviestudent():
	data={}
	q="select *,concat(fname,' ',lname)as NAME from student inner join course using(course_id) "
	res=select(q)
	data['student']=res	
	return render_template('adviewstudent.html',data=data)

# @admin.route('/admanagestaff',methods=['get','post'])
# def admanagestaff():
# 	data={}
	
# 	if 'submit' in request.form:
# 		did=request.form['dept']
# 		fname=request.form['fname']
# 		lname=request.form['lname']
# 		hname=request.form['hname']
# 		place=request.form['place']
# 		gender=request.form['gender']
# 		contact=request.form['contact']
# 		email=request.form['email']
# 		qualification=request.form['quali']
# 		username=request.form['username']
# 		password=request.form['password']
# 		q="select * from login where username='%s' and password='%s'" %(username,password)
# 		print(q)
# 		result=select(q)
# 		if len(result)>0:
# 			flash("That username and password is already exist")
# 		else:
# 			q="insert into login values(null,'%s','%s','staff')"%(username,password)
# 			res=insert(q)
# 			q="insert into staff values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,did,fname,lname,hname,place,gender,contact,email,qualification)
# 			insert(q)
# 			flash("Registration Successful")
# 	q="select *,concat(fname,' ',lname)as NAME from staff inner join department on deptid=department_id"
# 	res=select(q)
# 	data['teachers']=res	
# 	q="select * from department"
# 	res=select(q)
# 	data['deps']=res
# 	return render_template('admanagestaff.html',data=data)

# @admin.route('/admanagestudent',methods=['get','post'])
# def admanagestudent():
# 	data={}
	
# 	if 'submit' in request.form:
# 		cid=request.form['course']
# 		fname=request.form['fname']
# 		lname=request.form['lname']
# 		hname=request.form['hname']
# 		place=request.form['place']
# 		gender=request.form['gender']
# 		contact=request.form['contact']
# 		email=request.form['email']
# 		username=request.form['username']
# 		password=request.form['password']
# 		q="select * from login where username='%s' and password='%s'" %(username,password)
# 		print(q)
# 		result=select(q)
# 		if len(result)>0:
# 			flash("That username and password is already exist")
# 		else:
# 			q="insert into login values(null,'%s','%s','student')"%(username,password)
# 			res=insert(q)
# 			q="insert into student values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,cid,fname,lname,hname,place,gender,contact,email)
# 			insert(q)
# 			flash("Registration Successful")
# 	q="select *,concat(fname,' ',lname)as NAME from student inner join course using(course_id) "
# 	res=select(q)
# 	data['student']=res	
# 	q="select * from course"
# 	res=select(q)
# 	data['course']=res
# 	return render_template('admanagestudent.html',data=data)

@admin.route('/adviewfeedback',methods=['get','post'])
def adviewfeedback():
	data={}
	q="select feedback_id,concat(student.fname,' ',student.lname)as stuname,concat(staff.fname,' ',staff.lname)as staname,descriotion,date from feedbacks inner join student using(student_id) inner join staff using(staff_id)"
	res=select(q)
	data['feedback']=res
	return render_template('adviewfeedback.html',data=data)

@admin.route('/adviewrating',methods=['get','post'])
def adviewrating():
	data={}
	q="select *,concat(student.fname,' ',student.lname)as stname from rating inner join student using(student_id) inner join voice_notes using(voice_note_id) order by ratevalue desc"
	res=select(q)
	data['rating']=res
	return render_template('adviewrating.html',data=data)

@admin.route('/adviewdownloadednotes',methods=['get','post'])
def adviewdownloadednotes():
	data={}
	q="select *,concat(staff.fname,' ',staff.lname)as stname from voice_notes inner join staff using(staff_id) order by count desc"
	res=select(q)
	data['notes']=res
	return render_template('adviewdownloadednotes.html',data=data)

@admin.route('/adviewdocuments',methods=['get','post'])
def adviewdocuments():
	data={}
	q="select *,concat(staff.fname,' ',staff.lname)as stname from documents inner join staff using(staff_id) order by download_count desc"
	res=select(q)
	data['documents']=res
	return render_template('adviewdocuments.html',data=data)

@admin.route('/viewrated',methods=['get','post'])
def viewrated():
	data={}
	id=request.args['id']
	q="select *,concat(fname,' ',lname) as sname from rating inner join student using(student_id) where voice_note_id='%s'" %(id)
	res=select(q)
	data['rated']=res
	return render_template('viewrated.html',data=data)
