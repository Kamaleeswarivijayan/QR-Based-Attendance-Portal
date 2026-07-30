from students.models import Student
from teachers.models import Teacher


def user_role(request):

    role = None

    if request.user.is_authenticated:

        if request.user.is_superuser:
            role = "admin"

        elif Teacher.objects.filter(user=request.user).exists():
            role = "teacher"

        elif Student.objects.filter(user=request.user).exists():
            role = "student"

    return {
        "user_role": role
    }