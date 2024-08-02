from django.urls import path
from . import views
from .views import groups, get_fields, get_students, add_student_courses, view_student



urlpatterns = [
    path('home', views.index, name='index'),
    path('<int:id>', views.view_student, name='view_student'),
    path('add', views.add, name='add'),
    path('add-student', views.addstudent),
    # path('student-groups', views.studentgroups),
    path('groups', views.groups),
    path('get-fields/', get_fields, name='get_fields'),
    path('get-students/', get_students, name='get_students'),
    path('student-groups/', views.studentgroups, name='studentgroups'),
    path('student-courses/', views.courses, name='studentcourses'),

    path('groups-tutorial/', views.groups_student, name='groups_student'),
    path('get_fields_student/', views.get_fields_student, name='get_fields'),
    path('get_students/', views.get_students, name='get_students'),
    path('get-students-group/', views.get_students_group, name='get_students_group'),

    path('add-course/', views.add_student_courses, name='add_student_courses'),
    path('list-courses/', views.add_student_courses, name='add_student_courses')

]