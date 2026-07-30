from django.contrib.auth.models import User
from students.models import Department, Student
from teachers.models import Teacher
from attendance.models import Subject

# ==========================
# Departments
# ==========================
departments = [
    "Computer Science and Business Systems (CSBS)",
    "Computer Science Engineering (CSE)",
    "Artificial Intelligence and Data Science (AI&DS)",
    "Information Technology (IT)",
]

dept_objs = {}
for dept in departments:
    obj, _ = Department.objects.get_or_create(department_name=dept)
    dept_objs[dept] = obj

csbs = dept_objs["Computer Science and Business Systems (CSBS)"]

print("✅ Departments Created")

# ==========================
# Teachers
# ==========================
teachers = [
    ("rkumar", "R", "Kumar", "EMP001", "9876543210"),
    ("priya", "Priya", "S", "EMP002", "9876543211"),
    ("arjun", "Arjun", "K", "EMP003", "9876543212"),
    ("deepika", "Deepika", "R", "EMP004", "9876543213"),
    ("naveen", "Naveen", "P", "EMP005", "9876543214"),
]

teacher_objs = {}

for username, first, last, empid, phone in teachers:
    user, _ = User.objects.get_or_create(
        username=username,
        defaults={
            "first_name": first,
            "last_name": last,
            "email": f"{username}@college.com",
        },
    )

    if not user.has_usable_password():
        user.set_password("Teacher@123")
        user.save()

    teacher, _ = Teacher.objects.get_or_create(
        employee_id=empid,
        defaults={
            "user": user,
            "department": csbs,
            "phone": phone,
        },
    )

    teacher_objs[empid] = teacher

print("✅ Teachers Created")

# ==========================
# Subjects
# ==========================
subjects = [
    ("CCS355", "Neural Networks and Deep Learning", 6, "EMP001"),
    ("CCS356", "Object Oriented Software Engineering", 6, "EMP002"),
    ("CW3601", "Business Analytics", 6, "EMP003"),
    ("CCD334", "Supply Chain Management", 6, "EMP004"),
    ("CCB331", "Marketing Research and Marketing Management", 6, "EMP005"),
    ("CCS347", "Game Development", 6, "EMP001"),
]

for code, name, sem, empid in subjects:
    Subject.objects.get_or_create(
        subject_code=code,
        defaults={
            "subject_name": name,
            "semester": sem,
            "department": csbs,
            "teacher": teacher_objs[empid],
        },
    )

print("✅ Subjects Created")

# ==========================
# Students
# ==========================
student_names = [
    "Aakash", "Akash", "Anitha", "Arun", "Bharath",
    "Deepak", "Divya", "Gokul", "Hari", "Harini",
    "Jeeva", "Karthik", "Keerthana", "Logesh", "Monisha",
    "Naveen", "Nithya", "Pradeep", "Rahul", "Sakthi",
    "Sanjay", "Shruthi", "Sowmiya", "Varun", "Vignesh",
]

for i, name in enumerate(student_names, start=1):
    reg = f"511323244{str(i).zfill(3)}"

    user, _ = User.objects.get_or_create(
        username=reg,
        defaults={
            "first_name": name,
            "email": f"{name.lower()}@gmail.com",
        },
    )

    if not user.has_usable_password():
        user.set_password("Student@123")
        user.save()

    Student.objects.get_or_create(
        register_number=reg,
        defaults={
            "user": user,
            "department": csbs,
            "year": 3,
            "section": "A",
            "phone": f"987650{1000+i}",
        },
    )

print("✅ Students Created")
print("🎉 Demo data inserted successfully!")