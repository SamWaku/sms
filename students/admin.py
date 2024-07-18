from django.contrib import admin
from .models import Student,AcademicYear, FieldOfStudy, TutorialGroup, CurrentCourse, RepeatedCourse

# Register your models here.
admin.site.register(Student)
admin.site.register(AcademicYear)
admin.site.register(FieldOfStudy)
admin.site.register(TutorialGroup)
admin.site.register(CurrentCourse)
admin.site.register(RepeatedCourse)