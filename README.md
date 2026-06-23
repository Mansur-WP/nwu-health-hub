# 🏥 NWU HealthHub: A Smart Healthcare Management System

## Description

**NWU HealthHub** is a smart healthcare management system developed using Django. It is designed to digitize and streamline hospital operations by providing role-based access for administrators, doctors, patients, and pharmacists.

The system automates essential healthcare processes such as appointment scheduling, patient management, prescription handling, payment tracking, and administrative operations, improving efficiency and enhancing healthcare service delivery.

---

## Features

### 🔐 Authentication & Authorization

* User Registration and Login
* Role-Based Access Control
* Secure Authentication
* Session Management

### 👤 Patient Module

* View and Update Profile
* Book Appointments
* Cancel Appointments
* View Payment History
* View Prescriptions

### 🩺 Doctor Module

* View Patient Appointments
* Approve or Cancel Appointments
* Access Patient History
* Generate Prescriptions
* Send Prescriptions to Pharmacy

### 💊 Pharmacist Module

* View Prescription Queue
* Dispense Medications
* Manage Medicine Inventory
* Monitor Low Stock Levels

### 🛡️ Admin Dashboard

* Manage Staff
* Manage Doctors
* Verify Payments
* Monitor System Statistics
* View Recent Activities

### 💳 Payment Management

* Payment Processing
* Payment Verification
* Invoice and Receipt Generation

---

## Technologies Used

* Python
* Django 5.2
* SQLite
* Bootstrap 5
* HTML5
* CSS3
* JavaScript
* Chart.js

---

## Screenshots

### Homepage

`docs/screenshots/homepage.png`

### Patient Dashboard

`docs/screenshots/patient-dashboard.png`

### Doctor Dashboard

`docs/screenshots/doctor-dashboard.png`

### Pharmacist Dashboard

`docs/screenshots/pharmacist-dashboard.png`

### Admin Dashboard

`docs/screenshots/admin-dashboard.png`

---

## Project Structure

```text
accounts/         # Authentication and custom user model
patients/         # Patient module
doctors/          # Doctor module
pharmacists/      # Pharmacist module
appointments/     # Appointment scheduling
payments/         # Payment processing and receipts
prescriptions/    # Prescription management
dashboard/        # Administrative dashboard
home/             # Public pages
templates/        # HTML templates
static/           # CSS, JavaScript, and images
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/nwu-healthhub.git
cd nwu-healthhub
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file and add:

```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

---

## User Roles

| Role       | Responsibilities                                       |
| ---------- | ------------------------------------------------------ |
| Admin      | Manage users, doctors, payments, and system statistics |
| Doctor     | Approve appointments and generate prescriptions        |
| Patient    | Book appointments and manage personal records          |
| Pharmacist | Dispense medications and manage inventory              |

---

## Future Improvements

* Email Notifications
* SMS Appointment Reminders
* Medical History Module
* Audit Logging
* REST API Integration
* PostgreSQL Support
* Docker Deployment
* Automated Testing
* AI-Based Healthcare Assistant

---

## License

This project is released under the **MIT License**.

---

## Author

**Mansur Nasir**

Software Engineer | AI Enthusiast | Django Developer

Northwest University, Kano

---

### Academic Project

Developed as part of the **CYB 210: System Analysis and Design** course.
