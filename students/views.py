from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from accounts.decorators import student_required, admin_required
from .models import Student, Department
from attendance.models import Attendance


# ===========================
# Student Profile (Display only)
# ===========================

@login_required
@student_required
def student_profile(request):
    student = Student.objects.get(user=request.user)

    # POST handling removed – edit now on separate page

    present = Attendance.objects.filter(
        student=student,
        status="Present"
    ).count()

    absent = Attendance.objects.filter(
        student=student,
        status="Absent"
    ).count()

    late = Attendance.objects.filter(
        student=student,
        status="Late"
    ).count()

    total = Attendance.objects.filter(
        student=student
    ).count()

    percentage = 0
    if total > 0:
        percentage = round((present / total) * 100, 2)

    recent_attendance = Attendance.objects.select_related(
        "attendance_session__subject"
    ).filter(
        student=student
    ).order_by("-scan_time")[:10]

    context = {
        "student": student,
        "present": present,
        "absent": absent,
        "late": late,
        "total": total,
        "percentage": percentage,
        "recent_attendance": recent_attendance,
    }

    return render(request, "student/profile.html", context)


# ===========================
# Edit Student Profile
# ===========================

@login_required
@student_required
def edit_student_profile(request):
    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("student_profile")

    return render(request, "student/edit_profile.html")


# ===========================
# Student Change Password
# ===========================

@login_required
@student_required
def student_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("student_profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "student/change_password.html", {"form": form})


# ===========================
# Student Dashboard
# ===========================

@login_required
@student_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    return render(request, "student/student_dashboard.html", {"student": student})


# ===========================
# Student List (Admin only)
# ===========================

@login_required
@admin_required
def student_list(request):
    query = request.GET.get("q")
    students = Student.objects.select_related("user", "department")

    if query:
        students = students.filter(
            Q(register_number__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(department__department_name__icontains=query) |
            Q(section__icontains=query)
        )

    context = {"students": students, "query": query}
    return render(request, "student/student_list.html", context)


# ===========================
# Delete Student
# ===========================

@login_required
@admin_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.user.delete()
    messages.success(request, "Student Deleted Successfully.")
    return redirect("student_list")


# ===========================
# Add Student (Admin only)
# ===========================

@login_required
@admin_required
def add_student(request):
    departments = Department.objects.all()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        register_number = request.POST["register_number"]
        department_id = request.POST["department"]
        year = request.POST["year"]
        section = request.POST["section"]
        phone = request.POST["phone"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("add_student")

        if Student.objects.filter(register_number=register_number).exists():
            messages.error(request, "Register Number already exists.")
            return redirect("add_student")

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        Student.objects.create(
            user=user,
            register_number=register_number,
            department_id=department_id,
            year=year,
            section=section,
            phone=phone,
        )

        messages.success(request, "Student Added Successfully.")
        return redirect("student_list")

    return render(request, "student/student_add.html", {"departments": departments})


# ===========================
# Edit Student (Admin only)
# ===========================

@login_required
@admin_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    departments = Department.objects.all()

    if request.method == "POST":
        student.user.first_name = request.POST["first_name"]
        student.user.last_name = request.POST["last_name"]
        student.user.email = request.POST["email"]
        student.user.save()

        student.register_number = request.POST["register_number"]
        student.department_id = request.POST["department"]
        student.year = request.POST["year"]
        student.section = request.POST["section"]
        student.phone = request.POST["phone"]
        student.save()

        messages.success(request, "Student Updated Successfully.")
        return redirect("student_list")

    return render(
        request,
        "student/student_edit.html",
        {"student": student, "departments": departments}
    )