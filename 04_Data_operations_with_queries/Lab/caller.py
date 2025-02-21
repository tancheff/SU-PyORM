import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Run and print your queries

from main_app.models import Student

# ---------- 1. Add Students ----------
def add_students(student_id, first_name, last_name, birth_date, email):
    new_student = Student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        email=email
    )
    new_student.save()

data = [
    ('FC5204', 'John', 'Doe', '1995-05-15', 'john.doe@university.com'),
    ('FE0054', 'Jane', 'Smith', None, 'jane.smith@university.com'),
    ('FH2014', 'Alice', 'Johnson', '1998-02-10', 'alice.johnson@university.com'),
    ('FH2015', 'Bob', 'Wilson', '1996-11-25', 'bob.wilson@university.com'),
]

for d in data:
    add_students(*d)


print(Student.objects.all())

# ---------- 2. Get Students Info ----------
def get_students_info():
    # student_model = apps.get_model('main_app', 'Student')
    # all_students = student_model.objects.all()
    all_students = Student.objects.all()

    result = []

    for student in all_students:
        result.append(f"Student №{Student.student_id}: "
                      f"{Student.first_name} {Student.last_name}; Email: {Student.email}")

    return "\n".join(result)

print(get_students_info())

# ---------- 3. Update Students' Emails ----------
def update_students_emails():
    all_students = Student.objects.all()

    for student in all_students:
        old_email = student.email.split("@")
        student.email = f"{old_email[0]}@uni-students.com"
        # student.email = f"{old_email[0]}@university.com"

        Student.objects.bulk_update(all_students, ['email'])


update_students_emails()
for student in Student.objects.all():
    print(student.email)

# # ---------- 4. Truncate Students ----------
# def truncate_students():
#     Student.objects.all().delete()
#
# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")

print(Student.objects.all())