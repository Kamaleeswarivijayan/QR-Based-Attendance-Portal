from django.urls import path
import students.views as views
from .views import (
    student_list,
    add_student,
    edit_student,
    delete_student,
    student_dashboard,
    student_profile,
)

urlpatterns = [
    path("", student_list, name="student_list"),
    path("add/", add_student, name="add_student"),
    path("edit/<int:student_id>/", edit_student, name="edit_student"),
    path("delete/<int:student_id>/", delete_student, name="delete_student"),
    path("dashboard/", student_dashboard, name="student_dashboard"),

    path("profile/", views.student_profile, name="student_profile"),
    path("profile/edit/", views.edit_student_profile, name="edit_student_profile"),
    path("profile/change-password/", views.student_change_password, name="student_change_password"),
]