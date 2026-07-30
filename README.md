# 📱 QR-Based Attendance Portal

## 📌 Project Overview

The **QR-Based Attendance Portal** is a web-based application developed using **Django** that simplifies and secures classroom attendance. Teachers generate a unique QR code for each class session, and students scan the QR code to mark their attendance. The system automatically records attendance while preventing duplicate entries and expired QR usage.

---

# 🚀 Features

## 👨‍🏫 Teacher Module

- **Teacher Registration & Login**
- **Dashboard with Attendance Statistics**
- **Generate Secure QR Codes**
- **QR Code Auto Expiry**
- **Manage Subjects**
- **View Student Attendance**
- **Export Attendance Reports (PDF & Excel)**
- **Search & Filter Attendance Records**
- **Profile Management**
- **Change Password**

## 👨‍🎓 Student Module

- **Student Registration & Login**
- **Personal Dashboard**
- **Scan Attendance QR**
- **View Attendance History**
- **Attendance Percentage**
- **Attendance Calendar**
- **Profile Management**
- **Change Password**

## 👨‍💼 Admin Module

- **Manage Students**
- **Manage Teachers**
- **Manage Departments**
- **Manage Subjects**
- **Monitor Attendance Records**
- **Dashboard Analytics**
- **User Management**

---

# 🔐 Security Features

- **Secure Authentication**
- **Password Hashing**
- **CSRF Protection**
- **Session Management**
- **QR Code Expiry**
- **One-Time QR Scan**
- **Duplicate Attendance Prevention**
- **Role-Based Access Control**

---

# 🛠️ Technology Stack

## Frontend

- **HTML5**
- **CSS3**
- **Bootstrap 5**
- **JavaScript**

## Backend

- **Python**
- **Django**

## Database

- **SQLite (Development)**

## Libraries

- **qrcode**
- **Pillow**
- **openpyxl**
- **reportlab**

---

# 📂 Project Structure

```text
SSQAMS/
│
├── accounts/
├── students/
├── teachers/
├── attendance/
├── templates/
├── static/
├── media/
├── config/
├── manage.py
└── requirements.txt
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/SSQAMS.git
```

## 2️⃣ Navigate to the Project

```bash
cd SSQAMS
```

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 5️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

## 6️⃣ Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7️⃣ Start the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

# 📊 Workflow

1. **Teacher logs in.**
2. **Teacher creates an attendance session.**
3. **System generates a secure QR code.**
4. **Student logs in.**
5. **Student scans the QR code.**
6. **System validates:**
   - QR Expiry
   - Student Authentication
   - Duplicate Attendance
7. **Attendance is stored in the database.**
8. **Teacher views reports and analytics.**

---

# 📁 Modules

- **Authentication**
- **Student Management**
- **Teacher Management**
- **Attendance Management**
- **QR Code Generation**
- **Dashboard**
- **Reports**
- **Notifications**
- **Profile Management**

---

# 🎯 Future Enhancements

- **Face Recognition Attendance**
- **AI-Based Attendance Analytics**
- **Email Notifications**
- **Mobile Application**
- **GPS-Based Attendance**
- **Cloud Database Integration**
- **AI Attendance Prediction**
- **SMS Alerts**

---

# 👨‍💻 Developed By

## **Kamaleeswari V**
