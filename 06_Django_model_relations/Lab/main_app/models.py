from django.db import models

# Create your models here.

class Lecturer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    lecturer = models.ForeignKey(
        to=Lecturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"

class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    # subjects = models.ManyToManyField(Subject)

    subjects = models.ManyToManyField(to='Subject', through='StudentEnrollment')
    # relationship is defined as a string because model is created after this one
    # when providing the relationship as a string works because Django resolved them at runtime

"""
- unless otherwise specified the PK is created by Django
- PK is created as a field named 'id' (type=bigint)
- FK always references a model
- FK should always specify what happens on_delete

- to include a FK in the creation of an object, you need to refer to the instance of the FK
    i.e.:
    lecturer1 = Lecturer.objects.get(first_name="John", last_name="Doe")
    Subject.objects.create(name="Mathematics", code="MATH101", lecturer=lecturer1)

- models.ManyToManyField(name_of_model) creates a link table between two classes/models

"""

class StudentEnrollment(models.Model):
    class StudentGrades(models.TextChoices):
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'
        F = 'F', 'F'

    student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=1, choices=StudentGrades, blank=True, null=True)


class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(to=Lecturer, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    office_location = models.CharField(max_length=100, blank=True)
