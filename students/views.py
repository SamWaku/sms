from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse 
from .models import Student, AcademicYear, FieldOfStudy, TutorialGroup,RepeatedCourseStatus, CurrentCourseStatus
from .forms import StudentForm
from django.core.exceptions import ValidationError
from django.db.models import Count


from django.shortcuts import render
from django.core.mail import send_mail
from .models import Student
from .forms import StudentForm
from django.core.exceptions import ValidationError

from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404



def addstudent(request):
	return render (request,'students/add.html')

def courses(request):
    return render(request, 'students/courses.html' )

def index(request):
    return render(request, 'students/index.html', {
        'students': Student.objects.all()
    })

def view_student(request, id):
    student = Student.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                new_student = form.save()

                # Handle course assignments and carry status
                for course in form.cleaned_data['current_courses']:
                    CurrentCourseStatus.objects.create(
                        student=new_student,
                        course=course,
                        is_carried=request.POST.get(f'carry_{course.id}', False) == 'on'
                    )

                # Allocate the student to a tutorial group
                allocate_to_group(new_student)

                return render(request, 'students/add.html', {
                    'form': StudentForm(),
                    'success': True
                })
            except ValidationError as e:
                form.add_error('student_number', e)
        else:
            return render(request, 'students/add.html', {
                'form': form,
                'success': False
            })
    else:
        form = StudentForm()
        return render(request, 'students/add.html', {
            'form': form,
            'success': False
        })


def allocate_to_group(student):
    max_group_size = 4
    field_of_study = student.field_of_study

    # Find or create the appropriate tutorial group
    group = (TutorialGroup.objects
             .filter(field_of_study__name=field_of_study)
             .annotate(num_students=Count('students'))
             .filter(num_students__lt=max_group_size)
             .first())

    if not group:
        group_name = f'{field_of_study} Group {TutorialGroup.objects.filter(field_of_study__name=field_of_study).count() + 1}'
        field_of_study_obj, created = FieldOfStudy.objects.get_or_create(name=field_of_study)
        academic_year_obj, created = AcademicYear.objects.get_or_create(name=student.year)
        group = TutorialGroup.objects.create(
            name=group_name,
            field_of_study=field_of_study_obj,
            academic_year=academic_year_obj
        )

    group.students.add(student)
    group.save()


def groups(request):
    # Fetch distinct years and fields of study
    distinct_years = Student.objects.values_list('year', flat=True).distinct()
    distinct_fields = Student.objects.values_list('field_of_study', flat=True).distinct()

    # Group students by year and field of study
    grouped_students = {}
    for student in Student.objects.all():
        year = student.year
        field_of_study = student.field_of_study
        if year not in grouped_students:
            grouped_students[year] = {}
        if field_of_study not in grouped_students[year]:
            grouped_students[year][field_of_study] = []
        grouped_students[year][field_of_study].append(student)

    return render(request, 'students/groups.html', {
        'grouped_students': grouped_students,
        'distinct_years': distinct_years,
        'distinct_fields': distinct_fields
    })

def get_fields(request):
    year = request.GET.get('year')
    fields = Student.objects.filter(year=year).values_list('field_of_study', flat=True).distinct()
    return JsonResponse(list(fields), safe=False)


def get_students(request):
    year = request.GET.get('year')
    field = request.GET.get('field')
    students = Student.objects.filter(year=year, field_of_study=field).values(
        'student_number', 'first_name', 'last_name', 'email', 'school', 'field_of_study', 'year'
    )
    return JsonResponse(list(students), safe=False)


def groupslist(request):
    # Fetch distinct years and fields of study
    distinct_years = Student.objects.values_list('year', flat=True).distinct()
    distinct_fields = Student.objects.values_list('field_of_study', flat=True).distinct()

    # Initialize an empty dictionary to store grouped students
    grouped_students = {}

    # Loop over distinct years and fields of study
    for year in distinct_years:
        for field in distinct_fields:
            # Filter students based on the current year and field of study
            students = Student.objects.filter(year=year, field_of_study=field)
            # Add the filtered students to the grouped_students dictionary
            grouped_students[(year, field)] = students

    return render(request, 'students/groups.html', {
        'grouped_students': grouped_students,
        'distinct_years': distinct_years,
        'distinct_fields': distinct_fields
    })


def studentgroups(request):
    groups = TutorialGroup.objects.prefetch_related('students').all()
    return render(request, 'students/student-groups.html', {'studentgroups': groups})

def get_fields_student(request):
    year = request.GET.get('year')
    fields = Student.objects.filter(year__name=year).values_list('field_of_study__name', flat=True).distinct()
    return JsonResponse(list(fields), safe=False)


def groups_student(request):
    distinct_groups = TutorialGroup.objects.values_list('name', flat=True).distinct()
    return render(request, 'students/student-groups.html', {
        'distinct_groups': distinct_groups,
    })

def get_students_group(request):
    group_name = request.GET.get('group')
    students = Student.objects.filter(tutorial_groups__name=group_name).values(
        'id', 'student_number', 'first_name', 'last_name', 'email', 'school', 'field_of_study', 'year'
    )

    students_list = []
    for student in students:
        current_courses = list(CurrentCourseStatus.objects.filter(student_id=student['id']).values_list('course__course_name', flat=True))
        repeated_courses = list(RepeatedCourseStatus.objects.filter(student_id=student['id']).values_list('course__course_name', flat=True))

        student_dict = {
            'student_number': student['student_number'],
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'email': student['email'],
            'school': student['school'],
            'field_of_study': student['field_of_study'],
            'year': student['year'],
            'current_courses': current_courses if current_courses else ["No courses available"],
            'repeated_courses': repeated_courses if repeated_courses else ["No courses available"],
        }
        students_list.append(student_dict)

    return JsonResponse(students_list, safe=False)


# def get_students_group(request):
#     group_name = request.GET.get('group')
    
#     # Fetch students based on the group name
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'id', 'student_number', 'first_name', 'last_name', 'email', 'school', 'field_of_study', 'year'
#     )

#     students_list = []
#     for student in students:
#         # Get the current and repeated courses using the student ID (primary key)
#         current_courses = list(CurrentCourseStatus.objects.filter(student_id=student['id']).values_list('course__course_name', flat=True))
#         repeated_courses = list(RepeatedCourseStatus.objects.filter(student_id=student['id']).values_list('course__course_name', flat=True))

#         # Build the student dictionary
#         student_dict = {
#             'student_number': student['student_number'],
#             'first_name': student['first_name'],
#             'last_name': student['last_name'],
#             'email': student['email'],
#             'school': student['school'],
#             'field_of_study': student['field_of_study'],
#             'year': student['year'],
#             'current_courses': current_courses if current_courses else ['No current courses'],
#             'repeated_courses': repeated_courses if repeated_courses else ['No repeated courses'],
#         }
#         students_list.append(student_dict)

#     return JsonResponse(students_list, safe=False)


# def get_students_group(request):
#     group_name = request.GET.get('group')
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'student_number', 'first_name', 'last_name', 'email', 'school', 'field_of_study', 'year'
#     )

#     students_list = []
#     for student in students:
#         student_dict = {
#             'student_number': student['student_number'],
#             'first_name': student['first_name'],
#             'last_name': student['last_name'],
#             'email': student['email'],
#             'school': student['school'],
#             'field_of_study': student['field_of_study'],
#             'year': student['year'],
#             'current_courses': list(CurrentCourseStatus.objects.filter(student_id=student['student_number']).values_list('course__course_name', flat=True)),
#             'repeated_courses': list(RepeatedCourseStatus.objects.filter(student_id=student['student_number']).values_list('course__course_name', flat=True)),
#         }
#         students_list.append(student_dict)

#     return JsonResponse(students_list, safe=False)


# def get_students_group(request):
#     group_name = request.GET.get('group')
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'student_number', 'first_name', 'last_name', 'email', 'school', 'field_of_study', 'year'
#     )

#     # Iterate over students to add current and repeated courses
#     students_list = []
#     for student in students:
#         student_dict = {
#             'student_number': student['student_number'],
#             'first_name': student['first_name'],
#             'last_name': student['last_name'],
#             'email': student['email'],
#             'school': student['school'],
#             'field_of_study': student['field_of_study'],
#             'year': student['year'],
#             'current_courses': list(CurrentCourseStatus.objects.filter(student_id=student['student_number']).values_list('course__course_name', flat=True)),
#             'repeated_courses': list(RepeatedCourseStatus.objects.filter(student_id=student['student_number']).values_list('course__course_name', flat=True)),
#         }
#         students_list.append(student_dict)

#     return JsonResponse(students_list, safe=False)


# def get_students_group(request):
#     group_name = request.GET.get('group')
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'school', 'year'
#     )
#     return JsonResponse(list(students), safe=False)

def add_student_courses(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    CurrentCourseStatusFormSet = modelformset_factory(CurrentCourseStatus, form=CurrentCourseStatusForm, extra=5)
    RepeatedCourseStatusFormSet = modelformset_factory(RepeatedCourseStatus, form=RepeatedCourseStatusForm, extra=5)

    if request.method == 'POST':
        current_course_formset = CurrentCourseStatusFormSet(request.POST, queryset=CurrentCourseStatus.objects.filter(student=student))
        repeated_course_formset = RepeatedCourseStatusFormSet(request.POST, queryset=RepeatedCourseStatus.objects.filter(student=student))
        
        if current_course_formset.is_valid() and repeated_course_formset.is_valid():
            current_courses = current_course_formset.save(commit=False)
            for current_course in current_courses:
                current_course.student = student
                current_course.save()

            repeated_courses = repeated_course_formset.save(commit=False)
            for repeated_course in repeated_courses:
                repeated_course.student = student
                repeated_course.save()

            return redirect('index')
    else:
        current_course_formset = CurrentCourseStatusFormSet(queryset=CurrentCourseStatus.objects.filter(student=student))
        repeated_course_formset = RepeatedCourseStatusFormSet(queryset=RepeatedCourseStatus.objects.filter(student=student))

    return render(request, 'students/add-course.html', {
        'current_course_formset': current_course_formset,
        'repeated_course_formset': repeated_course_formset,
        'student': student,
    })

def view_student(request, id):
    student = get_object_or_404(Student, pk=id)
    current_courses = CurrentCourseStatus.objects.filter(student=student)
    repeated_courses = RepeatedCourseStatus.objects.filter(student=student)
    return render(request, 'students/list-courses.html', {
        'student': student,
        'current_courses': current_courses,
        'repeated_courses': repeated_courses,
    })

# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             try:
#                 new_student_number = form.cleaned_data['student_number']
#                 new_first_name = form.cleaned_data['first_name']
#                 new_last_name = form.cleaned_data['last_name']
#                 new_email = form.cleaned_data['email']
#                 new_school = form.cleaned_data['school']
#                 new_field_of_study = form.cleaned_data['field_of_study']
#                 new_year = form.cleaned_data['year']

#                 # Create the student object
#                 new_student = Student(
#                     student_number=new_student_number,
#                     first_name=new_first_name,
#                     last_name=new_last_name,
#                     email=new_email,
#                     school=new_school,
#                     field_of_study=new_field_of_study,
#                     year=new_year
#                 )
#                 new_student.save()

#                 # Allocate the student to a tutorial group
#                 allocate_to_group(new_student)

#                 # Send confirmation email
#                 # send_mail(
#                 #     'Welcome to Our School',
#                 #     f'Dear {new_first_name},\n\nThank you for registering with us. We are excited to have you join our group.',
#                 #     'chitailapious1@gmail.com',  # From email
#                 #     [new_email],  # To email
#                 #     fail_silently=False,
#                 # )

#                 return render(request, 'students/add.html', {
#                     'form': StudentForm(),
#                     'success': True
#                 })
#             except ValidationError as e:
#                 form.add_error('student_number', e)
#         else:
#             return render(request, 'students/add.html', {
#                 'form': form,
#                 'success': False
#             })
#     else:
#         form = StudentForm()
#         return render(request, 'students/add.html', {
#             'form': form,
#             'success': False
#         })



# def get_fields(request):
#     year = request.GET.get('year')
#     fields = Student.objects.filter(year=year).values_list('field_of_study', flat=True).distinct()
#     return JsonResponse(list(fields), safe=False)

# def allocate_to_group(student):
#     max_group_size = 4
#     field_of_study = student.field_of_study

#     # Find or create the appropriate tutorial group
#     group = (TutorialGroup.objects
#              .filter(field_of_study=field_of_study)
#              .annotate(num_students=Count('students'))
#              .filter(num_students__lt=max_group_size)
#              .first())

#     if not group:
#         group_name = f'{field_of_study.name} Group {TutorialGroup.objects.filter(field_of_study=field_of_study).count() + 1}'
#         group = TutorialGroup.objects.create(
#             name=group_name,
#             field_of_study=field_of_study
#         )

#     group.students.add(student)
#     group.save()

# View to render the main student groups page
# def groups_student(request):
#     distinct_groups = TutorialGroup.objects.values_list('name', flat=True).distinct()
#     return render(request, 'students/student-groups.html', {
#         'distinct_groups': distinct_groups,
#     })

# API endpoint to get students in a specific group
# def get_students_group(request):
#     group_name = request.GET.get('group')
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa', 'year'
#     )
#     return JsonResponse(list(students), safe=False)

# def get_students_group(request):
#     group_name = request.GET.get('group')
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'student_number', 'first_name', 'last_name', 'email', 'field_of_study__name', 'gpa', 'year__name'
#     )
#     return JsonResponse(list(students), safe=False)

# Create your views here.
# def studentgroups(request):
#     return render (request, 'students/groups.html')


# def allocate_to_group(student):
#     max_group_size = 4
#     field_of_study = student.field_of_study

#     # Find or create the appropriate tutorial group
#     group = (TutorialGroup.objects
#              .filter(field_of_study=field_of_study)
#              .annotate(num_students=Count('students'))
#              .filter(num_students__lt=max_group_size)
#              .first())

#     if not group:
#         group_name = f'{field_of_study.name} Group {TutorialGroup.objects.filter(field_of_study=field_of_study).count() + 1}'
#         group = TutorialGroup.objects.create(
#             name=group_name,
#             field_of_study=field_of_study,
#             academic_year=None  # Remove academic year if it's no longer relevant
#         )

#     group.students.add(student)
#     group.save()


# def allocate_to_group(student):
#     max_group_size = 4
#     field_of_study = student.field_of_study
#     academic_year = student.year

#     # Find or create the appropriate tutorial group
#     group = (TutorialGroup.objects
#              .filter(field_of_study=field_of_study, academic_year=academic_year)
#              .annotate(num_students=Count('students'))
#              .filter(num_students__lt=max_group_size)
#              .first())

#     if not group:
#         group = TutorialGroup.objects.create(
#             field_of_study=field_of_study,
#             academic_year=academic_year
#         )

#     group.students.add(student)
#     group.save()


# def allocate_to_group(student):
#     max_group_size = 4
#     field_of_study = student.field_of_study
#     academic_year = student.year

#     # Find or create the appropriate tutorial group
#     group = (TutorialGroup.objects
#              .filter(field_of_study=field_of_study, academic_year=academic_year)
#              .annotate(num_students=Count('students'))
#              .filter(num_students__lt=max_group_size)
#              .first())

#     if not group:
#         group_name = f'{field_of_study.name} {academic_year.name} Group {TutorialGroup.objects.count() + 1}'
#         group = TutorialGroup.objects.create(
#             name=group_name,
#             field_of_study=field_of_study,
#             academic_year=academic_year
#         )

#     group.students.add(student)
#     group.save()


# def get_students_group(request):
#     group_name = request.GET.get('group')
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'student_number', 'first_name', 'last_name', 'email', 'field_of_study__name', 'gpa', 'year__name'
#     )
#     return JsonResponse(list(students), safe=False)

# def get_students_group(request):
#     group_name = request.GET.get('group')

#     if group_name:
#         # Assuming 'group' parameter is the name of the TutorialGroup
#         group = TutorialGroup.objects.get(name=group_name)

#         # Get all students in the tutorial group
#         students = group.students.all()

#         context = {
#             'students': students,
#         }

#         return render(request, 'students/student-groups.html', context)
#     else:
#         # Handle the case where 'group' parameter is not provided
#         # Redirect or return an appropriate response
#         pass


# def get_students_group(request):
#     group_name = request.GET.get('group')
#     students = Student.objects.filter(tutorial_groups__name=group_name).values(
#         'student_number', 'first_name', 'last_name', 'email', 'field_of_study__name', 'gpa', 'year__name'
#     )
#     return JsonResponse(list(students), safe=False)

# def groups_student(request):
#     distinct_groups = TutorialGroup.objects.values_list('name', flat=True).distinct()
#     return render(request, 'students/student-groups.html', {
#         'distinct_groups': distinct_groups,
#     })

# def get_students(request):
#     year = request.GET.get('year')
#     field = request.GET.get('field')
#     students = Student.objects.filter(year=year, field_of_study=field).values(
#         'student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa', 'year'
#     )
#     return JsonResponse(list(students), safe=False)


# def get_students(request):
#     year = request.GET.get('year')
#     field = request.GET.get('field')
#     students = Student.objects.filter(year=year, field_of_study=field).values('first_name', 'last_name')
#     return JsonResponse(list(students), safe=False)

# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             new_student_number = form.cleaned_data['student_number']
#             new_first_name = form.cleaned_data['first_name']
#             new_last_name = form.cleaned_data['last_name']
#             new_email = form.cleaned_data['email']
#             new_field_of_study = form.cleaned_data['field_of_study']
#             new_gpa = form.cleaned_data['gpa']
#             new_year = form.cleaned_data['year']

#             # Get or create the field of study
#             field_of_study, created = FieldOfStudy.objects.get_or_create(name=new_field_of_study)

#             # Get or create the academic year
#             academic_year, created = AcademicYear.objects.get_or_create(name=new_year)

#             # Create the student object
#             new_student = Student(
#                 student_number=new_student_number,
#                 first_name=new_first_name,
#                 last_name=new_last_name,
#                 email=new_email,
#                 field_of_study=field_of_study.name,  # Assuming you want to store the name
#                 gpa=new_gpa,
#                 year=academic_year.name  # Assuming you want to store the name
#             )
#             new_student.save()

#             # Allocate the student to a tutorial group
#             allocate_to_group(new_student)

#             return render(request, 'students/add.html', {
#                 'form': StudentForm(),
#                 'success': True
#             })
#     else:
#         form = StudentForm()
#     return render(request, 'students/add.html', {
#         'form': form
#     })

# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             new_student_number = form.cleaned_data['student_number']
#             new_first_name = form.cleaned_data['first_name']
#             new_last_name = form.cleaned_data['last_name']
#             new_email = form.cleaned_data['email']
#             new_field_of_study = form.cleaned_data['field_of_study']
#             new_gpa = form.cleaned_data['gpa']
#             new_year = form.cleaned_data['year']

#             # Get or create the field of study
#             field_of_study, created = FieldOfStudy.objects.get_or_create(name=new_field_of_study)

#             # Get or create the academic year
#             academic_year, created = AcademicYear.objects.get_or_create(name=new_year)

#             # Create the student object
#             new_student = Student(
#                 student_number=new_student_number,
#                 first_name=new_first_name,
#                 last_name=new_last_name,
#                 email=new_email,
#                 field_of_study=field_of_study,
#                 gpa=new_gpa,
#                 year=academic_year
#             )
#             new_student.save()

#             # Allocate the student to a tutorial group
#             allocate_to_group(new_student)

#             return render(request, 'students/add.html', {
#                 'form': StudentForm(),
#                 'success': True
#             })
#     else:
#         form = StudentForm()
#     return render(request, 'students/add.html', {
#         'form': form
#     })

# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             new_student_number = form.cleaned_data['student_number']
#             new_first_name = form.cleaned_data['first_name']
#             new_last_name = form.cleaned_data['last_name']
#             new_email = form.cleaned_data['email']
#             new_field_of_study = form.cleaned_data['field_of_study']
#             new_gpa = form.cleaned_data['gpa']
#             new_year = form.cleaned_data['year']

#             # Get or create the field of study
#             field_of_study, created = FieldOfStudy.objects.get_or_create(name=new_field_of_study)

#             new_student = Student(
#                 student_number=new_student_number,
#                 first_name=new_first_name,
#                 last_name=new_last_name,
#                 email=new_email,
#                 field_of_study=field_of_study,
#                 gpa=new_gpa,
#                 year=new_year  # Remove year if you don't need it
#             )
#             new_student.save()

#             # Allocate the student to a tutorial group
#             allocate_to_group(new_student)

#             return render(request, 'students/add.html', {
#                 'form': StudentForm(),
#                 'success': True
#             })
#     else:
#         form = StudentForm()
#     return render(request, 'students/add.html', {
#         'form': form
#     })

# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add')  # Replace 'index' with the name of your view
#     else:
#         form = StudentForm()
#     return render(request, 'students/add.html', {'form': form})

# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             new_student_number = form.cleaned_data['student_number']
#             new_first_name = form.cleaned_data['first_name']
#             new_last_name = form.cleaned_data['last_name']
#             new_email = form.cleaned_data['email']
#             new_field_of_study = form.cleaned_data['field_of_study']
#             new_gpa = form.cleaned_data['gpa']
#             new_year = form.cleaned_data['year']

#             # Get or create the academic year
#             academic_year, created = AcademicYear.objects.get_or_create(name=new_year)

#             # Get or create the field of study
#             field_of_study, created = FieldOfStudy.objects.get_or_create(name=new_field_of_study)

#             new_student = Student(
#                 student_number=new_student_number,
#                 first_name=new_first_name,
#                 last_name=new_last_name,
#                 email=new_email,
#                 field_of_study=field_of_study,
#                 gpa=new_gpa,
#                 year=academic_year,
#             )
#             new_student.save()

#             # Allocate the student to a tutorial group
#             allocate_to_group(new_student)

#             return render(request, 'students/add.html', {
#                 'form': StudentForm(),
#                 'success': True
#             })
#     else:
#         form = StudentForm()
#     return render(request, 'students/add.html', {
#         'form': form
#     })


# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             new_student_number = form.cleaned_data['student_number']
#             new_first_name = form.cleaned_data['first_name']
#             new_last_name = form.cleaned_data['last_name']
#             new_email = form.cleaned_data['email']
#             new_field_of_study = form.cleaned_data['field_of_study']
#             new_gpa = form.cleaned_data['gpa']
#             new_year = form.cleaned_data['year']

#             # Get or create the academic year
#             academic_year, created = AcademicYear.objects.get_or_create(name=new_year)

#             # Get or create the field of study
#             field_of_study, created = FieldOfStudy.objects.get_or_create(name=new_field_of_study)

#             new_student = Student(
#                 student_number=new_student_number,
#                 first_name=new_first_name,
#                 last_name=new_last_name,
#                 email=new_email,
#                 field_of_study=field_of_study.name,
#                 gpa=new_gpa,
#                 year=academic_year.name,
#             )
#             new_student.save()
#             return render(request, 'students/add.html', {
#                 'form': StudentForm(),
#                 'success': True
#             })
#     else:
#         form = StudentForm()
#     return render(request, 'students/add.html', {
#         'form': form
#     })

# def add(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             new_student_number = form.cleaned_data['student_number']
#             new_first_name = form.cleaned_data['first_name']
#             new_last_name = form.cleaned_data['last_name']
#             new_email = form.cleaned_data['email']
#             new_field_of_study = form.cleaned_data['field_of_study']
#             new_gpa = form.cleaned_data['gpa']
#             new_year = form.cleaned_data['year']

#             # Get or create the field of study
#             field_of_study, created = FieldOfStudy.objects.get_or_create(name=new_field_of_study)

#             # Get or create the academic year
#             academic_year, created = AcademicYear.objects.get_or_create(name=new_year)

#             # Create the student object
#             new_student = Student(
#                 student_number=new_student_number,
#                 first_name=new_first_name,
#                 last_name=new_last_name,
#                 email=new_email,
#                 field_of_study=field_of_study.name,  # Assuming you want to store the name
#                 gpa=new_gpa,
#                 year=academic_year.name  # Assuming you want to store the name
#             )
#             new_student.save()

#             # Allocate the student to a tutorial group
#             allocate_to_group(new_student)

#             return render(request, 'students/add.html', {
#                 'form': StudentForm(),
#                 'success': True
#             })
#     else:
#         form = StudentForm()
#     return render(request, 'students/add.html', {
#         'form': form
#     })
