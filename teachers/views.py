from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from accounts.decorators import admin_required, teacher_required
from students.models import Department
from attendance.models import Attendance, AttendanceSession
from .models import Teacher

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# ===========================
# Teacher Dashboard
# ===========================

@login_required
@teacher_required
def teacher_dashboard(request):
    return render(request, "teacher/dashboard.html")


# ===========================
# Teacher Profile (Display only)
# ===========================

@login_required
@teacher_required
def teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)

    # POST handling removed – edit now on separate page

    total_sessions = AttendanceSession.objects.filter(teacher=teacher).count()
    total_attendance = Attendance.objects.filter(
        attendance_session__teacher=teacher
    ).count()

    context = {
        "teacher": teacher,
        "total_sessions": total_sessions,
        "total_attendance": total_attendance,
    }

    return render(request, "teacher/profile.html", context)


# ===========================
# Edit Teacher Profile
# ===========================

@login_required
@teacher_required
def edit_teacher_profile(request):
    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("teacher_profile")

    return render(request, "teacher/edit_profile.html")


# ===========================
# Teacher Change Password
# ===========================

@login_required
@teacher_required
def teacher_change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("teacher_profile")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "teacher/change_password.html", {"form": form})


# ===========================
# Teacher List
# ===========================

@login_required
@admin_required
def teacher_list(request):
    query = request.GET.get("q")
    teachers = Teacher.objects.select_related("user", "department")

    if query:
        teachers = teachers.filter(
            Q(employee_id__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(department__department_name__icontains=query)
        )

    return render(
        request,
        "teacher/teacher_list.html",
        {"teachers": teachers, "query": query},
    )


# ===========================
# Add Teacher
# ===========================

@login_required
@admin_required
def add_teacher(request):
    departments = Department.objects.all()

    if request.method == "POST":
        username = request.POST["username"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("add_teacher")

        user = User.objects.create_user(
            username=username,
            password=request.POST["password"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
        )

        Teacher.objects.create(
            user=user,
            employee_id=request.POST["employee_id"],
            department_id=request.POST["department"],
            phone=request.POST["phone"],
        )

        messages.success(request, "Teacher Added Successfully.")
        return redirect("teacher_list")

    return render(
        request,
        "teacher/teacher_add.html",
        {"departments": departments},
    )


# ===========================
# Edit Teacher (Admin)
# ===========================

@login_required
@admin_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    departments = Department.objects.all()

    if request.method == "POST":
        teacher.user.first_name = request.POST["first_name"]
        teacher.user.last_name = request.POST["last_name"]
        teacher.user.email = request.POST["email"]
        teacher.user.save()

        teacher.employee_id = request.POST["employee_id"]
        teacher.department_id = request.POST["department"]
        teacher.phone = request.POST["phone"]
        teacher.save()

        messages.success(request, "Teacher Updated Successfully.")
        return redirect("teacher_list")

    return render(
        request,
        "teacher/teacher_edit.html",
        {"teacher": teacher, "departments": departments},
    )


# ===========================
# Delete Teacher
# ===========================

@login_required
@admin_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.user.delete()
    messages.success(request, "Teacher Deleted Successfully.")
    return redirect("teacher_list")


# ===========================
# Live Attendance
# ===========================

@login_required
@teacher_required
def live_attendance(request):
    attendance_records = Attendance.objects.select_related(
        "student",
        "attendance_session",
        "attendance_session__subject",
    ).order_by("-scan_time")

    return render(
        request,
        "teacher/live_attendance.html",
        {"attendance_records": attendance_records},
    )