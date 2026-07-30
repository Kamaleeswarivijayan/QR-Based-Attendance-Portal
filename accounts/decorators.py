from functools import wraps
from django.shortcuts import redirect, render
from students.models import Student
from teachers.models import Teacher


# ---------------- Admin Only ----------------

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # User not logged in
        if not request.user.is_authenticated:
            return redirect("login")

        # Admin access
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Access denied
        return render(request, "errors/403.html", status=403)

    return wrapper


# ---------------- Teacher Only ----------------

def teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # User not logged in
        if not request.user.is_authenticated:
            return redirect("login")

        # Teacher access
        if Teacher.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)

        # Access denied
        return render(request, "errors/403.html", status=403)

    return wrapper


# ---------------- Student Only ----------------

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # User not logged in
        if not request.user.is_authenticated:
            return redirect("login")

        # Student access
        if Student.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)

        # Access denied
        return render(request, "errors/403.html", status=403)

    return wrapper


# ---------------- Admin OR Teacher ----------------

def admin_or_teacher_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # User not logged in
        if not request.user.is_authenticated:
            return redirect("login")

        # Admin access
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Teacher access
        if Teacher.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)

        # Access denied
        return render(request, "errors/403.html", status=403)

    return wrapper


# ---------------- Admin OR Student ----------------

def admin_or_student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # User not logged in
        if not request.user.is_authenticated:
            return redirect("login")

        # Admin access
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Student access
        if Student.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)

        # Access denied
        return render(request, "errors/403.html", status=403)

    return wrapper