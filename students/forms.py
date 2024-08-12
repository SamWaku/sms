from django import forms
from .models import Student, CurrentCourse, AcademicYear, FieldOfStudy, CurrentCourseStatus, RepeatedCourseStatus


class StudentForm(forms.ModelForm):
    current_courses = forms.ModelMultipleChoiceField(
        queryset=CurrentCourse.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Current Courses"
    )

    class Meta:
        model = Student
        fields = ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'year', 'school', 'current_courses']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['field_of_study'].widget.attrs.update({
            'class': 'form-control',
            'onchange': 'updateCourses()',
            'id': 'field_of_study'
        })
        self.fields['year'].widget.attrs.update({'class': 'form-control'})

    def clean_student_number(self):
        student_number = self.cleaned_data.get('student_number')
        if Student.objects.filter(student_number=student_number).exists():
            raise forms.ValidationError("A student with this student number already exists.")
        return student_number

    
class CurrentCourseStatusForm(forms.ModelForm):
    class Meta:
        model = CurrentCourseStatus
        fields = ['course', 'is_carried']

class RepeatedCourseStatusForm(forms.ModelForm):
    class Meta:
        model = RepeatedCourseStatus
        fields = ['course', 'is_carried']

# real
# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_number', 'first_name', 'last_name', 'email','field_of_study', 'year','school' ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # You can customize the form widgets or leave them as default inputs
#         self.fields['field_of_study'].widget.attrs.update({'class': 'form-control'})
#         self.fields['year'].widget.attrs.update({'class': 'form-control'})

# from django import forms
# from .models import Student

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa']
#         labels = {
#             'student_number': 'Student Number',
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'email': 'Email',
#             'field_of_study': 'Field of Study',
#             'gpa': 'GPA'
#         }

#         widgets = {
#             'student_number': forms.NumberInput(attrs={'class': 'form-control'}),
#             'frist_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
#             'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
#         }


# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa', 'year']
#         labels = {
#             'student_number': 'Student Number',
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'email': 'Email',
#             'field_of_study': 'Field of Study',
#             'gpa': 'GPA',
#             'year': 'Academic Year'
#         }
#         widgets = {
#             'student_number': forms.NumberInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'field_of_study': forms.Select(attrs={'class': 'form-control'}),
#             'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
#             'year': forms.Select(attrs={'class': 'form-control'}),
#         }


# here
# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa', 'year']
#         widgets = {
#             'field_of_study': forms.Select(choices=FieldOfStudy.objects.all()),
#             'year': forms.Select(choices=AcademicYear.objects.all()),
#         }

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa', 'year']

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa', 'year']
#         labels = {
#             'student_number': 'Student Number',
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'email': 'Email',
#             'field_of_study': 'Field of Study',
#             'gpa': 'GPA',
#             'year': 'Year',
#         }
#         widgets = {
#             'student_number': forms.NumberInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
#             'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
#             'year': forms.TextInput(attrs={'class': 'form-control'}),
#         }
