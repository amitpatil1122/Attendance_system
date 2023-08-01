"""Attendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.static import serve
from django.contrib import admin
from myapp.views import login,admin_view,add_teacher,validate_login,register_teacher,add_student,admin_add_student,view_teacher,view_student,teacher_view,student_view,logout,attendance,view_attendance,view_attend,teacher_view_student,view_attendance_student,export_attendance

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(r'^$',login),
    path(r'^admin_view/',admin_view),
    path(r'^add_teacher/',add_teacher),
    path(r'^validate_login/',validate_login),
    path(r'^register_teacher/',register_teacher),
    path(r'^add_student/',add_student),
    path(r'^admin_add_student/',admin_add_student),
    path(r'^view_teacher/',view_teacher),
    path(r'^view_student/',view_student),
    path(r'^teacher_view/',teacher_view),
    path(r'^student_view/',student_view),
    path(r'^logout/',logout),
    path(r'^attendance/',attendance),
    path(r'^view_attendance/',view_attendance),
    path(r'^view_attend/',view_attend),
    path(r'^teacher_view_student/',teacher_view_student),
    path(r'^view_attendance_student/',view_attendance_student),
    path(r'^export_attendance/',export_attendance)

]
