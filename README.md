# Kanban Backend API

This project is a **RESTful backend API for a Kanban board application** built with **Django** and **Django Rest Framework**.

The API provides functionality for managing boards, tasks, and comments, including authentication and permission handling.

This project was created to **practice and understand backend architecture with Django Rest Framework**.

---

# Features

* User registration and authentication (Token Authentication)
* Create and manage Kanban boards
* Assign board members
* Create and manage tasks
* Task assignment and review workflow
* Comment system for tasks
* Role-based permissions
* Task statistics and aggregated board information

---

# Technologies

* Python
* Django
* Django Rest Framework
* Token Authentication
* SQLite (default Django database)

---

# Permissions

The API includes several custom permission classes:

* **Board Member**
  Only members of a board can access its tasks and comments.

* **Board Owner**
  Only the board owner can delete a board.

* **Task Creator / Board Owner**
  Only the task creator or board owner can delete a task.

* **Comment Creator / Board Owner**
  Only the comment creator or board owner can delete a comment.

---

# Installation

Clone the repository:

```
git clone <repository-url>
cd backend
```

Create a virtual environment:

```
python -m venv venv
```

Activate the environment:

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Start the development server:

```
python manage.py runserver
```

---

# Purpose of this Project

This project was built to practice:

* Django Rest Framework
* REST API design
* authentication and permissions
* serializer validation
* query optimization with `select_related` and `annotate`

---

# License

This project is intended for **educational purposes**.
