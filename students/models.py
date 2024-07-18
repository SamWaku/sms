from django.db import models

# class AcademicYear(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class FieldOfStudy(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
#     gpa = models.FloatField()
#     year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'

# class TutorialGroup(models.Model):
#     name = models.CharField(max_length=50)
#     field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
#     academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True)
#     students = models.ManyToManyField(Student, related_name='tutorial_groups')

#     def __str__(self):
#         return self.name


# class AcademicYear(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class FieldOfStudy(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
#     gpa = models.FloatField()
#     year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'

# class TutorialGroup(models.Model):
#     name = models.CharField(max_length=50)
#     field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
#     academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True)
#     students = models.ManyToManyField(Student, related_name='tutorial_groups')

#     def __str__(self):
#         return self.name
# 
# Real code
# class AcademicYear(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class FieldOfStudy(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.CharField(max_length=50)  # Changed to CharField
#     gpa = models.FloatField()
#     year = models.CharField(max_length=50)  # Changed to CharField

#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'
    
#reeel 
class AcademicYear(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_number = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    school = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=50)  # Changed to CharField
    year = models.CharField(max_length=50)  # Changed to CharField

    def __str__(self):
        return f'Student: {self.first_name} {self.last_name}'

class TutorialGroup(models.Model):
    name = models.CharField(max_length=50)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='tutorial_groups')

    def __str__(self):
        return self.name

class CurrentCourse(models.Model):
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=50)
    course_short = models.CharField(max_length=50)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)  # Link to FieldOfStudy
    students = models.ManyToManyField(Student, related_name='current_courses')  # Link to Students

    def __str__(self):
        return self.course_name
    
class RepeatedCourse(models.Model):
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=50)
    course_short = models.CharField(max_length=50)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)  # Link to FieldOfStudy
    students = models.ManyToManyField(Student, related_name='repeated_courses')  # Link to Students

    def __str__(self):
        return self.course_name

# from django.db import models

# class AcademicYear(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class FieldOfStudy(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# # Updated Student model
# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
#     gpa = models.FloatField()
#     year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'

# from django.db import models

# class AcademicYear(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# class FieldOfStudy(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# # Create your models here.
# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.CharField(max_length=50)
#     gpa = models.FloatField()

    
#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'

# once
# class AcademicYear(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# class FieldOfStudy(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.CharField(max_length=50)  # Changed to CharField
#     gpa = models.FloatField()
#     year = models.CharField(max_length=50)  # Changed to CharField

#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'

# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)    
#     gpa = models.FloatField()
#     year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'


# class Student(models.Model):
#     student_number = models.PositiveIntegerField()
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=100)
#     field_of_study = models.CharField(max_length=50)
#     gpa = models.FloatField()
#     year = models.CharField(max_length=50)

#     def __str__(self):
#         return f'Student: {self.first_name} {self.last_name}'
