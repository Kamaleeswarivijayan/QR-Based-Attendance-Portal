from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),

    path("dashboard/", include("dashboard.urls")),
    path("students/", include("students.urls")),
    path("teachers/", include("teachers.urls")),
    path("attendance/", include("attendance.urls")),
]