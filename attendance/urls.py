from django.urls import path
from .views import *

urlpatterns = [
    path("subjects/", subject_list, name="subject_list"),
    path("subjects/add/", add_subject, name="add_subject"),
    path("subjects/edit/<int:subject_id>/", edit_subject, name="edit_subject"),
    path("subjects/delete/<int:subject_id>/", delete_subject, name="delete_subject"),

    path("generate-qr/", generate_qr, name="generate_qr"),

    
    path("scan/<str:token>/", scan_qr, name="scan_qr"),

    path("list/", attendance_list, name="attendance_list"),
    path("history/", attendance_history, name="attendance_history"),
    path("reports/", reports, name="reports"),

    path("export/excel/", export_excel, name="export_excel"),
    path("export/pdf/", export_pdf, name="export_pdf"),
    path("percentage/", attendance_percentage, name="attendance_percentage"),
    path("test-email/", test_email, name="test_email"),
    path(
    "close-session/<int:session_id>/",
    close_session,
    name="close_session",
    ),
    path(
    "calendar/",
    attendance_calendar,
    name="attendance_calendar",
    ),
    path(
    "calendar-events/",
    calendar_events,
    name="calendar_events",
    ),
    
    
]