from django.urls import path
from . import views
from .views import groups, get_fields, get_students



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

    path('groups-tutorial/', views.groups_student, name='groups_student'),
    path('get_fields_student/', views.get_fields_student, name='get_fields'),
    path('get_students/', views.get_students, name='get_students'),
    path('get-students-group/', views.get_students_group, name='get_students_group'),
]