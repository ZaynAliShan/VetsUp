import pymysql
import bcrypt
from flask import session
class DBHandler:
  # constructor
  def __init__(self,host,user,password,db):
    self.host = host
    self.user = user
    self.password = password
    self.db = db
    try:
      self.connection = pymysql.connect(
        host=self.host, user=self.user, password=self.password, db=self.db
      )
    except Exception as e:
      print (e)
  # destructor  
  def __del__(self):
    if self.connection != None:
      self.connection.close() 


  # funciton signup for members 
  def sign_up(self,username,email,password):
    try:
      cur = self.connection.cursor()
      query = "INSERT INTO member (m_username,m_email,m_password) VALUES (%s,%s,%s)" 
      args = (username,email,password)
      cur.execute(query,args)
      self.connection.commit()
      # reutrn ture if the members has successfully punched into DB
      return True
    except Exception as e:
      print(e)
      # return flase if records not punched in DB
      return False
    finally:
      cur.close()

  # login function
  def login(self,email,password):
    try:
      # execute query to check if admin was logged in and (to show it's own dashboard) and return
      cur = self.connection.cursor()
      query = "Select type, ad_username,ad_id from admin where ad_email = %s AND ad_password = %s"
      args = (email,password)
      cur.execute(query, args)
      data = cur.fetchall()
      if len(data) != 0:
        print(data)
        return data

      # execute query to check if receptionist was logged in and (to show it's own dashboard) and return
      query = "Select type, username, recep_id from receptionist where email = %s AND password = %s"
      args = (email,password)
      cur.execute(query, args)
      data = cur.fetchall()
      if len(data) != 0:
        return data

      # execute query to check if member was logged in and (to show it's own dashboard) and return
      # query = "Select type, m_username, m_id, from member where m_email = %s AND m_password = %s"
      print("\nin member")
      query = "Select type, m_username, m_id, m_password from member where m_email = %s"
      args = (email)
      cur.execute(query, args)
      data = cur.fetchall()
      print("\nchecking memeber",data)
      if len(data) != 0:  
        hash_pass = data[0][3]
        print("DB hashed Password:", hash_pass)
        user_encoded_pass = password.encode("utf-8")
        db_encoded_pass = hash_pass.encode("utf-8")
        if bcrypt.checkpw(user_encoded_pass, db_encoded_pass):
          print("DB data: ", data)
        else:
          return False
        return data
      return False
    except Exception as e:
      print ("in exception",e)
      return False
    finally:
      cur.close()

  # add-patient(RECEPTIONIST)
  # def addpatient(self, specie,breed,name,age,gender,date,address,phoneno,checkup_list,diagnostic_tools,medicine,diagnosis):
  def addpatient(self, specie,breed,name,age,gender,date,address,phoneno,checkup_list, bill):
    try:
      cur = self.connection.cursor()
      query = "INSERT INTO patient (specie,breed,name,age,gender,date,address,phone_no,checkup_type, bill) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      args = (specie, breed, name, age, gender, date, address, phoneno, checkup_list, bill)
      cur.execute(query,args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't add patient!")
      return False
    finally:
      cur.close()



  def addDoctor(self, firstName,lastName,username,cnic,age,gender,date,address,phone,vtime,noOfdays,rank):
    try:
      cur = self.connection.cursor()
      query = "INSERT INTO doctortable (first_name,last_name,username,cnic,age,gender,joining_date,address,phone_no,visitingTime,noOfdays,rank) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      args = (firstName,lastName,username,cnic,age,gender,date,address,phone,vtime,noOfdays,rank)
      cur.execute(query,args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't add Doctor!")
      return False
    finally:
      cur.close()



  def addReceptionist(self, firstName,lastName,username,email,password,cnic,age,gender,date,address,phone):
    try:
      cur = self.connection.cursor()
      query = "INSERT INTO receptionist (first_name,last_name,username,email,password,cnic,age,gender,joining_date,address,phone_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      args = (firstName,lastName,username,email,password,cnic,age,gender,date,address,phone)
      cur.execute(query,args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't add Receptionist!")
      return False
    finally:
      cur.close()

  def addEmployee(self, firstName, lastName, cnic, age, gender, date, address, phone,job):
    try:
      cur = self.connection.cursor()
      query = "INSERT INTO employee (first_name,last_name,cnic,age,gender,joiningDate,address,phoneNo,staff_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      args = (firstName, lastName, cnic, age, gender, date, address, phone,job)
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't add Receptionist!")
      return False
    finally:
      cur.close()


  def addItem(self, name,price):
    try:
      cur = self.connection.cursor()
      query = "INSERT INTO ratelist (name,price) VALUES (%s,%s)"
      args = (name,price)
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't add Item!")
      return False
    finally:
      cur.close()


  def show_patients(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT specie, breed, name, age, gender, checkup_type, phone_no, date, bill FROM patient"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show patients!")
      return False
    finally:
      cur.close()

  def show_doctors(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT doc_id,first_name,last_name,gender,address,phone_no,age,cnic,joining_date,visitingTime,noOfDays,rank FROM doctortable"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show doctors!")
      return False
    finally:
      cur.close()


  def show_receptionists(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT recep_id,first_name,last_name,gender,address,phone_no,age,cnic,joining_date FROM receptionist"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show receptionists!")
      return False
    finally:
      cur.close()



  def show_employees(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT emp_id,first_name,last_name,gender,staff_type,address,phoneNo,age,cnic,joiningDate FROM employee"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show Employees!")
      return False
    finally:
      cur.close()


  def show_items(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT item_id,name,price FROM ratelist"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show items!")
      return False
    finally:
      cur.close()


  def show_members(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT m_id,m_username,m_email FROM member"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show receptionists!")
      return False
    finally:
      cur.close()


  def for_appt_patients(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT p_id,specie, checkup_type FROM patient"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show patients!")
      return False
    finally:
      cur.close()


  def for_appt_doctors(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT doc_id, first_name, last_name, rank FROM doctortable"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show doctors!")
      return False
    finally:
      cur.close()

  def make_appointment(self,p_id,doc_id,time,date):
    try:
      cur = self.connection.cursor()
      query = "INSERT INTO appointment (p_id,doc_id,time,date) VALUES (%s,%s,%s,%s)"
      args = (p_id,doc_id,time,date)
      cur.execute(query,args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't make appointments!")
      return False
    finally:
      cur.close()

  def show_appointments(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT * FROM appointment"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show appointments!")
      return False
    finally:
      cur.close()

  def del_appointments (self, del_apt_id):
    try:
      cur = self.connection.cursor()
      query = "DELETE FROM appointment WHERE apt_id = %s"
      args = del_apt_id
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't delete appointment!")
      return False
    finally:
      cur.close()



  def removeDoctor (self, del_apt_id):
    try:
      cur = self.connection.cursor()
      query = "DELETE FROM doctortable WHERE doc_id = %s"
      args = del_apt_id
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't Remove Doctor!")
      return False
    finally:
      cur.close()



  def getDoctor (self, del_apt_id):
    try:
      cur = self.connection.cursor()
      query = "Select * FROM doctortable WHERE doc_id = %s"
      args = del_apt_id
      cur.execute(query, args)
      data = cur.fetchone()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't Remove Doctor!")
      return False
    finally:
      cur.close()


  def getItem (self, item_id):
      try:
        cur = self.connection.cursor()
        query = "Select * FROM ratelist WHERE item_id = %s"
        args = item_id
        cur.execute(query, args)
        data = cur.fetchone()
        return data
      except Exception as e:
        print(e)
        print("Failure: Couldn't Find Doctor!")
        return False
      finally:
        cur.close()

  def updateDoctorData(self,fn,ln,g,ph,age,cnic,un,vt,nod,rank):
    try:
      
      # query = "SELECT first_name, last_name, gender, address, phone_no, age, cnic, username, visitingTime, noOfDays, rank from doctortable WHERE doc_id = %s"
      

      # cur.execute(query, args)
      # data = cur.fetchone()
      # print(data)
      cur = self.connection.cursor()
      doc_id = session.get("doctor_id")
      print("DOCTOR id from session DB:", doc_id)
      query2 =" UPDATE doctortable SET first_name = %s ,last_name = %s, gender = %s" \
             ",phone_no =%s,age=%s,cnic =%s,username=%s, visitingTime = %s, noOfDays = %s, rank = %s WHERE doc_id = %s"

      args2 = (fn,ln,g,ph,age,cnic,un,vt,nod,rank, doc_id)
      cur.execute(query2,args2)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't Remove Doctor!")
      return False
    finally:
      cur.close()


  def updateItemData(self,name,price):
    try:
        cur = self.connection.cursor()
        item_id = session.get("item_id")

        query = "update ratelist set name=%s,price = %s where item_id = %s"
        args = (name,price,item_id)

        cur.execute(query,args)
        self.connection.commit()
        return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't update Item!")
      return False
    finally:
      cur.close()


  def removeEmployee (self, del_apt_id):
    try:
      cur = self.connection.cursor()
      query = "DELETE FROM employee WHERE emp_id = %s"
      args = del_apt_id
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't Remove Employee!")
      return False
    finally:
      cur.close()



  def removeItem (self, del_apt_id):
    try:
      cur = self.connection.cursor()
      query = "DELETE FROM ratelist WHERE item_id = %s"
      args = del_apt_id
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't Remove Item!")
      return False
    finally:
      cur.close()


  def removeMember (self, del_apt_id):
    try:
      cur = self.connection.cursor()
      query = "DELETE FROM member WHERE m_id = %s"
      args = del_apt_id
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't Remove Member!")
      return False
    finally:
      cur.close()


  def removeReceptionist (self, del_apt_id):
    try:
      cur = self.connection.cursor()
      query = "DELETE FROM receptionist WHERE recep_id = %s"
      args = del_apt_id
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't Remove Receptionist!")
      return False
    finally:
      cur.close()


  def update_apts(self,p_id,doc_id,time,date,apt_id):
    try:
      cur = self.connection.cursor()
      query = "UPDATE appointment SET p_id = %s, doc_id = %s, time = %s, date = %s WHERE apt_id = %s"
      args = (p_id,doc_id,time,date,apt_id)
      cur.execute(query, args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't update appointment!")
      return False
    finally:
      cur.close()

  def check_items(self,name):
    try:
      cur = self.connection.cursor()
      query = "SELECT price FROM ratelist where name = %s"
      args = (name)
      cur.execute(query, args)
      data = cur.fetchone()
      return data
    except Exception as e:
      print(e)
      print("Failure!")
      return False
    finally:
      cur.close()

  def show_pat_for_update(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT p_id,specie,name,checkup_type FROM patient"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure!")
      return False
    finally:
      cur.close()

  def fetch_bill(self,pat_id):
    try:
      cur = self.connection.cursor()
      query = "SELECT bill from patient WHERE p_id = %s"
      args = pat_id
      cur.execute(query, args)
      data = cur.fetchone()
      return data
    except Exception as e:
      print(e)
      print("Failure!")
      return False
    finally:
      cur.close()

  def update_add_patient(self,dia_string,medicine,diagnosis,bill, pat_id):
    try:
      cur = self.connection.cursor()
      query = "UPDATE patient SET diagnostic_tools = %s, medicine = %s, diagnosis = %s, bill = %s WHERE p_id = %s"
      args = (dia_string, medicine, diagnosis, bill, pat_id)
      cur.execute(query,args)
      self.connection.commit()
      return True
    except Exception as e:
      print(e)
      print("Failure: Couldn't add patient!")
      return False
    finally:
      cur.close()

  def showBills(self):
    try:
      cur = self.connection.cursor()
      query = "Select p_id,bill from patient"
      cur.execute(query)
      data = cur.fetchall()
      cur.connection.commit()
      print(data)
      return data
    except Exception as e:
      print("Failure: couldn't show bills")
      return False
    finally:
      cur.close()

  def search_patient_dynamic(self,q):
    try:
      cur = self.connection.cursor()
      query = "SELECT specie, breed, name, age, gender, checkup_type, phone_no FROM patient WHERE name LIKE %s" 
      args = "%" + q + "%"
      cur.execute(query,args)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't Search Patient!")
      return False
    finally:
      cur.close()

  def recepit_show_patients(self):
    try:
      cur = self.connection.cursor()
      query = "SELECT p_id, specie, name, phone_no, checkup_type, medicine, diagnosis, bill FROM patient"
      cur.execute(query)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show patients!")
      return False
    finally:
      cur.close()

  def get_receipt(self, pat_id):
    try:
      cur = self.connection.cursor()
      query = "SELECT p_id, specie, name, checkup_type, medicine, diagnosis, bill FROM patient WHERE p_id = %s"
      args = (pat_id)
      cur.execute(query, args)
      data = cur.fetchall()
      return data
    except Exception as e:
      print(e)
      print("Failure: Couldn't show patients!")
      return False
    finally:
      cur.close()

































  # def sign_up(self,email,password,username,accounttype):
  #   try:
  #     cur = self.connection.cursor()
  #     if accounttype == 'Student':
  #       query = "INSERT INTO student (s_email,s_password,s_username,ad_ID) VALUES (%s,%s,%s,1)"
  #     elif accounttype == 'Teacher':
  #       query = "INSERT INTO teacher (t_email,t_password,t_username,ad_ID) VALUES (%s,%s,%s,1)"
  #     args = (email,password,username)
  #     cur.execute(query,args)
  #     self.connection.commit()
  #   except Exception as e:
  #     print (e)
  #   finally:
  #     cur.close()

  # def login(self,email,password):
  #   try:
  #     cur = self.connection.cursor()
  #     query = "Select type, s_username,s_ID from student where s_email = %s AND s_password = %s"
  #     args = (email,password)
  #     cur.execute(query, args)
  #     data = cur.fetchall()
  #     if len(data) != 0:
  #       print(data)
  #       return data

  #     query = "Select type, t_username, t_ID from teacher where t_email = %s AND t_password = %s"
  #     args = (email,password)
  #     cur.execute(query, args)
  #     data = cur.fetchall()
  #     if len(data) != 0:
  #       return data

  #     query = "Select type, ad_username from admin where ad_email = %s AND ad_password = %s"
  #     args = (email,password)
  #     cur.execute(query, args)
  #     data = cur.fetchall()
  #     if len(data) != 0:
  #       return data
  #     return False
  #   except Exception as e:
  #     print (e)
  #     return False
  #   finally:
  #     cur.close()

  # def show(self,accdata):
  #   try:
  #     cur = self.connection.cursor()
  #     if accdata == 'Teacher':
  #       query = "SELECT t_email,t_password,t_username from teacher"
  #     elif accdata == 'Student':
  #       query = "SELECT s_email,s_password,s_username from student"
  #     cur.execute(query)
  #     data = cur.fetchall()
  #     return data
  #   except Exception as e:
  #     print (e)
  #   finally:
  #     cur.close()
      
  # def create_class_id(self):
  #   try:
  #     cur = self.connection.cursor()

  #     random.seed(datetime.now().timestamp())
  #     string.ascii_letters = ['b', 'd', 'f', 'h', 'j', 'l', 'n', 'p', 'r', 't', 'v', 'x', 'z']
  #     i = 0
  #     random_letters = ""
  #     while i < 5:
  #         letter = random.choices(string.ascii_letters, k=1)
  #         random_letters = random_letters + str(letter[0])
  #         i += 1

  #     query = "select * from classroom where class_ID = %s"
  #     args=random_letters
  #     cur.execute(query,args)
  #     data = cur.fetchall()
  #     if data == ():
  #         return random_letters
  #     else:
  #         self.create_class_id()

  #   except Exception as e:
  #     print(e)
  #   finally:
  #     cur.close()
    

  # def create_classroom(self,cl_name,t_ID,created_by):
  #   try:
  #     cur = self.connection.cursor()
  #     classid = self.create_class_id()
  #     query1 = "INSERT INTO classroom (class_ID,t_ID,class_name,class_cDate,ad_ID,created_by) VALUES (%s,%s,%s,SYSDATE(),%s,%s)"
  #     # cl_name = input("Enter class name: ")
  #     args = (classid,t_ID,cl_name,1,created_by)
  #     cur.execute(query1,args)
  #     self.connection.commit()
  #     # print("Classroom has been created")
  #     return True
  #   except Exception as e:
  #     print (e)
  #     return False
  #   finally:
  #     cur.close()

  # def add_student(self,class_ID,s_ID):
  #   try:
  #     cur = self.connection.cursor()
  #     query = "INSERT INTO enroll (class_ID,s_ID) VALUES (%s,%s)"
  #     args = (class_ID,s_ID)
  #     cur.execute(query,args)
  #     self.connection.commit()
  #     # print("Student has been added")
  #     return True
  #   except Exception as e:
  #     print(e)
  #     return False
  #   finally:
  #     cur.close()

  # def show_classes(self,created_by):
  #   try:
  #     cur = self.connection.cursor()
  #     query = "SELECT * from classroom WHERE created_by = %s"
  #     args = created_by
  #     cur.execute(query,args)
  #     data = cur.fetchall()
  #     if len(data) != None:
  #       return data
  #     else:
  #       return False
  #   except Exception as e:
  #     print (e)
  #     return False
  #   finally:
  #     cur.close()    

  # def join_class(self,classid,s_ID,sess_email):
  #   try:
  #     cur = self.connection.cursor()
  #     query3 = "INSERT INTO enroll (class_ID,s_ID,joined_by) VALUES (%s,%s,%s)"
  #     args3 = (classid, s_ID,sess_email)
  #     cur.execute(query3, args3)
  #     self.connection.commit()
  #     return True
  #   except Exception as e:
  #     print (e)
  #     return False
  #   finally:
  #     cur.close()  

  # def show_classes_std(self,joined_by):
  #   try:
  #     cur = self.connection.cursor()
  #     query = "SELECT * from enroll WHERE joined_by = %s"
  #     args = joined_by
  #     cur.execute(query,args)
  #     data = cur.fetchall()
  #     if len(data) != None:
  #       return data
  #     else:
  #       return False
  #   except Exception as e:
  #     print (e)
  #     return False
  #   finally:
  #     cur.close()



