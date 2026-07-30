from django.urls import path
from .views import (
    teacher_dashboard,
    teacher_list,
    add_teacher,
    edit_teacher,
    delete_teacher,
    live_attendance,
    teacher_profile,
    edit_teacher_profile,
    teacher_change_password,
)

urlpatterns = [
    # Dashboard
    path(
        "dashboard/",
        teacher_dashboard,
        name="teacher_dashboard",
    ),

    # Teacher Management
    path(
        "",
        teacher_list,
        name="teacher_list",
    ),

    path(
        "add/",
        add_teacher,
        name="add_teacher",
    ),

    path(
        "edit/<int:teacher_id>/",
        edit_teacher,
        name="edit_teacher",
    ),

    path(
        "delete/<int:teacher_id>/",
        delete_teacher,
        name="delete_teacher",
    ),

    # Live Attendance
    path(
        "live-attendance/",
        live_attendance,
        name="live_attendance",
    ),

    # Teacher Profile
    path(
        "profile/",
        teacher_profile,
        name="teacher_profile",
    ),
    path(
        "profile/edit/",
        edit_teacher_profile,
        name="edit_teacher_profile",
    ),
    path(
        "profile/change-password/",
        teacher_change_password,
        name="teacher_change_password",
    ),
]