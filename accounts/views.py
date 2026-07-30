from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from students.models import Student
from teachers.models import Teacher
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from students.models import Student
from teachers.models import Teacher


def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return redirect("login")

        # ---------------- ADMIN ----------------

        if role == "admin":

            if user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")

            messages.error(request, "You are not an Admin.")
            return redirect("login")

        # ---------------- TEACHER ----------------

        elif role == "teacher":

            if Teacher.objects.filter(user=user).exists():
                login(request, user)
                return redirect("teacher_dashboard")

            messages.error(request, "Teacher account not found.")
            return redirect("login")

        # ---------------- STUDENT ----------------

        elif role == "student":

            if Student.objects.filter(user=user).exists():
                login(request, user)
                return redirect("student_dashboard")

            messages.error(request, "Student account not found.")
            return redirect("login")

        messages.error(request, "Invalid Role.")
        return redirect("login")

    return render(request, "accounts/login.html")