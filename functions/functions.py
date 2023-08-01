from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.sessions.models import Session

def add_student_function(request):
    cursor = connection.cursor()

    query = "SELECT name,id FROM user WHERE type = 'teacher' "
    cursor.execute(query)
    res = cursor.fetchall()
    teacher_list = []
    for teacher in res:
        teacher_list.append(teacher[0])

    return render_to_response("add_student.html", {'result': teacher_list})