from flask import Flask, make_response, render_template, request, session, redirect, url_for, jsonify
from DBHandler import DBHandler
import json
import bcrypt

app = Flask(__name__)

app.config.from_object("config")
app.secret_key = app.config["SECRET_KEY"]

@app.route("/")
def main_page():
  return render_template("main_page.html", msg=None)

# -------------- SIGN-UP,LOG-IN Page ------------------
@app.route("/ls")
def signup_login_page():
  return render_template("signup_login.html", msg=None)

@app.route("/contact_us")
def contact_page():
  return render_template("contact_us.html")

# -------------------- SIGN-UP ------------------------

@app.route("/signup", methods=["POST"])
def signup():
  try:
    # retriving data from the form using POST
    member_username = request.form["username"]
    member_email = request.form["email"]
    member_password = request.form["password"]
    
    print("Password without hashing is:", member_password)

    # we are hashing and salting the password with bcrypt

    hashed_password = bcrypt.hashpw(member_password.encode("utf-8"), bcrypt.gensalt())


    print("Password with hashing is:", hashed_password)

    # make handler
    handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])

    member_added = handler.sign_up(member_username,member_email,hashed_password)

    if member_added == True:
      return render_template("signup_login.html",msg = "You have been signed up")
    else:
      return render_template("failure.html")
  except Exception as e:
    print (e)
    return render_template("failure.html")


# ---------- DASHBOARD (FOR REECEPTIONIST) ------------
@app.route("/recepdashboard")
def recep_dashboard_2():
  recep_id = session.get("RECEP_ID")
  if recep_id != None:
    return render_template("recep_dashboard_2.html",recep_id = recep_id)
  else:
    return "YOU MUST BE LOGGED IN FIRST!"



@app.route("/adminBoard")
def admin_dashboard():
  admin_id = session.get("AD_ID")
  if admin_id != None:
    return render_template("admin_dashboard_2.html",msg = None)
  else:
    return "YOU MUST BE LOGGED IN FIRST!"


# @app.route("/adminBoard")
# def admin_dashboard():
#   admin_id = session.get("AD_ID")
#   if admin_id != None:
#     return render_template("admin_dashboard.html",msg = None)
#   else:
#     return "YOU MUST BE LOGGED IN FIRST!"

# -------------------- LOG-IN -------------------------
@app.route("/login", methods=["POST"])
def login():
  # retriving data from the form using POST
  email = request.form["email"]
  password = request.form["password"]

  # make handler
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])

  login_data = handler.login(email,password)
  if login_data != False and login_data[0][0] == 'admin':
    try:
      ad_id = login_data[0][2]
      session["EMAIL"] = email
      session["PASSWORD"] = password
      session["AD_ID"] = str(ad_id) 
      # AD_ID must be parsed into int before using else where
      return redirect(url_for('admin_dashboard'))
    except Exception as e:
      print(e)
      return render_template("failure.html")

  elif login_data != False and login_data[0][0] == 'recep':
    try:
      recep_id = login_data[0][2]
      session["EMAIL"] = email
      session["PASSWORD"] = password
      session["RECEP_ID"] = str(recep_id)
      # RECEP_ID must be parsed into int before using else where
      # return render_template("recep_dashboard.html",msg = None)
      return redirect(url_for('recep_dashboard_2'))
    except Exception as e:
      print (e)
      return render_template("failure.html")
  elif login_data != False and login_data[0][0] == 'member':
    try:
      m_id = login_data[0][2]
      session["EMAIL"] = email
      session["PASSWORD"] = password
      session["M_ID"] = str(m_id)
      # M_ID must be parsed into int before using else where
      em = session.get("EMAIL")
      return render_template("member_dashboard.html",msg = None)
    except Exception as e:
      print (e)
  return render_template("failure.html")

# -------------------- LOG-OUT ------------------------
@app.route("/logout")
def logout():
  session.clear()
  return render_template("signup_login.html",msg = "You have been logged out of session!")


# ---------- ADD - PATIENT (FOR REECEPTIONIST) ------------
# design a form that will take all the attributes and then write a function to insert data into the 
# database, take form input and insert (add)

@app.route("/addpatient")
def addpatient_form():
  return render_template("addpatient.html", msg=None)

@app.route("/addpatient", methods=["POST"])
def addpatient():

  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])

  specie = request.form["specie"]
  breed = request.form["breed"]
  name = request.form["name"]
  age = request.form["age"]
  age = int(age)
  gender = request.form["gender"]
  date = request.form["date"]

  address = request.form["address"]
  phoneno = request.form["phoneno"]

  checkup_list = request.form.getlist('checkup_type')


  # diagnostic_tools = request.form.getlist('diagnostic_tools')

  # medicine = request.form["medicine"]
  # diagnosis = request.form["diagnosis"]

  bill = 0
  for i in checkup_list:
    amount = handler.check_items(i)
    bill = bill + amount[0] 
  print("Bill is: ", bill)

  # print(specie,breed,name,age,gender,date,address,phoneno,checkup_list,diagnostic_tools,medicine,diagnosis)
  print(specie,breed,name,age,gender,date,address,phoneno,checkup_list,bill)

  checkup_string = ''

  for i in checkup_list:
    if(i!=checkup_list[-1]):
      checkup_string = checkup_string + i + ','
    else:
      checkup_string = checkup_string + i
  print(checkup_string)
  # dia_string = ''
  # for i in diagnostic_tools:
  #   dia_string = dia_string + i + ','
  # print(dia_string)

 
  
  # add_success = handler.addpatient(specie,breed,name,age,gender,date,address,phoneno,checkup_string,dia_string,medicine,diagnosis)

  add_success = handler.addpatient(specie,breed,name,age,gender,date,address,phoneno,checkup_string,bill)

  if add_success == True:
    return render_template("success.html")
  else:
    return "Add Failure!"

@app.route("/add_doctor")
def addDoctor_form():
    message = request.args.get("message");
    print("\n\n",message,"\n\n")
    return render_template("addDoctor.html", msg=message)

@app.route("/add_doctor", methods=["POST"])
def addDoctor():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  firstName = request.form["fName"]
  lastName = request.form["lName"]
  userName = request.form["uName"]
  cnic = request.form["cnic"]
  age = request.form["age"]
  age = int(age)
  gender = request.form["gender"]
  date = request.form["date"]
  address = request.form["address"]
  phoneno = request.form["phoneno"]
  vtime = request.form["visitingTime"]
  noOfDays = request.form["noOfDays"]
  noOfDays = int(noOfDays)
  rank = request.form["rank"]
  add_success = handler.addDoctor(firstName, lastName, userName, cnic, age, gender, date, address, phoneno, vtime,noOfDays,rank)

  if add_success == True:
    return redirect(url_for('showdoctor'))

    # return redirect(url_for('addDoctor_form', message=message))
  else:
    return "Add Failure!"


@app.route("/getdoctor/<doctor_id>")
def getDoctor(doctor_id):

  session["doctor_id"] = doctor_id

  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.getDoctor((doctor_id))
  if(data):
    return render_template("UpdateDoctor.html", data=data)
  else:
    return render_template("UpdateDoctor.html", data=None)


#/updateitemdata
@app.route("/updateitemdata",methods=["POST"])
def update_item_data():
  name = request.form["name"]
  price = request.form["price"]
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  flag = handler.updateItemData(name,price)
  if flag:
      return redirect(url_for('show_Items'))
  else:
     return render_template("failure.html")


@app.route("/updatedoctordata",methods=["POST"])
def updatedoctordata():
    f_name = request.form["first_name"]
    l_name = request.form["last_name"]
    gender = request.form["gender"]
    phone_no = request.form["phone_no"]
    age = request.form["age"]
    cnic = request.form["cnic"]
    username = request.form["username"]
    visitingTime = request.form["visitingTime"]
    noOfDays = request.form["noOfDays"]
    rank = request.form["rank"]
    
    handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])

    flag = handler.updateDoctorData(f_name,l_name,gender,phone_no,age,cnic,username,visitingTime,noOfDays,rank)

    if flag:
      return redirect(url_for('showdoctor'))
    else:
      return render_template("failure.html")



@app.route("/getemployee/<employee_id>")
def getEmployee(employee_id):
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.getDoctor((employee_id))
  if(data):
    return render_template("UpdateEmployee.html", data=data)
  else:
    return render_template("UpdateEmployee.html", data=None)


@app.route("/updateshowdoctor")
def updateShowDoctor():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_doctors()
  return render_template("updateshowdoctor.html", data=data)


@app.route("/add_receptionist")
def addReceptionist_form():
  return render_template("addReceptionist.html", msg=None)

@app.route("/add_receptionist", methods=["POST"])
def addReceptionist():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  firstName = request.form["fName"]
  lastName = request.form["lName"]
  userName = request.form["uName"]
  email = request.form["email"]
  password = request.form["password"]
  cnic = request.form["cnic"]
  age = request.form["age"]
  age = int(age)
  gender = request.form["gender"]
  date = request.form["date"]
  address = request.form["address"]
  phoneno = request.form["phoneno"]

  add_success = handler.addReceptionist(firstName, lastName, userName, email, password, cnic, age, gender, date, address, phoneno)

  if add_success == True:
    return redirect(url_for('show_Receptionists'))
  else:
    return "Add Failure!"




@app.route("/add_employee")
def addEmployee_form():
  return render_template("addEmployee.html", msg=None)

@app.route("/add_employee", methods=["POST"])
def addEmployee():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  firstName = request.form["fName"]
  lastName = request.form["lName"]
  cnic = request.form["cnic"]
  age = request.form["age"]
  age = int(age)
  gender = request.form["gender"]
  date = request.form["date"]
  address = request.form["address"]
  phoneno = request.form["phoneno"]
  job = request.form["job"]

  add_success = handler.addEmployee(firstName, lastName, cnic, age, gender, date, address, phoneno,job)

  if add_success == True:
    return redirect(url_for('show_Employees'))
  else:
    return "Add Failure!"



@app.route("/add_new_item")
def addItem_form():
  return render_template("addItem.html", msg=None)

@app.route("/add_new_item", methods=["POST"])
def addItem():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  name = request.form["name"]
  price = request.form["price"]
  price = int(price)

  add_success = handler.addItem(name,price)

  if add_success == True:
    return redirect(url_for('show_Items'))
  else:
    return "Add Failure!"




# ---------- Update - PATIENT (FOR REECEPTIONIST) ------------
@app.route("/show_update_patient")
def update_patient_form():
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"]) 
  data = handler.show_pat_for_update()
  if len(data) != 0:
    return render_template("update_patient_form.html",data=data) 
  else:
    return render_template("failure")

@app.route("/update_patients", methods = ["POST"])
def update_patient():
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"]) 
  pat_id = request.form["id"]
  diagnostic_tools = request.form.getlist('diagnostic_tools')
  medicine = request.form["medicine"]
  diagnosis = request.form["diagnosis"]
  curr_amount = handler.fetch_bill(pat_id)
  print("amount from DB:", curr_amount)
  curr_amount = curr_amount[0]
  for i in diagnostic_tools:
    amount = handler.check_items(i)
    curr_amount = curr_amount + amount[0]
  print(curr_amount)

  dia_string = ''
  for i in diagnostic_tools:
    dia_string = dia_string + i + ','
  print(dia_string)

 
  add_success = handler.update_add_patient(dia_string,medicine,diagnosis,curr_amount,int(pat_id))
  if add_success == True:
    return render_template("success.html")
  else:
    return "Add Failure!"
  



# ---------- SHOW - PATIENT (FOR REECEPTIONIST) ------------
@app.route("/showpatient")
def showpatient():
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data = handler.show_patients()
  if len(data) != 0:
    return render_template("showpatient.html",data=data)


# ---------- SHOW - DCOTOR (FOR REECEPTIONIST) ------------
@app.route("/recep_show_doctor")
def recep_show_doctor():
  print("** IN FUNCC **")
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data = handler.show_doctors()
  print("** DATA: **", data)
  if len(data) != 0:
    return render_template("recep_show_doctors.html",data=data)


@app.route("/showdoctor")
def showdoctor():
  print("\n\n\nin show")
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data = handler.show_doctors()
  if len(data) != 0:
    return render_template("showdoctor.html",data=data)

@app.route("/api/delshowdoctor",  methods = ["DELETE"] )
def delShowDoctor():
  body = request.get_json()
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  doctorId = body["id"]
  if(handler.removeDoctor(doctorId)):
    return {"status":"True"},200
  else:
    return {"status":"False"},404

@app.route("/deleteshowdoctor")
def deleteshowdoctor():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_doctors()
  if len(data) != 0:
    return render_template("deleteshowdoctor.html", data=data)


  # ---------- SHOW - REECEPTIONIST ------------

@app.route("/show_receptionists")
def show_Receptionists():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_receptionists()
  if len(data) != 0:
    return render_template("showReceptionist.html", data=data)

@app.route("/deleteshowrecep")
def delshowRecep():
    handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
    data = handler.show_receptionists()
    if len(data) != 0:
      return render_template("delshowReceptionist.html", data=data)

@app.route("/api/delshowrecep", methods=["DELETE"])
def delShowRecep():
  body = request.get_json()
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  recepId = body["id"]
  if (handler.removeReceptionist(recepId)):
    return {"status": "True"}, 200
  else:
    return {"status": "False"}, 404

    # ---------- SHOW - Employee ------------

@app.route("/show_employees")
def show_Employees():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_employees()
  if len(data) != 0:
    return render_template("showEmployees.html", data=data)


@app.route("/deleteshowemployee")
def del_show_Employees():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_employees()
  if len(data) != 0:
    return render_template("delshowEmployees.html", data=data)


@app.route("/api/delshowemployee", methods=["DELETE"])
def delShowemployeee():
  body = request.get_json()
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  employeeId = body["id"]
  if (handler.removeEmployee(employeeId)):
    return {"status": "True"}, 200
  else:
    return {"status": "False"}, 404


@app.route("/update_item")
def update_items():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_items()
  return render_template("updateshowItem.html", data=data)


@app.route("/getItem/<item_id>")
def get_item(item_id):

  session["item_id"] = item_id

  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.getItem(item_id)
  if(data):
    return render_template("updateItem.html", data=data)
  else:
    return render_template("updateItem.html", data=None)

@app.route("/show_items")
def show_Items():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_items()
  if len(data) != 0:
    return render_template("showItems.html", data=data)

@app.route("/delShowItems")
def del_show_Items():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_items()
  if len(data) != 0:
    return render_template("delShowItems.html", data=data)


@app.route("/api/delshowitem", methods=["DELETE"])
def delShowitemss():
  body = request.get_json()
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  employeeId = body["id"]
  if (handler.removeItem(employeeId)):
    return {"status": "True"}, 200
  else:
    return {"status": "False"}, 404




@app.route("/show_members")
def show_Members():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_members()
  if len(data) != 0:
    return render_template("showMembers.html", data=data)

# ---------- MAKE APPOINTMENTs - (FOR REECEPTIONIST) ------------

@app.route("/appointment")
def appointment_page():
  return render_template("for_app_patients.html")

@app.route("/api/appointment")
def appointment():
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data1 = handler.for_appt_patients()
  if len(data1) != 0:
    # print(data1)

    d_list = []

    for i in data1:
      dictt = {}
      dictt["id"] = i[0]
      dictt["name"] = i[1]
      dictt["checkup_type"] = i[2]
      d_list.append(dictt)
      # print(dictt)
    print(d_list)

    json_data = jsonify(d_list)

    # return json_data
    return json_data, 200

    # return Response(json_data, mimetype="application/json", status=200)

    # return render_template("for_app_patients.html", data=data1)

@app.route("/for_app_patients", methods=["POST"])
def make_appointment_form():

  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])

  pat_id = request.form["id"]
  app_time = request.form["time"]
  app_date = request.form["date"]

  session["PAT_ID"] = pat_id
  session["APP_TIME"] = app_time
  session["APP_DATE"] = app_date

  data1 = handler.for_appt_doctors()
  return render_template("for_app_doctors.html",data=data1)
  
@app.route("/for_app_doctor", methods=["POST"])
def make_appt():

  doc_id = request.form["id"]
  session["DOC_ID"] = doc_id

  p_id = session.get("PAT_ID")
  appt_time = session.get("APP_TIME")
  appt_date = session.get("APP_DATE")


  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  
  success = handler.make_appointment(int(p_id),int(doc_id),appt_time,appt_date)
  if success == True:
    return render_template("appt_success.html",p_id=int(p_id),doc_id=int(doc_id)  ,appt_time=appt_time,appt_date=appt_date)


# ---------- DELETE APPOINTMENTs - (FOR REECEPTIONIST) ------------
@app.route("/del_appointments")
def del_appointments():
  # display appointments table first
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data = handler.show_appointments()
  if len(data) != 0:
    return render_template("showappointments.html", data = data)
  else:
    return render_template("failure.html")

@app.route("/api/input_del_appointments", methods = ["DELETE"])
def input_del_appointments():

  print("\n\n +++ IN ROUTE +++ ")

  if request.method == "DELETE":

    print("\n\n *** IN API DELETE *** ")

    handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])

    # del_apt_id = request.form["id"]
    # session["DEL_APT_ID"] = del_apt_id

    del_apt_id = request.get_json()
    print("\n\n\nDeletion id: ",del_apt_id)

    del_id = int(del_apt_id['id'])
    
    print("\nDel id:", del_id)

    success = handler.del_appointments(del_id)
    s_dict = {"success_status":success}
    
    j_data = jsonify(s_dict)

    return j_data, 200

  # if success == True:



  #   return render_template("apt_success.html", del_apt_id=del_apt_id, val = "deleted!")
  # else:
  #   return render_template("failure.html")


# ---------- REMOVVE DOCTOR  ------------
@app.route("/remove_doctor")
def remove_doctor():
  # display appointments table first
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_doctors()
  if len(data) != 0:
    return render_template("removeDoctor.html", data=data)
  else:
    return render_template("failure.html")


@app.route("/input_remove_doctor", methods=["POST"])
def input_remove_doctor():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])

  del_apt_id = request.form["id"]
  session["DEL_APT_ID"] = del_apt_id

  success = handler.removeDoctor(int(del_apt_id))

  if success == True:
    return render_template("doc_success.html", del_apt_id=del_apt_id, val="deleted!")
  else:
    return render_template("failure.html")



@app.route("/remove_employee")
def remove_employee():
  # display appointments table first
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_employees()
  if len(data) != 0:
    return render_template("removeEmployee.html", data=data)
  else:
    return render_template("failure.html")


@app.route("/input_remove_employee", methods=["POST"])
def input_remove_employee():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])

  del_apt_id = request.form["id"]
  session["DEL_APT_ID"] = del_apt_id

  success = handler.removeEmployee(int(del_apt_id))

  if success == True:
    return render_template("doc_success.html", del_apt_id=del_apt_id, val="deleted!")
  else:
    return render_template("failure.html")


@app.route("/remove_item")
def remove_item():
  # display appointments table first
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_items()
  if len(data) != 0:
    return render_template("removeItem.html", data=data)
  else:
    return render_template("failure.html")


@app.route("/input_remove_item", methods=["POST"])
def input_remove_item():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])

  del_apt_id = request.form["id"]
  session["DEL_APT_ID"] = del_apt_id

  success = handler.removeItem(int(del_apt_id))

  if success == True:
    return render_template("doc_success.html", del_apt_id=del_apt_id, val="deleted!")
  else:
    return render_template("failure.html")



@app.route("/remove_member")
def remove_member():
  # display appointments table first
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_members()
  if len(data) != 0:
    return render_template("removeMember.html", data=data)
  else:
    return render_template("failure.html")


@app.route("/input_remove_member", methods=["POST"])
def input_remove_member():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])

  del_apt_id = request.form["id"]
  session["DEL_APT_ID"] = del_apt_id

  success = handler.removeMember(int(del_apt_id))

  if success == True:
    return render_template("doc_success.html", del_apt_id=del_apt_id, val="deleted!")
  else:
    return render_template("failure.html")



@app.route("/remove_receptionist")
def remove_receptionist():
  # display appointments table first
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])
  data = handler.show_receptionists()
  if len(data) != 0:
    return render_template("removeReceptionist.html", data=data)
  else:
    return render_template("failure.html")


@app.route("/input_remove_receptionist", methods=["POST"])
def input_remove_receptionist():
  handler = DBHandler(app.config["DB_IP"], app.config["DB_USER"], app.config["DB_PASSWORD"], app.config["DB_NAME"])

  del_apt_id = request.form["id"]
  session["DEL_APT_ID"] = del_apt_id

  success = handler.removeReceptionist(int(del_apt_id))

  if success == True:
    return render_template("doc_success.html", del_apt_id=del_apt_id, val="deleted!")
  else:
    return render_template("failure.html")





@app.route("/display_appointments")
def show_appointments():
  
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data = handler.show_appointments()
  if len(data) != 0:
    return render_template("display_appointments.html",data=data)
  else:
    return render_template("failure.html")
  
@app.route("/update_appointments")
def update_appointments():

  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data = handler.show_appointments()
  if len(data) != 0:
    return render_template("for_update_show_appts.html",data=data)
  else:
    return render_template("failure.html")

@app.route("/update_apts", methods = ["POST"])
def update_apts():

  apt_id = request.form["apt_id"]
  p_id = request.form["p_id"]
  doc_id = request.form["doc_id"]
  apt_time = request.form["time"]
  apt_date = request.form["date"]

  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"]) 

  success = handler.update_apts(p_id,doc_id,apt_time,apt_date,apt_id) 
  if success == True:
    return render_template("apt_success.html",del_apt_id = apt_id, val = "updated!")
  else:
    return render_template("failure.html")

@app.route("/search_patient")
def searchform():
  return render_template("search_pat_form.html",msg=None)


@app.route("/search", methods = ["GET"])
def search():
  q = request.args.get("q")
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"]) 
  # data = handler.search_patient(q)
  data = handler.search_patient_dynamic(q)
  print(data)
  # return render_template("dynamic_search_text.html",data = data)
  return render_template("search.html",data=data)

@app.route("/show_bill")
def showBill():
  handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  data = handler.showBills()
  return render_template("showbill.html",data=data)


# RECEIPT

@app.route("/recepit")
def receipt():
  try:
    handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
    data = handler.recepit_show_patients()
    print(data)
    if len(data) != 0:
      return render_template("recepit_show_patients.html", data=data)
  except Exception as e:
    print(e)
    return render_template("failure.html")

@app.route("/receipt_show_patients", methods=["POST"])
def get_receipt():

  try:
    pat_id = request.form["id"]
    handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
    data = handler.get_receipt(int(pat_id))
    if len(data) != 0:
        return render_template("bill.html", data=data)
  except Exception as e:
    print(e)
    return render_template("failure.html")

if __name__ == "__main__":
  app.run(debug=True)



# specie,breed,name,age,gender,date,address,phoneno 







































# @app.route("/login")
# def login_form():
#   return render_template("login.html")

# @app.route("/logout")
# def logout():
#   session.clear()
#   return "You have been logged out of the session!"

# @app.route("/user")
# def user():
#   email = session.get("EMAIL")
#   password = session.get("PASSWORD")
#   if email != None and password != None:
#     return render_template("user.html",email=email,password=password)
#   else:
#     return "ERROR: You must be logged in first!"

# @app.route("/login",methods=["POST"])
# def login():
#   email = request.form["email"]
#   password = request.form["password"]

#   handler = DBHandler(app.config["DB_IP"],app.config["DB_USER"],app.config["DB_PASSWORD"],app.config["DB_NAME"])
  
#   success = handler.login(email,password)
#   if success == True:
#     session["EMAIL"] = email
#     session["PASSWORD"] = password
#     return render_template("logged.html",email=email,password=password)
#   else:
#     return "ERROR: Login Failed!"