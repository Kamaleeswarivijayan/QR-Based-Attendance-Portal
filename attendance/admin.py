from django.contrib import admin
from .models import Subject, AttendanceSession, Attendance

admin.site.register(Subject)
admin.site.register(AttendanceSession)
admin.site.register(Attendance)