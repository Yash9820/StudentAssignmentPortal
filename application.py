from flask import Flask, render_template,request,flash,session,url_for,redirect,session,jsonify,g,send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm,TeacherRegistrationForm,EditProfileForm,EditTeacherProfile
from flask_mail import Mail
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_mysqldb import MySQL
import MySQLdb.cursors 
from flask_bcrypt import Bcrypt
from datetime import datetime, date	

from werkzeug.utils import secure_filename
import urllib.request
import os



application = Flask(__name__)
application.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
	MAIL_USE_TLS = False,
    MAIL_USERNAME = 'studentassignmentportal12@gmail.com',
    MAIL_PASSWORD=  '181267174'
)
mail = Mail(application)
application.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://admin:admin123@studentassignment.cztg8tdyetxc.us-east-1.rds.amazonaws.com:3306/student'.format(user='admin', password='admin123', server='studentassignment.cztg8tdyetxc.us-east-1.rds.amazonaws.com', database='student')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['MYSQL_HOST'] = 'studentassignment.cztg8tdyetxc.us-east-1.rds.amazonaws.com'
application.config['MYSQL_USER'] = 'admin'
application.config['MYSQL_PASSWORD'] = 'admin123'
application.config['MYSQL_DB'] = 'student'
application.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(application) 
db = SQLAlchemy(application)
bcrypt=Bcrypt(application)


class Register(db.Model):
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Enrollment = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	Gender = db.Column(db.String(120),	nullable=False)
	birth = db.Column(db.String(12),	nullable=False)
	contact = db.Column(db.String(20),	nullable=False)
	semester = db.Column(db.String(120),	nullable=False)
	city = db.Column(db.String(120),	nullable=False)
	state = db.Column(db.String(120),	nullable=False)
	Address = db.Column(db.String(120),	nullable=False)
	pincode = db.Column(db.String(120),	nullable=False)
	password = db.Column(db.String(120),	nullable=False)
	confirm_password = db.Column(db.String(120),nullable=False)

class Teacherregister(db.Model):
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	Gender = db.Column(db.String(120),	nullable=False)
	birth = db.Column(db.String(12),	nullable=False)
	contact = db.Column(db.String(20),	nullable=False)
	department = db.Column(db.String(120),	nullable=False)
	qualifications = db.Column(db.String(120),	nullable=False)
	designation = db.Column(db.String(120),	nullable=False)
	Address = db.Column(db.String(120),	nullable=False)
	pincode = db.Column(db.String(120),	nullable=False)
	password = db.Column(db.String(120),	nullable=False)
	confirm_password = db.Column(db.String(120),nullable=False)

class Subjectdetail(db.Model):
	sname = db.Column(db.String(80),	unique=False,	nullable=False)
	scode = db.Column(db.String(80),	unique=False,	nullable=False)
	sem = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)

@application.route("/")
def home():
    return render_template('index.html')

@application.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		name = request.form.get('name')
		email = request.form.get('email')
		Enrollment = request.form.get('Enrollment')
		Gender = request.form.get('Gender')
		birth = request.form.get('birth')
		contact = request.form.get('contact')
		semester = request.form.get('semester')
		city = request.form.get('city')
		state = request.form.get('state')
		Address = request.form.get('Address')
		pincode = request.form.get('pincode')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
		entry = Register(name=name,email = email,Enrollment = Enrollment,Gender = Gender,birth= birth,contact=contact,semester = semester,city = city,state = state,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password)
		db.session.add(entry)
		db.session.commit()
		flash(f'Account created for {form.email.data}!', 'success')
		return redirect(url_for('register'))
	return render_template('register.html', title='Register', form=form)

@application.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		email=request.form.get('email')
		password1 = request.form.get('password')
		#secure_password = bcrypt.generate_password_hash('password').decode('utf-8')
		#secure_pass = sha256_crypt.verify("password",secure_password)
		#secure_pass=bcrypt.check_password_hash(secure_password,password)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM register WHERE email = % s ', [email])    
		if result>0:
			register = cursor.fetchone()
			password=register['password']
			if bcrypt.check_password_hash(password,password1):
				session['loggedin']=True
				session['email']=register['email'] 
				session['name']=register['name']
				session['Enrollment']=register['Enrollment']
				session['Gender']=register['Gender']
				session['birth']=register['birth']
				session['contact']=register['contact']
				session['semester']=register['semester']
				session['city']=register['city']
				session['state']=register['state']
				session['Address']=register['Address']
				session['pincode']=register['pincode']
				flash('You have been logged in!', 'success')
				return redirect(url_for('stsignup'))
				cursor.close() 
			else:
				flash('Password is incorrect','danger')
		else: 
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@application.route("/stsignup")
def stsignup():
	if g.email:
		return render_template('/StudentLogin/index.html',email=session['email'],name=session['name'],Enrollment=session['Enrollment'],Gender=session['Gender'],birth=session['birth'],contact=session['contact'],semester=session['semester'],city=['city'],state=session['state'],Address=session['Address'],pincode=session['pincode'])
	return redirect(url_for('login'))

@application.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
	if g.email:
		form = EditProfileForm(request.form)
		if form.validate_on_submit():
			session['email'] = form.email.data
			session['name'] = form.name.data
			session['Enrollment'] = form.Enrollment.data
			session['Gender'] = form.Gender.data
			session['birth'] = form.birth.data
			session['contact'] = form.contact.data
			session['semester'] = form.semester.data
			session['city'] = form.city.data
			session['state'] = form.state.data
			session['Address'] = form.Address.data
			session['pincode'] = form.pincode.data
		elif request.method == 'GET':
			form.email.data = session['email']
			form.name.data = session['name']
			form.Enrollment.data = session['Enrollment']
			form.Gender.data = session['Gender']
			form.contact.data = session['contact']
			form.semester.data = session['semester']
			form.city.data = session['city']
			form.state.data = session['state']
			form.Address.data = session['Address']
			form.pincode.data = session['pincode']
		return render_template('/StudentLogin/edit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('login'))

@application.route('/teacher_edit_profile', methods=['GET', 'POST'])
def teacher_edit_profile():
	if g.email:
		form = EditTeacherProfile(request.form)
		if form.validate_on_submit():
			g.email = form.email.data
			session['name'] = form.name.data
			session['Tid'] = form.Tid.data
			session['Gender'] = form.Gender.data
			session['birth'] = form.birth.data
			session['contact'] = form.contact.data
			session['department'] = form.department.data
			session['qualifications'] = form.qualifications.data
			session['designation'] = form.designation.data
			session['Address'] = form.Address.data
			session['pincode'] = form.pincode.data
		elif request.method == 'GET':
			form.email.data = g.email
			form.name.data = session['name']
			form.Tid.data = session['Tid']
			form.Gender.data = session['Gender']
			form.contact.data = session['contact']
			form.department.data = session['department']
			form.qualifications.data=session['qualifications']
			form.designation.data=session['designation']
			form.Address.data = session['Address']
			form.pincode.data = session['pincode']
		return render_template('/TeacherAdmin/tedit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('teacherlogin'))


@application.route("/logout3")
def logout3():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@application.route("/teacherlogin", methods=['GET', 'POST'])
def teacherlogin():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		email=request.form.get('email')
		password1 = request.form.get('password')
		#secure_password = bcrypt.generate_password_hash('password').decode('utf-8')
		#secure_pass = sha256_crypt.verify("password",secure_password)
		#secure_pass=bcrypt.check_password_hash(secure_password,password)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		result=cursor.execute('SELECT * FROM teacherregister WHERE email = % s ', [email])    
		if result>0:
			register = cursor.fetchone()
			password=register['password']
			if bcrypt.check_password_hash(password,password1):
				session['loggedin']=True
				session['email']=register['email'] 
				session['name']=register['name'] 
				session['Tid']=register['Tid']
				session['Gender']=register['Gender']
				session['birth']=register['birth']
				session['contact']=register['contact']
				session['department']=register['department']
				session['qualifications']=register['qualifications']
				session['designation']=register['designation']
				session['Address']=register['Address']
				session['pincode']=register['pincode']
				flash('You have been logged in!', 'success')
				return redirect(url_for('teachersignup'))
				cursor.close() 
			else:
				flash('Password is incorrect','danger')
		else: 
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('teacherlogin.html', title='Login', form=form)
	
@application.route("/teachersignup")
def teachersignup():
	if g.email:
		return render_template('/TeacherAdmin/index.html',email=session['email'],name=session['name'],Tid=session['Tid'],Gender=session['Gender'],birth=session['birth'],contact=session['contact'],department=session['department'],qualifications=session['qualifications'],designation=session['designation'],Address=session['Address'],pincode=session['pincode'])
	return redirect(url_for('teacherlogin'))

@application.route("/logout2")
def logout2():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@application.route('/logout')
def logout():
	logout_user()
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('login'))


@application.route("/contact")
def contact():
    return render_template('contact.html')



@application.route("/adminlogin",methods =['GET', 'POST'])
def adminlogin():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate_on_submit() and 'email' in request.form and 'password' in request.form:
		session.pop('email', None)
		email=request.form.get('email')
		password = request.form.get('password')
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
		cursor.execute('SELECT * FROM admin WHERE email = % s AND password = % s', (email, password, )) 
		account = cursor.fetchone() 
		if account: 
			session['loggedin'] = True
			session['id'] = account['id'] 
			session['email'] = account['email'] 
			flash('You have been logged in!', 'success')
			return redirect(url_for('admindash'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('adminlogin.html',title='Login', form=form)

@application.route("/admindash")
def admindash():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('select count(email)  FROM register')
		result1=cur.execute('select count(email)  FROM teacherregister')
		result2=cur.execute('select count(scode)  FROM subjectdetail')
		result3=cur.execute('select count(id)  FROM crassignment')
		return render_template('/ADMIN/index.html',email=session['email'],data=result,data1=result1,data2=result2,data3=result3)
	return redirect(url_for('adminlogin'))


@application.before_request
def before_request():
	g.email=None
	if 'email' in session:
		g.email=session['email']

@application.route('/logout1')
def logout1():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('adminlogin'))
	
@application.route("/teacheregister",methods =['GET', 'POST'])
def teacheregister():
	form = TeacherRegistrationForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		name = request.form.get('name')
		email = request.form.get('email')
		Tid = request.form.get('Tid')
		Gender = request.form.get('Gender')
		birth = request.form.get('birth')
		contact = request.form.get('contact')
		department = request.form.get('department')
		qualifications = request.form.get('qualifications')
		designation = request.form.get('designation')
		Address = request.form.get('Address')
		pincode = request.form.get('pincode')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		secure_password = bcrypt.generate_password_hash(password).decode('utf-8')
		entry = Teacherregister(name=name,email = email,Tid = Tid,Gender = Gender,birth= birth,contact=contact,department = department,qualifications = qualifications,designation = designation,Address = Address,pincode = pincode,password = secure_password,confirm_password=secure_password)
		db.session.add(entry)
		db.session.commit()
		flash(f'Account created for {form.email.data}!', 'success')
		return redirect(url_for('teacheregister'))
	return render_template('teachergister.html',title='Teacherregister', form=form)



@application.route("/about")
def about():
    return render_template('about.html')


@application.route('/Addsubject',methods=["POST","GET"])
def Addsubject():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute("SELECT * FROM teacherregister ORDER BY Tid")
		carbrands = cur.fetchall()
		if request.method=='POST' :
			sname = request.form.get('sname')
			scode = request.form.get('scode')
			sem = request.form.get('sem')
			Tid = request.form.get('Tid')
			name = request.form.get('name')
			email = request.form.get('email')
			Add = Subjectdetail(sname=sname,scode=scode,sem=sem,Tid=Tid,name=name,email=email)
			db.session.add(Add)
			db.session.commit()
			mail.send_message('New message from Student Assignment Submission Portal' ,
                          sender='studentassignmentportal12@gmail.com',
                          recipients =[email] ,
                           body ="Your Subject Name is:--" + sname +"\t Subjet Code Is:" + scode +"\t for Semester:-- "  +  sem  + "\n And Your Professor Id is \t" + Tid
                          )
			flash(f'Subject Details are Successfully Added !', 'success')
		return render_template('/ADMIN/blank.html',carbrands=carbrands)
	return redirect(url_for('adminlogin'))		
 
@application.route("/carbrand",methods=["POST","GET"])
def carbrand():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM teacherregister WHERE Tid = %s ORDER BY Tid ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
                'name': row['name'],
                'email': row['email']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

@application.route("/studentprofile", methods=['GET', 'POST'])
def studentprofile():
	if g.email:
		form = RegistrationForm(request.form)
		return render_template('/StudentLogin/profile.html', title='Register', form=form)
	return redirect(url_for('login'))

@application.route("/teacherprofile", methods=['GET', 'POST'])
def teacherprofile():
	if g.email:
		form = TeacherRegistrationForm(request.form)
		return render_template('/TeacherAdmin/tprofile.html', title='Register', form=form)
	return redirect(url_for('teacherlogin'))

@application.route('/createassignment',methods=["POST","GET"])
def createassignment():
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result = cur.execute("SELECT * FROM subjectdetail ORDER BY Tid")
		carbrands = cur.fetchall()
		return render_template('/TeacherAdmin/CreateAssignment.html',carbrands=carbrands)
	return redirect(url_for('teacherlogin'))

@application.route("/crassignment",methods=["POST","GET"])
def crassignment():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM subjectdetail WHERE Tid = %s ORDER BY Tid ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
				'sname': row['sname'],
                'name': row['name'],
                'email': row['email'],
				'sem':row['sem']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

@application.route("/crassignment1",methods=["POST","GET"])
def crassignments():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        print(category_id)
        result = cur.execute("SELECT * FROM subjectdetail WHERE sem = %s ORDER BY sem ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'Tid': row['Tid'],
				'sname': row['sname'],
                'name': row['name'],
                'email': row['email'],
				'sem':row['sem']}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

@application.route('/showstudent')
def showstudent():
	cursor = mysql.connection.cursor()
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM register')
	data = cur.fetchall()
	cur.close()
	return render_template('/ADMIN/showstudent.html', employee = data)

@application.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
	form = EditProfileForm(request.form)
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM register WHERE id = %s', (id,))
	data = cur.fetchall()
	cur.close()
	print(data[0])
	return render_template('/ADMIN/edit_student.html', employee = data[0],form=form)
 
@application.route('/update/<id>', methods=['POST'])
def update_employee(id):
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		Enrollment = request.form['Enrollment']
		Gender = request.form['Gender']
		birth = request.form['birth']
		contact = request.form['contact']
		semester = request.form['semester']
		city = request.form['city']
		state = request.form['state']
		Address = request.form['Address']
		pincode = request.form['pincode']
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("""
       UPDATE register
       SET name = %s,email = %s,Enrollment=%s,Gender=%s,birth=%s,contact = %s,semester=%s,city=%s,state=%s,Address=%s,pincode=%s
       WHERE id = %s
    """, (name, email,Enrollment,Gender,birth,contact,semester,city,state,Address,pincode, id))
		flash('Student Data Updated Successfully')
		
		return redirect(url_for('showstudent'))
 
@application.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM register WHERE id = {0}'.format(id))
    flash('Student Data Removed Successfully')
    return redirect(url_for('showstudent'))

UPLOAD_FOLDER = './static/upassig/'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc','docx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Crassignment(db.Model):
	stitle = db.Column(db.String(80),	unique=False,	nullable=False)
	amark = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(80),	unique=False,	nullable=False)
	sname = db.Column(db.String(80),	unique=False,	nullable=False)
	email = db.Column(db.String(80),	unique=True,	primary_key=True,	nullable=False)
	Tid = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	pdpart = db.Column(db.String(1000),	unique=False,	nullable=False)
	ddate = db.Column(db.String(12),	nullable=False)
	sdate = db.Column(db.String(12),	nullable=False)
	sem = db.Column(db.String(120),	nullable=False)
	file = db.Column(db.String(150))
	adescription = db.Column(db.String(200), nullable=False)
	data=db.Column(db.LargeBinary)

@application.route('/crassign',methods=['POST'])
def crassign():
	if g.email:
		if request.method=='POST':
			file=request.files['inputFile']
			filename=secure_filename(file.filename)
			name = request.form.get('name')
			sname = request.form.get('sname')
			stitle = request.form.get('stitle')
			email = request.form.get('email')
			Tid = request.form.get('Tid')
			pdpart = request.form.get('pdpart')
			ddate = request.form.get('ddate')
			sdate = request.form.get('sdate')
			amark = request.form.get('amark')
			sem = request.form.get('sem')
			adescription = request.form.get('adescription')
			if file and allowed_file(file.filename):
				file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
				newassign=Crassignment(stitle=stitle,Tid=Tid,pdpart=pdpart,sem=sem,sname=sname,name=name,email=email,file=file.filename,sdate=sdate,ddate=ddate,adescription=adescription,amark=amark,data=file.read())
				db.session.add(newassign)
				db.session.commit()
				flash('Assignment Successfully created') 
				return redirect(url_for('createassignment'))
			else:
				flash('Invalid Uplaod only txt, pdf, doc,docx') 
		return redirect(url_for('createassignment'))
	return redirect(url_for('teacherlogin'))

@application.route("/showassignment", methods=['GET', 'POST'])
def showassignment():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM subjectdetail')
		data = cur.fetchall()
		cur.close()	
		return render_template('/StudentLogin/showassign.html',showst = data)
	return redirect(url_for('login'))



@application.route('/view/<string:sname>', methods = ['POST','GET'])
def viewassignment(sname):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM crassignment WHERE sname = %s',(sname,))
		data = cur.fetchall()
		cur.close()
		return render_template('/StudentLogin/showassignsubject.html',showstsb = data,datetime = date.today())
	return redirect(url_for('login'))

@application.route('/viewassignmentsb/<string:id>', methods = ['POST','GET'])
def viewassignmentsb(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM crassignment WHERE id = %s',(id,))
		data = cur.fetchall()
		cur.close()
		return render_template('/StudentLogin/viewfullassign.html',showstsb = data)
	return redirect(url_for('login'))

@application.route('/down/<file>', methods = ['GET'])
def down(file):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('select * FROM crassignment WHERE file = %s',(file,))
		data = cur.fetchall()
		cur.close()
		file_path = UPLOAD_FOLDER + file
		return send_file(file_path, as_attachment=True, attachment_filename='')
		#return send_file(BytesIO(data.data),as_attachment=True,attachment_filename=data.file)
	return redirect(url_for('login'))

UPLOAD_FOLDERR = 'static/uploadanswer/'
application.config['UPLOAD_FOLDERR'] = UPLOAD_FOLDERR

class Uploadassign(db.Model):
	Enrollment = db.Column(db.String(11), 	unique=True,	primary_key=True,	nullable=False)
	sname = db.Column(db.String(80),	unique=False,	nullable=False)
	name = db.Column(db.String(200),	unique=False,	nullable=False)
	pname = db.Column(db.String(200),	unique=False,	nullable=False)
	semester = db.Column(db.String(120),	nullable=False)
	ddate = db.Column(db.String(12),	nullable=False)
	sdate = db.Column(db.String(12),	nullable=False)
	realmark = db.Column(db.String(80),	unique=False,	nullable=False)
	asmark = db.Column(db.String(80),	unique=False,	nullable=False)
	remark = db.Column(db.String(80),	unique=False,	nullable=False)
	stitle = db.Column(db.String(80),	unique=False,	nullable=False)
	asid= db.Column(db.String(80),	unique=False,	nullable=False)
	uploaddate = db.Column(db.String(12),	nullable=False)
	file = db.Column(db.String(150))

@application.route('/uploadans', methods=['GET','POST'])
def uploadans():
	if g.email:
		if request.method=='POST':
			semester=session['semester']
			pname=request.form.get('pname')
			sname = request.form.get('sname')
			id = request.form.get('id')
			asmark = request.form.get('asmark')
			remark = request.form.get('remark')
			from datetime import datetime
			now = datetime.now()
			formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
			stitle = request.form.get('stitle')
			realmark = request.form.get('realmark')
			ddate = request.form.get('ddate')
			sdate = request.form.get('sdate')
			Enrollment=session['Enrollment']
			name=session['name']
			file=request.files['inputFile']
			filename=secure_filename(file.filename)
			if file and allowed_file(file.filename):
				file.save(os.path.join(application.config['UPLOAD_FOLDERR'], filename))
				uploadassign=Uploadassign(Enrollment=session['Enrollment'],name=session['name'],semester=session['semester'],file=file.filename,uploaddate=formatted_date,sname=sname,stitle=stitle,asmark='null',remark='null',asid=id,pname=pname,sdate=sdate,ddate=ddate,realmark=realmark)
				db.session.add(uploadassign)
				db.session.commit()
				print(id)
				flash('Assignment Successfully uploaded') 
				return redirect(url_for('viewassignmentsb',id=id))
			else:
				flash('Invalid Uplaod only txt, pdf, doc,docx') 
		return render_template('/StudentLogin/viewfullassign.html')
	return redirect(url_for('login'))

@application.route("/showallassignment", methods=['GET', 'POST'])
def showallassignment():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM crassignment')
		data = cur.fetchall()
		cur.close()	
		return render_template('/TeacherAdmin/showallassign.html',showst = data)
	return redirect(url_for('teacherlogin'))

@application.route('/editassign/<id>', methods = ['POST', 'GET'])
def editassign(id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM crassignment WHERE id = %s', (id,))
	data = cur.fetchall()
	cur.close()
	print(data[0])
	return render_template('/TeacherAdmin/editallassign.html', showst = data[0])

@application.route('/deleteassign/<string:id>', methods = ['POST','GET'])
def deleteassign(id):
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('DELETE FROM crassignment WHERE id = {0}'.format(id))
	os.remove(os.path.join(application.config['UPLOAD_FOLDER'], id.filename))
	flash('Assignment Data Removed Successfully')
	return redirect(url_for('showallassignment'))

@application.route("/statusforstudent", methods=['GET', 'POST'])
def statusforstudent():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM uploadassign')
		data = cur.fetchall()
		cur.close()	
		return render_template('/StudentLogin/statusofassign.html',showstatus = data)
	return redirect(url_for('login'))

@application.route('/viewuploadans/<string:id>', methods = ['POST','GET'])
def viewuploadans(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM uploadassign WHERE id = %s',(id,))
		data = cur.fetchall()
		cur.close()
		return render_template('/StudentLogin/showuploadans.html',viewans = data)
	return redirect(url_for('login'))

@application.route('/downans/<file>', methods = ['GET'])
def downans(file):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		result=cur.execute('select * FROM uploadassign WHERE file = %s',(file,))
		data = cur.fetchall()
		cur.close()
		file_path = UPLOAD_FOLDERR + file
		return send_file(file_path, as_attachment=True, attachment_filename='')
		#return send_file(BytesIO(data.data),as_attachment=True,attachment_filename=data.file)
	return redirect(url_for('login'))

@application.route("/statusofstudent", methods=['GET', 'POST'])
def statusofstudent():
	if g.email:
		cursor = mysql.connection.cursor()
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM uploadassign')
		data = cur.fetchall()
		cur.close()	
		return render_template('/TeacherAdmin/statusofassign.html',showstatus = data)
	return redirect(url_for('teacherlogin'))

@application.route('/viewuploadansst/<string:id>', methods = ['POST','GET'])
def viewuploadansst(id):
	if g.email:
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('select * FROM uploadassign WHERE id = %s',(id,))
		data = cur.fetchall()
		cur.close()
		return render_template('/TeacherAdmin/showuploadans.html',viewans = data)
	return redirect(url_for('teacherlogin'))

@application.route('/uploadmark', methods=['GET','POST'])
def uploadmark():
	if g.email:
		if request.method=='POST':
			asmark=request.form.get('asmark')
			remark=request.form.get('remark')
			id=request.form.get('id')
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute("""
       UPDATE uploadassign
       SET asmark=%s, remark=%s
       WHERE id=%s
    """, (asmark, remark, id))
			
			cur.close()
			flash('Assignment mark uploaded') 
			return redirect(url_for('viewuploadansst',id=id))
		return render_template('/TeacherAdmin/showuploadans.html')
	return redirect(url_for('teacherlogin'))

@application.route('/updateprofilestudent', methods=['GET','POST'])
def updateprofilestudent():
	if g.email:
		if request.method=='POST':
			name = request.form.get('name')
			email = request.form.get('email')
			Enrollment = request.form.get('Enrollment')
			Enrollment=session['Enrollment']
			Gender = request.form.get('Gender')
			birth = request.form.get('birth')
			contact = request.form.get('contact')
			semester = request.form.get('semester')
			city = request.form.get('city')
			state = request.form.get('state')
			Address = request.form.get('Address')
			pincode = request.form.get('pincode')
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute("""
       UPDATE register
       SET name = %s,Gender=%s,birth=%s,contact = %s,city=%s,state=%s,Address=%s,pincode=%s
       WHERE Enrollment = %s
    """, (name,Gender,birth,contact,city,state,Address,pincode, Enrollment))
			
			cur.close()
			flash('Your Profile is successfully updated','success') 
			return redirect(url_for('edit_profile'))
		return render_template('/StudentLogin/edit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('stsignup'))

@application.route('/updateprofileteacher', methods=['GET','POST'])
def updateprofileteacher():
	if g.email:
		if request.method=='POST':
			name = request.form.get('name')
			email = request.form.get('email')
			Tid = session['Tid']
			Gender = request.form.get('Gender')
			birth = request.form.get('birth')
			contact = request.form.get('contact')
			department = request.form.get('department')
			qualifications = request.form.get('qualifications')
			designation = request.form.get('designation')
			Address = request.form.get('Address')
			pincode = request.form.get('pincode')
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cur.execute("""
       UPDATE teacherregister
       SET name = %s,Gender=%s,birth=%s,contact = %s,department=%s,qualifications=%s,designation=%s,Address=%s,pincode=%s
       WHERE Tid = %s
    """, (name,Gender,birth,contact,department,qualifications,designation,Address,pincode, Tid))
			
			cur.close()
			flash('Your Profile is successfully updated','success') 
			return redirect(url_for('teacher_edit_profile'))
		return render_template('/TeacherAdmin/tedit_profile.html', title='Edit Profile',form=form)
	return redirect(url_for('stsignup'))

@application.route('/showprofessor')
def showprofessor():
	cursor = mysql.connection.cursor()
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM teacherregister')
	data = cur.fetchall()
	cur.close()
	return render_template('/ADMIN/showprofessor.html', showprofe = data)

@application.route('/editprof/<id>', methods = ['POST', 'GET'])
def editprof(id):
	form = EditTeacherProfile(request.form)
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT * FROM teacherregister WHERE id = %s', (id,))
	data = cur.fetchall()
	cur.close()
	print(data[0])
	return render_template('/ADMIN/tedit_profile.html', showprofe = data[0],form=form)
 
@application.route('/updateprof/<id>', methods=['POST'])
def updateprof(id):
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		Tid = request.form['Tid']
		Gender = request.form['Gender']
		birth = request.form['birth']
		contact = request.form['contact']
		department = request.form['department']
		qualifications = request.form['qualifications']
		designation = request.form['designation']
		Address = request.form['Address']
		pincode = request.form['pincode']
		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("""
       UPDATE teacherregister
       SET name = %s,email = %s,Tid=%s,Gender=%s,birth=%s,contact = %s,department=%s,qualifications=%s,designation=%s,Address=%s,pincode=%s
       WHERE id = %s
    """, (name, email,Tid,Gender,birth,contact,department,qualifications,designation,Address,pincode, id))
		flash('Professor Data Updated Successfully')
		
		return redirect(url_for('showprofessor'))
 
@application.route('/deleteprof/<string:id>', methods = ['POST','GET'])
def deleteprof(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM teacherregister WHERE id = {0}'.format(id))
    flash('Professor Data Removed Successfully')
    return redirect(url_for('showprofessor'))

@application.route("/viewuploadans/logout3")
def logout4():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@application.route("/view/logout3")
def logout5():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@application.route("/viewassignmentsb/logout3")
def logout6():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.pop('Enrollment', None)
	session.pop('Gender', None)
	session.clear()
	return redirect(url_for('login'))

@application.route("/editassign/logout2")
def logout7():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@application.route("/viewuploadansst/logout2")
def logout8():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('teacherlogin'))

@application.route('/edit/logout1')
def logout9():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('adminlogin'))

@application.route('/editprof/logout1')
def logout10():
	session.pop('loggedin', None)
	session.pop('email', None)
	session.clear()
	return redirect(url_for('adminlogin'))


application.secret_key="12345678"


if __name__ == '__main__':
	application.debug = True
	application.run()

