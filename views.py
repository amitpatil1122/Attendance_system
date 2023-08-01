from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.contrib import messages
import csv

# Create your views here.

def login(request):
    return render(request,"login.html")

def logout(request):
   try:
      del request.session['is_logged']
   except:
      pass
   return render(request,"login.html")



def admin_view(request):
    logged = 1
    if request.session.has_key('is_logged'):
        return render(request,"admin_view.html")
    else:
        return render(request,'login.html', {'logged': logged})

def teacher_view(request):

    if request.session.has_key('is_logged'):
        username = request.session['is_logged']

        cursor = connection.cursor()

        query = "SELECT name FROM user where username = '"+username+"'"
        cursor.execute(query)
        result = cursor.fetchone()[0]

        a = "SELECT name,class_div,id FROM user where class_teacher = '"+result+"' "
        cursor.execute(a)
        res = cursor.fetchall()


        teachers = []
        for teacher in res:
            attendance = {"name" : teacher[0],"class_div" : teacher[1],'id':teacher[2]}
            teachers.append(attendance)

    return render(request,"teacher_view.html",{'teachers' : teachers})


def student_view(request):

    if request.session.has_key('is_logged'):
        username = request.session['is_logged']


        cursor = connection.cursor()

        query = "SELECT name,address,mobile,email,gender,dob,class_div FROM user where username = '"+username+"'"
        cursor.execute(query)

        res = cursor.fetchall()

        students = []
        for student in res:
            detail = {"name" : student[0], "address" : student[1], "mobile" : student[2], "email" : student[3], "gender" : student[4], "dob" : student[5], "class_div" : student[6]}
            students.append(detail)



    return render(request,"student_view.html",{'students' : students})


def add_teacher(request):
    logged = 1
    if request.session.has_key('is_logged'):
        return render(request,"admin_view.html")
    else:
        return render(request,"login.html",{'logged' : logged})

def add_student(request):
    cursor = connection.cursor()

    query = "SELECT name,id FROM user WHERE type = 'teacher' "
    cursor.execute(query)
    res = cursor.fetchall()
    teacher_list = []
    for teacher in res:
        teacher_list.append(teacher[0])



    return render(request,"add_student.html",{'result' : teacher_list})

def view_teacher(request):

    cursor = connection.cursor()


    query = "SELECT name,address,mobile,email,gender,dob FROM user where type = 'teacher' "
    cursor.execute(query)
    res = cursor.fetchall()
    teacher_list = []
    for teacher in res:
        teacher_info = {"name" : teacher[0],"address" : teacher[1],"mobile" : teacher[2],"email" : teacher[3],"gender" : teacher[4],"dob" : teacher[5]}
        teacher_list.append(teacher_info)



    return render(request,"view_teacher.html",{'teacher_list' : teacher_list})

def view_student(request):

    cursor = connection.cursor()

    query = "SELECT name,address,mobile,email,gender,dob,class_div,class_teacher FROM user where type = 'student' "
    cursor.execute(query)
    res = cursor.fetchall()
    student_list= []
    for student in res:
        student_info = {"name" : student[0],"address" : student[1] , "mobile" : student[2], "email" : student[3], "gender" : student[4] , "dob" : student[5], "class_div" : student[6],"class_teacher" : student[7]}
        student_list.append(student_info)

    return render(request,"view_student.html",{'student_list' : student_list})



@csrf_exempt
def validate_login(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE username = '" + username + "'"
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        login_falied = 1
        if result is None:
            return render("login.html", {'login_falied': login_falied})
        else:
            if result[2]==username and result[3]==password:
                request.session['is_logged'] = username
                if result[4]=='admin':
                    return HttpResponseRedirect("/admin_view/")
                elif result[4]=='teacher':
                    return HttpResponseRedirect("/teacher_view/")
                elif result[4]=='student':
                    return HttpResponseRedirect("/student_view/")
                else:
                    return render(request,"login.html",{'login_falied': login_falied})
            else:
                return render(request,"login.html",{'login_falied': login_falied})

    else:
        return HttpResponseRedirect("/login/")

@csrf_exempt
def register_teacher(request):
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            name = request.POST.get('name')
            address = request.POST.get('address')
            username = request.POST.get('username')
            password = request.POST.get('password')
            subject = request.POST.get('subject')
            mobile = request.POST.get('mobile')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            email = request.POST.get('email')


            cursor = connection.cursor()

                                        # check for user already exist

            a = "SELECT COUNT(*) FROM user where username='"+username+"'"
            cursor.execute(a)

            res = cursor.fetchone()[0]
            if res == 0:
                                        # insert teacher data in database

                query = "insert into user (name,username,password,subject,mobile,dob,gender,email,type,address) values ('" + name + "' , '" + username + "' , '" + password + "' , '" + subject + "' , '" + mobile + "' , '" + dob + "' , '" + gender + "' , '" + email + "' , 'teacher', '" + email + "')"
                cursor.execute(query)

            else:
                user_already_exist = 1
                return render(request,'admin_view.html',{'user_already_exist' : user_already_exist})

    registered_successfully = 1
    return render(request,'admin_view.html',{'registered_successfully' : registered_successfully})



@csrf_exempt
def admin_add_student(request):
    if request.session.has_key('is_logged'):
        if request.method == 'POST':
            name = request.POST.get('name')
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            class_div = request.POST.get('class_div')
            class_teacher = request.POST.get('class_teacher')
            username = request.POST.get('username')
            password = request.POST.get('password')

            cursor = connection.cursor()



            query_sql = "SELECT name,id FROM user WHERE type = 'teacher' "
            cursor.execute(query_sql)
            res = cursor.fetchall()
            teacher_list = []
            for teacher in res:
                teacher_list.append(teacher[0])

            a = "SELECT COUNT(*) FROM user where username='" + username + "'"
            cursor.execute(a)

            res = cursor.fetchone()[0]
            if res == 0:

                sql = "insert into user (name,address,mobile,dob,gender,email,class_div,username,password,class_teacher,type) values ('"+name+"','"+address+"','"+mobile+"','"+dob+"','"+gender+"','"+email+"','"+class_div+"','"+username+"','"+password+"','"+class_teacher+"','student')"
                cursor.execute(sql)

            else:
                user_already_exist = 1
                return render(request,'add_student.html',{'user_already_exist' : user_already_exist,'result': teacher_list})

        registered_successfully = 1
        return render(request,"add_student.html",{'registered_successfully' : registered_successfully,'result': teacher_list})



def attendance(request):

    if request.method == 'POST':
        if request.session.has_key('is_logged'):
            username = request.session['is_logged']

            cursor = connection.cursor()

            query = "SELECT name FROM user where username = '" + username + "'"
            cursor.execute(query)
            result = cursor.fetchone()[0]

            a = "SELECT name,class_div,id FROM user where class_teacher = '" + result + "' "
            cursor.execute(a)
            res = cursor.fetchall()
            present_date = request.POST.get('present_date')

            teachers = []
            for teacher in res:
                attendance = {"name": teacher[0], "class_div": teacher[1], 'id': teacher[2]}
                teachers.append(attendance)
                attend_success = 1

                presenty = request.POST.get('present_'+str(teacher[2]))
                if presenty == 'on':
                    presenty = '1'
                else:
                    presenty = '0'
                print(presenty)
                print(str(teacher[2]))
                print(present_date)
                print(presenty)



                sql = "INSERT INTO present (user_id,date,is_present) VALUES ('"+str(teacher[2])+"','"+present_date+"',"+presenty+")"
                cursor.execute(sql)
    return render(request,"teacher_view.html",{'teachers' : teachers, 'attend_success' : attend_success})


def view_attendance(request):
    cursor = connection.cursor()

    query = "SELECT name,id FROM user WHERE type = 'teacher' "
    cursor.execute(query)
    res = cursor.fetchall()
    teacher_list = []
    for teacher in res:
        teacher_list.append(teacher[0])
    return render(request,"view_attendance.html", {'result': teacher_list})


def view_attend(request):

    username1 = request.POST.get('class_teacher')
    #print(username1)

    username = str(username1)
   # print(username)

    cursor = connection.cursor()

    query = "SELECT name,id FROM user WHERE type = 'teacher' "
    cursor.execute(query)
    res = cursor.fetchall()
    teacher_list = []
    for teacher in res:
        teacher_list.append(teacher[0])


    a = "select p.user_id,u.name,SUM(p.is_present) from user as u,present as p where class_teacher = '"+username+"' and u.id=p.user_id GROUP BY p.user_id"
    cursor.execute(a)
    res = cursor.fetchall()
    print(res)
    attendance_list = []
    for student in res:
        attendance_info = {"id": student[0], "name": student[1], "is_present": student[2]}
        attendance_list.append(attendance_info)

    return render(request,"view_attendance.html", {'attendance_list': attendance_list,'result': teacher_list,'class_teacher':username1})

def export_attendance(request):
    username1 = request.POST.get('class_teacher')
    attendance_list = request.POST.get('attendance_list')
    #print(username1)

    username = str(username1)
  #  print(username)

    cursor = connection.cursor()

    query = "SELECT name,id FROM user WHERE type = 'teacher' "
    cursor.execute(query)
    res = cursor.fetchall()
    teacher_list = []
    for teacher in res:
        teacher_list.append(teacher[0])

    a = "select p.user_id,u.name,SUM(p.is_present) from user as u,present as p where class_teacher = '" + username + "' and u.id=p.user_id GROUP BY p.user_id"
    cursor.execute(a)
    res = cursor.fetchall()
    print(res)
    attendance_list = []
    f = open("./myapp/static/Attendance_Report.csv", "w")
    f.write("ID,Student_Name,Attendance\n")

    for student in res:
        attendance_info = {"id": student[0], "name": student[1], "is_present": student[2]}

        #attendance_list.append(attendance_info)

        f.write(str(student[0])+","+str(student[1])+","+str(student[2])+"\n")
    f.close()


    return redirect('/static/Attendance_Report.csv')




def teacher_view_student(request):
    cursor = connection.cursor()

    query = "SELECT name,address,mobile,email,gender,dob,class_div,class_teacher FROM user where type = 'student' "
    cursor.execute(query)
    res = cursor.fetchall()
    student_list = []
    for student in res:
        student_info = {"name": student[0], "address": student[1], "mobile": student[2], "email": student[3],
                        "gender": student[4], "dob": student[5], "class_div": student[6], "class_teacher": student[7]}
        student_list.append(student_info)

    return render(request,"teacher_view_student.html", {'student_list': student_list})






def view_attendance_student(request):

    if request.session.has_key('is_logged'):
        username = request.session['is_logged']
        print(username)

        cursor = connection.cursor()
        query = "SELECT u.class_teacher,p.is_present,p.date FROM user as u,present as p where username = '"+username+"' and u.id=p.user_id"
        cursor.execute(query)
        res = cursor.fetchall()
    

        student_list= []

        for student in res:
            students = {"class_teacher" : student[0],"is_present" : student[1], "date" : student[2]}
            student_list.append(students)

    return render(request,"view_attendance_student.html",{'students' : student_list})