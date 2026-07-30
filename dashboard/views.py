from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
import json
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.shortcuts import render
from students.models import Student
from teachers.models import Teacher
from attendance.models import Attendance
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from accounts.decorators import admin_required
from students.models import Student
from teachers.models import Teacher
from attendance.models import Subject, Attendance
from django.contrib import messages
from django.http import HttpResponse
@login_required
@admin_required
def admin_dashboard(request):

    # Dashboard Statistics
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_subjects = Subject.objects.count()

    attendance_today = Attendance.objects.filter(
        scan_time__date=timezone.now().date()
    ).count()

    total_attendance = Attendance.objects.count()

    # Recent Attendance
    recent_attendance = (
        Attendance.objects.select_related(
            "student",
            "student__user",
            "student__department",
            "attendance_session",
            "attendance_session__subject",
        )
        .order_by("-scan_time")[:5]
    )

    # Attendance count by subject (for Chart.js)
    chart_data = (
        Attendance.objects.values(
            "attendance_session__subject__subject_name"
        )
        .annotate(total=Count("id"))
        .order_by("attendance_session__subject__subject_name")
    )

    labels = [
        item["attendance_session__subject__subject_name"]
        for item in chart_data
    ]

    values = [
        item["total"]
        for item in chart_data
    ]

    context = {
        "students": total_students,
        "teachers": total_teachers,
        "subjects": total_subjects,
        "attendance_today": attendance_today,
        "attendance_count": total_attendance,
        "recent_attendance": recent_attendance,
        "labels": json.dumps(labels),
        "values": json.dumps(values),
    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context,
    )
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
@login_required
@admin_required
def admin_profile(request):

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("admin_profile")

    context = {
        "total_students": Student.objects.count(),
        "total_teachers": Teacher.objects.count(),
        "total_attendance": Attendance.objects.count(),
    }

    return render(request, "admin_panel/profile.html", context)
@login_required
@admin_required
def admin_profile(request):

    print("METHOD:", request.method)

    if request.method == "POST":
        print("POST RECEIVED")
        print(request.POST)

        return HttpResponse("POST WORKING")

    context = {
        "total_students": Student.objects.count(),
        "total_teachers": Teacher.objects.count(),
        "total_attendance": Attendance.objects.count(),
    }

    return render(request, "admin_panel/profile.html", context)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
@admin_required
def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully.")

            return redirect("admin_profile")

    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "admin_panel/change_password.html",
        {"form": form}
    )
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
@admin_required
def edit_profile(request):

    if request.method == "POST":

        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")

        request.user.save()

        messages.success(request, "Profile updated successfully.")

        return redirect("admin_profile")

    return render(request, "admin_panel/edit_profile.html")
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
@admin_required
def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password changed successfully.")
            return redirect("admin_profile")

    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "admin_panel/change_password.html",
        {"form": form},
    )