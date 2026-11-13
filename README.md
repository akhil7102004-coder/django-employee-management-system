# Django Employee Management System

A web-based Employee Management System developed using **Python, Django, MySQL, HTML, CSS, and Bootstrap**. The application provides a centralized interface to manage employee records with complete CRUD (Create, Read, Update, Delete) functionality.

## 📌 Project Overview

The Django Employee Management System is designed to simplify employee record management through a user-friendly web interface.

It allows users to add new employees, view employee information, update existing records, and delete employee details. The application uses MySQL as its relational database to store and manage employee information.

## ✨ Features

- **Dashboard:** Centralized interface for employee management.
- **Add Employees:** Register new employees with their details.
- **View Employees:** Display employee records in a structured table.
- **Update Employees:** Edit existing employee information.
- **Delete Employees:** Remove employee records.
- **MySQL Integration:** Store and manage employee data using MySQL.
- **Responsive UI:** Bootstrap-based interface.
- **Django Admin:** Manage database records through Django's built-in administration panel.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web application framework |
| MySQL | Relational database |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Frontend interactions |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
EmployeeManagement/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── employees/
│   ├── migrations/
│   ├── templates/
│   │   └── employees/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── employee_list.html
│   │       ├── employee_form.html
│   │       └── employee_confirm_delete.html
│   │
│   ├── static/
│   │   └── employees/
│   │       └── css/
│   │           └── style.css
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## 🗄️ Database Structure

**Database:** MySQL

**Database Name:** `employee_management`

### Employee Table

| Field | Data Type | Description |
|---|---|---|
| id | AutoField | Primary Key |
| name | CharField | Employee Name |
| email | EmailField | Employee Email |
| phone | CharField | Contact Number |
| department | CharField | Department |
| designation | CharField | Job Designation |
| salary | DecimalField | Employee Salary |
| joining_date | DateField | Date of Joining |

The database is managed using Django ORM.

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/akhil7102004-coder/django-employee-management-system.git
```

### 2. Navigate to the Project Directory

```bash
cd django-employee-management-system
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root directory using `.env.example` as a reference.

Configure the following variables:

```env
DJANGO_SECRET_KEY=your_django_secret_key
DJANGO_DEBUG=True

MYSQL_DATABASE=employee_management
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

Replace the values with your local configuration. Keep your actual `.env` file private.

### 7. Create the MySQL Database

Open MySQL Workbench or your MySQL client and execute:

```sql
CREATE DATABASE employee_management;
```

### 8. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Create a Superuser

```bash
python manage.py createsuperuser
```

### 10. Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

**Application:** http://127.0.0.1:8000/

**Employee Management:** http://127.0.0.1:8000/employees/

**Django Admin:** http://127.0.0.1:8000/admin/

## 📸 Screenshots

Add screenshots of your application here to demonstrate its interface and functionality.

### Dashboard
<!-- Add dashboard screenshot here -->

### Employee List
<!-- Add employee list screenshot here -->

### Add Employee
<!-- Add add employee screenshot here -->

### Edit Employee
<!-- Add edit employee screenshot here -->

## 🚀 Future Enhancements

- Employee search and filtering.
- Department-wise employee analytics.
- Pagination for employee records.
- User authentication and role-based access.
- Employee profile management.
- Dashboard charts and reports.
- Cloud deployment.

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Developing web applications using Django.
- Implementing CRUD operations.
- Connecting Django applications with MySQL.
- Working with Django Models, Views, Forms, and Templates.
- Managing relational databases using Django ORM.
- Building responsive interfaces using Bootstrap.
- Using Git and GitHub for version control.
- Managing application configuration using environment variables.

## 👨‍💻 Author

**Akhil A.**

B.Tech Computer Science and Engineering

GitHub: [@akhil7102004-coder](https://github.com/akhil7102004-coder)

---

⭐ If you find this project useful, consider giving it a star!
