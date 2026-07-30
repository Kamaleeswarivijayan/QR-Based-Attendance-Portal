import io
import base64
import qrcode
from accounts.decorators import (
    admin_required,
    student_required,
    admin_or_teacher_required,
    admin_or_student_required,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Attendance, AttendanceSession, Subject
from .utils import generate_qr_token, get_expiry_time
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from students.models import Student, Department
from teachers.models import Teacher
from django.contrib.auth.decorators import login_required
from .models import Attendance
from students.models import Student
from django.contrib.auth.decorators import login_required
from teachers.models import Teacher
from .models import Attendance
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

@login_required
@admin_or_teacher_required
def export_excel(request):

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Attendance Report"

    worksheet.append([
        "Student",
        "Register Number",
        "Subject",
        "Scan Time",
        "Status"
    ])

    attendance_records = Attendance.objects.select_related(
        "student",
        "attendance_session",
        "attendance_session__subject"
    )

    for attendance in attendance_records:
        worksheet.append([
            f"{attendance.student.user.first_name} {attendance.student.user.last_name}",
            attendance.student.register_number,
            attendance.attendance_session.subject.subject_name,
            attendance.scan_time.strftime("%d-%m-%Y %H:%M"),
            attendance.status,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Attendance_Report.xlsx"'
    )

    workbook.save(response)

    return response

@login_required
@admin_or_teacher_required
def attendance_list(request):

    attendance_records = Attendance.objects.select_related(
        "student",
        "attendance_session",
        "attendance_session__subject"
    ).order_by("-scan_time")

    # Search
    search = request.GET.get("q")
    if search:
        attendance_records = attendance_records.filter(
            Q(student__user__first_name__icontains=search) |
            Q(student__user__last_name__icontains=search) |
            Q(student__register_number__icontains=search)
        )

    # Subject Filter
    subject = request.GET.get("subject")
    if subject:
        attendance_records = attendance_records.filter(
            attendance_session__subject_id=subject
        )

    # Dashboard Counts
    total_records = attendance_records.count()
    present_count = attendance_records.filter(status="Present").count()
    late_count = attendance_records.filter(status="Late").count()
    absent_count = attendance_records.filter(status="Absent").count()

    subjects = Subject.objects.all()

    return render(
        request,
        "attendance/attendance_list.html",
        {
            "attendance_records": attendance_records,
            "subjects": subjects,
            "query": search,
            "selected_subject": subject,
            "total_records": total_records,
            "present_count": present_count,
            "late_count": late_count,
            "absent_count": absent_count,
        },
    )
@login_required
@student_required
def attendance_history(request):
    student = Student.objects.get(user=request.user)

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by('-scan_time')

    return render(
        request,
        "attendance/attendance_history.html",
        {
            "attendance_records": attendance_records
        }
    )

# ===========================
# QR Attendance
# ===========================

# ===========================
# QR Attendance
# ===========================

@login_required
@student_required
def scan_qr(request, token):

    # Get attendance session
    session = get_object_or_404(
        AttendanceSession,
        qr_token=token
    )

    # Check QR expiry
    if timezone.now() > session.expires_at:
        messages.error(request, "QR Code Expired.")
        return redirect("login")

    # Check logged in user is a student
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Only students can mark attendance.")
        return redirect("login")

    # Prevent duplicate attendance
    if Attendance.objects.filter(
        student=student,
        attendance_session=session
    ).exists():
        messages.warning(request, "Attendance already marked.")
        return redirect("student_dashboard")

    # Save attendance
    attendance = Attendance.objects.create(
        student=student,
        attendance_session=session,
        status="Present"
    )
# Calculate attendance percentage
    subject = session.subject

    total = Attendance.objects.filter(
        student=student,
        attendance_session__subject=subject
    ).count()

    present = Attendance.objects.filter(
        student=student,
        attendance_session__subject=subject,
        status="Present"
    ).count()

    percentage = (present / total) * 100 if total > 0 else 0

    # Send warning email if attendance is below 75%
    if percentage < 75:
        send_low_attendance_email(student, subject, round(percentage, 2))
    # Send email
    try:
        send_mail(
            subject="Attendance Marked Successfully",
            message=f"""
Hello {student.user.first_name},

Your attendance has been marked successfully.

---------------------------------------
Student Name : {student.user.get_full_name()}
Register No  : {student.register_number}
Subject      : {session.subject.subject_name}
Teacher      : {session.teacher.user.get_full_name()}
Status       : Present
Date & Time  : {attendance.scan_time.strftime('%d-%m-%Y %I:%M %p')}
---------------------------------------

Thank you.

QR Attendance Management System
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print("Email Error:", e)

    messages.success(request, "Attendance marked successfully!")

    return render(
        request,
        "attendance/attendance_success.html",
        {
            "student": student,
            "subject": session.subject,
        }
    )

@login_required
@admin_or_teacher_required
def close_session(request, session_id):

    session = get_object_or_404(
        AttendanceSession,
        id=session_id
    )

    students = Student.objects.filter(
        department=session.subject.department
    )

    for student in students:

        if not Attendance.objects.filter(
            student=student,
            attendance_session=session
        ).exists():

            Attendance.objects.create(
                student=student,
                attendance_session=session,
                status="Absent"
            )

            # Email Absent Student
            send_mail(
                subject="Absent Notification",
                message=f"""
Dear {student.user.first_name},

You were marked ABSENT for

Subject : {session.subject.subject_name}

Date : {timezone.now().strftime('%d-%m-%Y')}

Please contact your faculty if this is incorrect.

QR Attendance Management System
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[student.user.email],
                fail_silently=True,
            )

    messages.success(request, "Attendance session closed successfully.")

    return redirect("attendance_list")



def send_low_attendance_email(student, subject, percentage):
    from django.core.mail import send_mail
    from django.conf import settings

    send_mail(
        subject="⚠ Low Attendance Warning",
        message=f"""
Dear {student.user.first_name},

Your attendance for the subject "{subject.subject_name}" has dropped to {percentage}%.

Minimum Required Attendance : 75%

Please attend upcoming classes regularly.

Thank you,
QR Attendance Management System
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[student.user.email],
        fail_silently=True,
    )
# ===========================
# Generate QR
# ===========================
@login_required
@admin_or_teacher_required
def generate_qr(request):

    subjects = Subject.objects.all()

    if request.method == "POST":

        subject = Subject.objects.get(
            id=request.POST["subject"]
        )

        token = generate_qr_token()

        session = AttendanceSession.objects.create(
            subject=subject,
            teacher=subject.teacher,
            qr_token=token,
            expires_at=get_expiry_time()
        )

        scan_url = request.build_absolute_uri(
            f"/attendance/scan/{token}/"
        )

        qr = qrcode.make(scan_url)

        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")

        qr_code = base64.b64encode(
            buffer.getvalue()
        ).decode()

        return render(
             request,
             "attendance/generate_qr.html",
             {
                "subjects": subjects,
                "qr_code": qr_code,
                "scan_url": scan_url,
                "session": session,
                "expires_at": session.expires_at,
                },
        )

    return render(
        request,
        "attendance/generate_qr.html",
        {
            "subjects": subjects,
        },
    )

# ===========================
# Subject CRUD
# ===========================

@login_required
@admin_required
def subject_list(request):

    query = request.GET.get("q")

    subjects = Subject.objects.select_related(
        "department",
        "teacher",
        "teacher__user"
    )

    if query:
        subjects = subjects.filter(
            Q(subject_code__icontains=query)
            | Q(subject_name__icontains=query)
            | Q(department__department_name__icontains=query)
            | Q(teacher__user__first_name__icontains=query)
        )

    return render(
        request,
        "subject/subject_list.html",
        {
            "subjects": subjects,
            "query": query,
        }
    )


@login_required
@admin_required
def add_subject(request):

    departments = Department.objects.all()
    teachers = Teacher.objects.select_related("user")

    if request.method == "POST":

        Subject.objects.create(
            subject_code=request.POST["subject_code"],
            subject_name=request.POST["subject_name"],
            semester=request.POST["semester"],
            department_id=request.POST["department"],
            teacher_id=request.POST["teacher"],
        )

        messages.success(request, "Subject added successfully.")

        return redirect("subject_list")

    return render(
        request,
        "subject/subject_add.html",
        {
            "departments": departments,
            "teachers": teachers,
        }
    )


@login_required
@admin_required
def edit_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    departments = Department.objects.all()
    teachers = Teacher.objects.select_related("user")

    if request.method == "POST":

        subject.subject_code = request.POST["subject_code"]
        subject.subject_name = request.POST["subject_name"]
        subject.semester = request.POST["semester"]
        subject.department_id = request.POST["department"]
        subject.teacher_id = request.POST["teacher"]

        subject.save()

        messages.success(request, "Subject updated successfully.")

        return redirect("subject_list")

    return render(
        request,
        "subject/subject_edit.html",
        {
            "subject": subject,
            "departments": departments,
            "teachers": teachers,
        }
    )

from attendance.models import Attendance
from .models import Subject

@login_required
@admin_or_teacher_required
def reports(request):

    attendance_records = Attendance.objects.select_related(
        "student",
        "attendance_session",
        "attendance_session__subject",
    ).order_by("-scan_time")

    # Search
    search = request.GET.get("search")
    if search:
        attendance_records = attendance_records.filter(
            student__user__first_name__icontains=search
        )

    # Subject Filter
    subject = request.GET.get("subject")
    if subject:
        attendance_records = attendance_records.filter(
            attendance_session__subject_id=subject
        )

    subjects = Subject.objects.all()

    return render(
        request,
        "attendance/reports.html",
        {
            "attendance_records": attendance_records,
            "subjects": subjects,
        },
    )
@login_required
@admin_required
def delete_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    subject.delete()

    messages.success(request, "Subject deleted successfully.")

    return redirect("subject_list")

from django.http import HttpResponse

@login_required
@admin_or_teacher_required
def export_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Attendance_Report.pdf"'

    doc = SimpleDocTemplate(response)

    elements = []

    styles = getSampleStyleSheet()

    elements.append(
        Paragraph("<b>Attendance Report</b>", styles["Heading1"])
    )

    data = [
        [
            "Student",
            "Register No",
            "Subject",
            "Status",
            "Time",
        ]
    ]

    attendance_records = Attendance.objects.select_related(
        "student",
        "attendance_session",
        "attendance_session__subject"
    )

    for attendance in attendance_records:

        data.append([
            f"{attendance.student.user.first_name} {attendance.student.user.last_name}",
            attendance.student.register_number,
            attendance.attendance_session.subject.subject_name,
            attendance.status,
            attendance.scan_time.strftime("%d-%m-%Y %H:%M"),
        ])

    table = Table(data)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("BACKGROUND", (0,1), (-1,-1), colors.beige),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("BOTTOMPADDING", (0,0), (-1,0), 10),
        ])
    )

    elements.append(table)

    doc.build(elements)

    return response

from django.db.models import Count, Q

@login_required
@admin_or_teacher_required
def attendance_percentage(request):

    students = Student.objects.all()
    subjects = Subject.objects.all()

    report = []

    above_75 = 0
    between_50_75 = 0
    below_50 = 0

    for student in students:

        for subject in subjects:

            total = Attendance.objects.filter(
                student=student,
                attendance_session__subject=subject
            ).count()

            present = Attendance.objects.filter(
                student=student,
                attendance_session__subject=subject,
                status="Present"
            ).count()

            percentage = 0

            if total > 0:
                percentage = round((present / total) * 100, 2)

            # Count categories
            if percentage >= 75:
                above_75 += 1
            elif percentage >= 50:
                between_50_75 += 1
            else:
                below_50 += 1

            report.append({
                "student": student,
                "subject": subject,
                "present": present,
                "total": total,
                "percentage": percentage,
            })


    return render(
        request,
        "attendance/attendance_percentage.html",
        {
            "report": report,
            "total_students": students.count(),
            "above_75": above_75,
            "between_50_75": between_50_75,
            "below_50": below_50,
        },
    )
from django.http import HttpResponse

def test_email(request):

    send_mail(
        subject="QR Attendance Portal",
        message="Congratulations! Your Django email configuration is working successfully.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["kamaleeswarivijayan@gmail.com"],  # Replace with your email
        fail_silently=False,
    )

    return HttpResponse("Email sent successfully!")
@login_required
@student_required
def attendance_calendar(request):
    return render(request, "attendance/calendar.html")


@login_required
@student_required
def calendar_events(request):

    student = Student.objects.get(user=request.user)

    attendance = Attendance.objects.filter(student=student)

    events = []

    for record in attendance:

        color = "#28a745"

        if record.status == "Absent":
            color = "#dc3545"

        events.append({
            "title": record.status,
            "start": record.scan_time.date().isoformat(),
            "color": color,
        })

    return JsonResponse(events, safe=False)