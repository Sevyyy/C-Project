# -*- coding: utf-8 -*-
import os.path
import time
from datetime import datetime
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import torndb

define('port', default=8000, help='run on the given port', type=int)

def get_current_term():
	m = datetime.today().month
	if 3 <= m <= 8:
		return str(datetime.today().year - 1) + '02'
	elif m < 3:
		return str(datetime.today().year - 1) + '01'
	else:
		return str(datetime.today().year) + '01'
def get_next_term():
	m = datetime.today().month 
	if 3 <= m <= 8:
		return str(datetime.today().year) + '01'
	elif m < 3:
		return str(datetime.today().year - 1) + '02'
	else:
		return str(datetime.today().year) + '02'
def get_last_term():
	m = datetime.today().month
	if 3 <= m <= 8:
		return str(datetime.today().year - 1) + '01'
	elif m < 3:
		return str(datetime.today().year - 2) + '02'
	else:
		return str(datetime.today().year - 1) + '02'
def is_date(date):
	try:
		time.strptime(date,"%Y-%m-%d")
		return True
	except:
		return False

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
		(r'/',HomePageHandler),
		(r'/student',StudentHandler),
		(r'/professor',ProfessorHandler),
		(r'/registrar',RegistrarHandler),
		(r'/changepassword',ChangePasswordHandler),
		(r'/error/([a-z]+)',ErrorHandler),
		(r'/notice',NoticeHandler),
		(r'/mpi',MPIHandler),
		(r'/mtproinfo/([a-z]+)',MtProInfoHandler),
		(r'/msi',MSIHandler),
		(r'/mtstuinfo/([a-z]+)',MtStuInfoHandler),
		(r'/mcc',MCCHandler),
		(r'/mtcoursecatalog/([a-z]+)',MtCourseCatalogHandler),
		(r'/selectcoursetoteach',SelectCourseToTeachHandler),
		(r'/registerforcourse',RegisterForCourseHandler),
		(r'/submitgrade',SubmitGradeHandler),
		(r'/viewreportcard',ViewReportCardHandler)
		]
		settings = dict(
                   template_path=os.path.join(os.path.dirname(__file__), "templates"),    
                   static_path=os.path.join(os.path.dirname(__file__), "static"),    
                   debug=True,
                   cookie_secret = 'nqPyTtY9QMCeD5wm7TEw+Vvia8hSjkiHpCCogq8WY0c=',
				   xsrf_cookies = True,
				   login_url = '/'    
                   )
		tornado.web.Application.__init__(self, handlers, **settings)
		self.db = torndb.Connection("localhost", "homework", user = "root", password = "000", charset='utf8')

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
	    return self.application.db
	def get_current_user(self):
		return 'aaa'

class HomePageHandler(BaseHandler):
	def get(self):
		self.clear_cookie('account')
		self.clear_cookie('user_type')
		tag = self.db.get('select * from close_or_not')['close']
		self.set_secure_cookie('close',str(tag))
		self.render('HomePage.html')
	def post(self):
		user_type = self.get_argument('user_type')
		account = self.get_argument('account')
		password = self.get_argument('password')
		self.set_secure_cookie('account',account)
		self.set_secure_cookie('user_type',user_type)
		if user_type == 's':
			psd = self.db.get('select password from student where student_id = %s',account)
			if psd:
				psd = psd['password']
				if psd == password:
					self.redirect('/student')
				else:
					self.redirect('/error/keyerror')
			else:
				self.redirect('/error/accounterror')
		elif user_type == 'p':
			psd = self.db.get('select password from professor where professor_id = %s',account)
			if psd:
				psd = psd['password']
				if psd == password:
					self.redirect('/professor')
				else:
					self.redirect('/error/keyerror')
			else:
				self.redirect('/error/accounterror')
		elif user_type == 'r':
			psd = self.db.get('select password from registrar where registrar_id = %s',account)
			if psd:
				psd = psd['password']
				if psd == password:
					self.redirect('/registrar')
				else:
					self.redirect('/error/keyerror')
			else:
				self.redirect('/error/accounterror')

class StudentHandler(BaseHandler):
	def get(self):
		if self.get_secure_cookie('account'):
			self.db.execute('delete from registering where account = %s',self.get_secure_cookie('account'))
			student_name = self.db.get('select name from student where student_id = %s',self.get_secure_cookie('account'))['name']
			self.render('Student.html',student_name = student_name)
		else:
			self.redirect('/error/illegallylogging')
	def post(self):
		pass

class ProfessorHandler(BaseHandler):
	def get(self):
		if self.get_secure_cookie('account'):
			self.db.execute('delete from registering where account = %s',self.get_secure_cookie('account'))
			professor_name = self.db.get('select name from professor where professor_id = %s',self.get_secure_cookie('account'))['name']
			self.render('Professor.html',professor_name = professor_name)
		else:
			self.redirect('/error/illegallylogging')
	def post(self):
		pass

class RegistrarHandler(BaseHandler):
	def get(self):
		if self.get_secure_cookie('account'):
			registrar_name = self.db.get('select name from registrar where registrar_id = %s',self.get_secure_cookie('account'))['name']
			tag = self.get_secure_cookie('close')
			self.render('Registrar.html',registrar_name = registrar_name,tag = tag)
		else:
			self.redirect('/error/illegallylogging')
	def post(self):
		if self.get_argument('op') == 'Close Registration':
			user_num = self.db.get('select count(*) as count from registering')['count']
			if user_num == 0:
				notice = self.db.query('select professor_course_id as pcid,pc.count as count from professor_course as pc,professor as p,course as c where pc.professor_id = p.professor_id and pc.course_id = c.course_id and c.term = %s',get_next_term())
				for each in notice:
					if each['count'] < 3:
						#pass
						self.db.execute('delete from professor_course where professor_course_id = %s',each['pcid'])	
				self.set_secure_cookie('close','1')
				self.db.execute('update close_or_not set close = 1')
				self.redirect('/registrar')
			else:
				self.redirect('/error/registering')
		elif self.get_argument('op') == 'Open Registration':
			self.set_secure_cookie('close','0')
			self.db.execute('update close_or_not set close = 0')
			self.redirect('/registrar')

class ChangePasswordHandler(BaseHandler):
	def get(self):
		self.render('ChangePassword.html')
	def post(self):
		newpsd = self.get_argument('newpsd')
		if self.get_secure_cookie('user_type') == 's':
			self.db.execute("update student set password = %s where student_id = %s",newpsd,self.get_secure_cookie('account'))
			self.redirect('/student')
		elif self.get_secure_cookie('user_type') == 'p':
			self.db.execute("update professor set password = %s where professor_id = %s",newpsd,self.get_secure_cookie('account'))
			self.redirect('/professor')
		elif self.get_secure_cookie('user_type') == 'r':
			self.db.execute("update registrar set password = %s where registrar_id = %s",newpsd,self.get_secure_cookie('account'))
			self.redirect('/registrar')

class ErrorHandler(BaseHandler):
	def get(self,error_type):
		self.render('Error.html',error_type = error_type)
	def post(self):
		pass

class NoticeHandler(BaseHandler):
	def get(self):
		user_type = self.get_secure_cookie('user_type')
		info = self.db.query('select p.name as pname,c.name as cname,c.day as cday,c.time as ctime,c.type as ctype from course as c,professor_course as pc,professor as p where pc.professor_id = p.professor_id and pc.course_id = c.course_id and c.term = %s',get_next_term())
		tag = self.db.get('select * from close_or_not')['close']
		self.render('Notice.html',tag = tag,info = info,user_type = user_type)
	def post(self):
		pass

class MtProInfoHandler(BaseHandler):
	def get(self,mt_type):
		self.render('MtProInfo.html',mt_type = mt_type,name='',birthday='',position='',department='',ssn='')
	def post(self,mt_type):
		if mt_type == 'addaprofessor':
			name = self.get_argument("name")
			birthday = self.get_argument("birthday")
			ssn = self.get_argument("ssn")
			position = self.get_argument("position")
			department = self.get_argument("department")
			if is_date(birthday):
				self.db.insert('insert into professor (name,birthday,position,department,ssn) values (%s,%s,%s,%s,%s)',name,birthday,position,department,ssn)
				self.redirect('/mtproinfo/addaprofessor')
			else:
				self.redirect('/error/prodateerror')
		elif mt_type == 'changeaprofessor':
			pro_id=self.get_argument('pro_id',None)
			if pro_id:
				info = self.db.get("select name,birthday,position,department,ssn from professor where professor_id = %s", pro_id)
				if info:
					self.set_secure_cookie('mpi_c_proid',pro_id)
					name = info['name']
					birthday = info['birthday']
					position = info['position']
					department = info['department']
					ssn = info['ssn']
					self.render('MtProInfo.html',mt_type=mt_type,name=name,birthday=birthday,position=position,department=department,ssn=ssn)
				else:
					self.redirect('/error/'+'cpidnotfound')
			if (self.get_argument('change',None)):
				pro_id = self.get_secure_cookie('mpi_c_proid')
				name = self.get_argument("name")
				birthday = self.get_argument("birthday")
				ssn = self.get_argument("ssn")
				position = self.get_argument("position")
				department = self.get_argument("department")
				self.clear_cookie('mpi_c_proid')
				if is_date(birthday):
					self.db.execute("update professor set name = %s,birthday = %s,position = %s,department = %s,ssn = %s where professor_id = %s",name,birthday,position,department,ssn,pro_id)
					self.redirect('/mtproinfo/changeaprofessor')
				else:
					self.redirect('/error/prodateerror')
		elif mt_type == 'deleteaprofessor':
			pro_id=self.get_argument('pro_id',None)
			if pro_id:
				info = self.db.get("select name,birthday,position,department,ssn from professor where professor_id = %s", pro_id)
				if info:
					self.set_secure_cookie('mpi_d_proid',pro_id)
					name = info['name']
					birthday = info['birthday']
					position = info['position']
					department = info['department']
					ssn = info['ssn']
					self.render('MtProInfo.html',mt_type=mt_type,name=name,birthday=birthday,position=position,department=department,ssn=ssn)
				else:
					self.redirect('/error/'+'dpidnotfound')
			if (self.get_argument('delete',None)):
				pro_id = self.get_secure_cookie('mpi_d_proid')
				self.db.execute("delete from professor where professor_id = %s",pro_id)
				self.clear_cookie('mpi_d_proid')
				self.redirect('/mtproinfo/deleteaprofessor')

class MPIHandler(BaseHandler):
	def get(self):
		self.render('MPI.html')
	def post(self):
		pass

class MtStuInfoHandler(BaseHandler):
	def get(self,mt_type):
		self.render('MtStuInfo.html',mt_type = mt_type,stu_id='',name='',birthday='',graduate_date='',department='',position='',ssn='')
	def post(self,mt_type):
		if mt_type == 'addastudent':
			name = self.get_argument("name")
			birthday = self.get_argument("birthday")
			ssn = self.get_argument("ssn")
			position = self.get_argument("position")
			graduate_date = self.get_argument("graduate_date")
			if is_date(birthday) and is_date(graduate_date):
				self.db.insert('insert into student (name,birthday,position,graduate_date,ssn) values (%s,%s,%s,%s,%s)',name,birthday,position,graduate_date,ssn)
				self.redirect('/mtstuinfo/addastudent')
			else:
				self.redirect('/error/studateerror')
		elif mt_type == 'changeastudent':
			stu_id=self.get_argument('stu_id',None)
			if stu_id:
				info = self.db.get("select name,birthday,position,graduate_date,ssn from student where student_id = %s", stu_id)
				if info:
					self.set_secure_cookie('msi_c_stuid',stu_id)
					name = info['name']
					birthday = info['birthday']
					position = info['position']
					graduate_date = info['graduate_date']
					ssn = info['ssn']
					self.render('MtStuInfo.html',mt_type=mt_type,stu_id=stu_id,name=name,birthday=birthday,position=position,graduate_date=graduate_date,ssn=ssn)
				else:
					self.redirect('/error/csidnotfound')
			if (self.get_argument('change',None)):
				stu_id = self.get_secure_cookie('msi_c_stuid')
				name = self.get_argument("name")
				birthday = self.get_argument("birthday")
				ssn = self.get_argument("ssn")
				position = self.get_argument("position")
				graduate_date = self.get_argument("graduate_date")
				self.clear_cookie('msi_c_stuid')
				if is_date(birthday) and is_date(graduate_date):
					self.db.execute("update student set name = %s,birthday = %s,position = %s,graduate_date = %s,ssn = %s where student_id = %s",name,birthday,position,graduate_date,ssn,stu_id)
					self.redirect('/mtstuinfo/changeastudent')
				else:
					self.redirect('/error/studateerror')
		elif mt_type == 'deleteastudent':
			stu_id=self.get_argument('stu_id',None)
			if stu_id:
				info = self.db.get("select name,birthday,position,graduate_date,ssn from student where student_id = %s", stu_id)
				if info:
					self.set_secure_cookie('msi_d_stuid',stu_id)
					name = info['name']
					birthday = info['birthday']
					position = info['position']
					graduate_date = info['graduate_date']
					ssn = info['ssn']
					self.render('MtStuInfo.html',mt_type=mt_type,stu_id=stu_id,name=name,birthday=birthday,position=position,graduate_date=graduate_date,ssn=ssn)
				else:
					self.redirect('/error/dsidnotfound')
			if (self.get_argument('delete')):
				stu_id = self.get_secure_cookie('msi_d_stuid')
				self.db.execute("delete from student where student_id = %s",stu_id)
				self.clear_cookie('msi_d_stuid')
				self.redirect('/mtstuinfo/deleteastudent')

class MSIHandler(BaseHandler):
	def get(self):
		self.render('MSI.html')
	def post(self):
		pass

class MtCourseCatalogHandler(BaseHandler):
	def get(self,mt_type):
		self.render('MtCourseCatalog.html',mt_type = mt_type,name='',day='',time='',term='',c_type='')
	def post(self,mt_type):
		if mt_type == 'addacourse':
			name = self.get_argument("name")
			day = self.get_argument("day")
			time = self.get_argument("time")
			term = self.get_argument("term")
			self.db.insert('insert into course (name,day,time,term) values (%s,%s,%s,%s)',name,day,time,term)
			self.redirect('/mtcoursecatalog/addacourse')
		elif mt_type == 'changeacourse':
			c_id = self.get_argument('c_id',None)
			if c_id:
				info = self.db.get('select * from course where course_id = %s',c_id)
				if info:
					self.set_secure_cookie('mcc_c_cid',c_id)
					name = info['name']
					day = info['day']
					time = info['time']
					term = info['term']
					c_type = info['type']
					self.render('MtCourseCatalog.html',mt_type = mt_type,name=name,day=day,time=time,term=term,c_type = c_type)
				else:
					self.redirect('/error/ccidnotfound')
			if (self.get_argument('change',None)):
				c_id = self.get_secure_cookie('mcc_c_cid')
				name = self.get_argument("name")
				day = self.get_argument("day")
				time = self.get_argument("time")
				term = self.get_argument("term")
				c_type = self.get_argument("type")
				self.db.execute('update course set name = %s,day = %s,time = %s,term = %s where course_id = %s',name,day,time,term,c_id)
				self.clear_cookie('mcc_c_cid')
				self.redirect('/mtcoursecatalog/changeacourse')
		elif mt_type == 'deleteacourse':
			self.render('MtCourseCatalog.html',mt_type = mt_type,name='',day='',time='',term='',c_type = '')

class MCCHandler(BaseHandler):
	def get(self):
		self.render('MCC.html')
	def post(self):
		pass

class SelectCourseToTeachHandler(BaseHandler):
	def get(self):
		close = self.db.get('select close from close_or_not')['close']
		if close == '1':
			self.redirect('/error/pclosed')
			return
		pro_id = self.get_secure_cookie('account')
		info=[]
		course_list = self.db.query('select * from course where term = %s',get_next_term())
		for each in course_list:
			temp = {}
			temp['name'] = each['name']
			temp['day'] = each['day']
			temp['time'] = each['time']
			temp['course_id'] = each['course_id']
			temp['type'] = each['type']
			course_id = each['course_id']
			pcid = self.db.get('select * from professor_course where professor_id = %s and course_id = %s',pro_id,course_id)
			if pcid:
				temp['available'] = True
				temp['pcid'] = pcid
			else:
				temp['available'] = False
				temp['pcid'] = None
			info.append(temp)
		self.db.insert('insert into registering (account) values (%s)',pro_id)
		self.render('SelectCourseToTeach.html',info = info)
	def post(self):
		pro_id = self.get_secure_cookie('account')
		cid = self.get_arguments('cid')
		course_list = self.db.query('select * from course where term = %s',get_next_term())
		dt_set = set()
		dt_dict = {}
		for each in cid:
			dt = self.db.get('select concat(c.day,c.time) as dt, c.day as cd,c.time as ct, c.name as cname from course as c where c.course_id = %s',each)
			if dt['dt'] not in dt_set:
				dt_set.add(dt['dt'])
				dt_dict[dt['dt']] = each
			else:
				# info = self.db.query('select c.name as cname,day,time from course as c where c.time = %s and c.day = %s and course_id in %s',dt['ct'],dt['cd'])
				info = []
				temp = {}
				temp['cname'] = dt['cname']
				temp['day'] = dt['cd']
				temp['time'] = dt['ct']
				info.append(temp)
				temp = {}
				c_id = dt_dict[dt['dt']]
				t = self.db.get('select c.day as cd,c.time as ct, c.name as cname from course as c where c.course_id = %s',c_id)
				temp['cname'] = t['cname']
				temp['day'] = t['cd']
				temp['time'] = t['ct']
				info.append(temp)
				self.render('conflict.html',conflict_type = 'p',info = info)
				return
				#self.redirect('/error/pcconflict',info = info)
		for i in range(len(course_list)):
			if str(course_list[i]['course_id']) in cid:
				if self.db.get('select * from professor_course where professor_id = %s and course_id = %s',pro_id,course_list[i]['course_id']) == None:
					self.db.insert('insert into professor_course (professor_id,course_id) values (%s,%s)',pro_id,course_list[i]['course_id'])
			else:
				if self.db.get('select * from professor_course where professor_id = %s and course_id = %s',pro_id,course_list[i]['course_id']):
					self.db.execute('delete from professor_course where professor_id = %s and course_id = %s',pro_id,course_list[i]['course_id'])
		self.redirect('/professor')

class SubmitGradeHandler(BaseHandler):
	def get(self):
		pro_id = self.get_secure_cookie('account')
		course = self.db.query('select name,day,time,professor_course_id from professor_course as pc,course as c where pc.course_id = c.course_id and term = %s and pc.professor_id = %s',get_last_term(),pro_id)
		self.render('SubmitGrade.html',course=course,pcid='')
	def post(self):
		pro_id = self.get_secure_cookie('account')
		pcid = self.get_argument('course',None)
		if pcid:
			self.set_secure_cookie('sg_pcid',pcid)
			course = self.db.query('select s_c_register_id as spcid,s.name as sname,score from s_c_register as spc,professor_course as pc,course as c,student as s where s.student_id = spc.student_id and spc.professor_course_id = pc.professor_course_id and pc.course_id = c.course_id and spc.professor_course_id = %s',pcid)
			self.render('SubmitGrade.html',course=course,pcid=pcid)
		if (self.get_arguments('submit',None)):
			pcid = self.get_secure_cookie('sg_pcid')
			course = self.db.query('select s_c_register_id as spcid,s.name as sname,score from s_c_register as spc,professor_course as pc,course as c,student as s where s.student_id = spc.student_id and spc.professor_course_id = pc.professor_course_id and pc.course_id = c.course_id and spc.professor_course_id = %s',pcid)
			for i in range(len(course)):
				score = self.get_argument(str(course[i]['sname']))
				self.db.execute('update s_c_register set score = %s where s_c_register_id = %s',score,course[i]['spcid'])
			self.clear_cookie('sg_pcid')
			self.redirect('/submitgrade')

class ViewReportCardHandler(BaseHandler):
	def get(self):
		stu_id = self.get_secure_cookie('account')
		score = self.db.query('select c.name as cname,score from s_c_register as spc,professor_course as pc,course as c where student_id = %s and spc.professor_course_id = pc.professor_course_id and pc.course_id = c.course_id and term = %s',stu_id,get_last_term())
		self.render('ViewReportCard.html',score = score)
	def post(self):
		pass

class RegisterForCourseHandler(BaseHandler):
	def get(self):
		close = self.db.get('select close from close_or_not')['close']
		if close == '1':
			self.redirect('/error/sclosed')
			return
		stu_id = self.get_secure_cookie('account')
		info = self.db.query('select pc.professor_course_id as pcid,p.name as pname,c.name as cname,c.day as cday,c.time as ctime,c.type as ctype,pc.count as pccount from course as c,professor_course as pc,professor as p where pc.professor_id = p.professor_id and pc.course_id = c.course_id and c.term = %s',get_next_term())
		for each in info:
			if(self.db.get('select * from s_c_save where professor_course_id = %s and student_id = %s',each['pcid'],stu_id)):
				each['save'] = True
			else:
				each['save'] = False
			if(self.db.get('select * from s_c_register where professor_course_id = %s and student_id = %s',each['pcid'],stu_id)):
				each['register'] = True
			else:
				each['register'] = False
		self.db.insert('insert into registering (account) values (%s)',stu_id)
		self.render('RegisterForCourses.html',info = info)
	def post(self):
		stu_id = self.get_secure_cookie('account')
		pcid = self.get_arguments('pcid')
		info = self.db.query('select pc.professor_course_id as pcid,p.name as pname,c.name as cname,c.day as cday,c.time as ctime,c.type as ctype,pc.count as pccount from course as c,professor_course as pc,professor as p where pc.professor_id = p.professor_id and pc.course_id = c.course_id and c.term = %s',get_next_term())
		for each in info:
			if(self.db.get('select * from s_c_save where professor_course_id = %s and student_id = %s',each['pcid'],stu_id)):
				each['save'] = True
			else:
				each['save'] = False
			if(self.db.get('select * from s_c_register where professor_course_id = %s and student_id = %s',each['pcid'],stu_id)):
				each['register'] = True
			else:
				each['register'] = False
		if self.get_argument('op') == 'save':
			for each in info:
				if str(each['pcid']) in pcid:
					if each['save'] == False:
						self.db.insert('insert into s_c_save (student_id,professor_course_id) values (%s,%s)',stu_id,each['pcid'])
				else:
					if each['save'] == True:
						self.db.execute('delete from s_c_save where student_id = %s and professor_course_id = %s',stu_id,each['pcid'])			
		elif self.get_argument('op') == 'register':
			dt_set = set()
			dt_dict = {}
			for each in pcid:
				dt = self.db.get('select c.day as cday,c.time as ctime,p.name as pname,c.name as cname,concat(c.day,c.time) as dt from professor_course as pc,course as c,professor as p where pc.professor_id = p.professor_id and pc.course_id = c.course_id and pc.professor_course_id = %s',each)
				if dt['dt'] not in dt_set:
					dt_set.add(dt['dt'])
					dt_dict[dt['dt']] = each
				else:
					info = []
					temp = {}
					temp['cname'] = dt['cname']
					temp['day'] = dt['cday']
					temp['time'] = dt['ctime']
					temp['pname'] = dt['pname']
					info.append(temp)
					temp = {}
					pc_id = dt_dict[dt['dt']]
					t = self.db.get('select p.name as pname,c.day as cday,c.time as ctime, c.name as cname from course as c,professor_course as pc,professor as p where pc.professor_id = p.professor_id and pc.course_id = c.course_id and pc.professor_course_id = %s',pc_id)
					temp['cname'] = t['cname']
					temp['day'] = t['cday']
					temp['time'] = t['ctime']
					temp['pname'] = t['pname']
					info.append(temp)
					self.render('conflict.html',info = info,conflict_type = 's')
					return
			for i in range(len(info)):
				if str(info[i]['pcid']) in pcid:
					count = self.db.get('select count from professor_course where professor_course_id = %s',info[i]['pcid'])['count']
					if count >= 10:
						course = self.db.get('select name from course as c,professor_course as pc where pc.course_id = c.course_id and professor_course_id = %s',info[i]['pcid'])['name']
						#self.redirect('/error/coursecounterror')
						self.render('coursecounterror.html',course=course)
			for each in info:
				if str(each['pcid']) in pcid:
					if each['register'] == False:
						self.db.insert('insert into s_c_register (student_id,professor_course_id) values (%s,%s)',stu_id,each['pcid'])
					if each['save'] == False:
						self.db.insert('insert into s_c_save (student_id,professor_course_id) values (%s,%s)',stu_id,each['pcid'])
				else:
					if each['register'] == True:
						self.db.execute('delete from s_c_register where student_id = %s and professor_course_id = %s',stu_id,each['pcid'])			
					if each['save'] == True:
						self.db.execute('delete from s_c_save where student_id = %s and professor_course_id = %s',stu_id,each['pcid'])			
		elif self.get_argument('op') == 'delete':
			for each in info:
				if each['save'] == True:
					self.db.execute('delete from s_c_save where student_id = %s and professor_course_id = %s',stu_id,each['pcid'])
		self.redirect('/student')

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()
	