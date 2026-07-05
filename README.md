# Trello Capstone Backend

A RESTful backend API inspired by Trello, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. The project provides secure authentication, collaborative boards, invitations, sections, ticket management, and comprehensive automated testing.

---

## Features

### Authentication

* User registration
* User login with JWT authentication
* Password hashing
* Protected endpoints

### Boards

* Create boards
* View owned and joined boards
* Retrieve board details
* Owner-based authorization

### Board Members

* Invite members
* Accept invitations
* View board members
* Remove members
* Role-based access control (Owner / Member)

### Invitations

* Send invitations
* View pending invitations
* View sent invitations
* Accept invitations
* Revoke invitations

### Sections

* Create sections
* Update sections
* Delete empty sections
* Retrieve board sections
* Ordered section positioning

### Tickets

* Create tickets
* Update tickets
* Assign tickets
* Move tickets between sections
* Update ticket status
* Close tickets

---

# Tech Stack

* Python 3.14
* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic
* Pydantic v2
* JWT Authentication
* Pytest

---

# Project Structure

```
app/
├── api/
├── core/
├── db/
├── enums/
├── models/
├── repositories/
├── schemas/
├── services/
├── main.py

alembic/

tests/
├── integration/
├── unit/

.env
.env.example
requirements.txt
README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/sjanasalagrid/trello-capstone-backend.git
```

Move into the project

```bash
cd trello-capstone-backend
```

Create a virtual environment

macOS/Linux

```bash
python3 -m venv .venv
```

Windows

```bash
python -m venv .venv
```

Activate the environment

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/trello_db

TEST_DATABASE_URL=postgresql://username:password@localhost:5432/capstone_test

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Database Setup

Create the development database

```
trello_db
```

Create the testing database

```
capstone_test
```

Run migrations

```bash
alembic upgrade head
```

Check current migration

```bash
alembic current
```

---

# Running the Application

Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Running Tests

Run all tests

```bash
pytest
```

Verbose output

```bash
pytest -v
```

Run integration tests

```bash
pytest tests/integration
```

Run unit tests

```bash
pytest tests/unit
```

Run a single test file

```bash
pytest tests/integration/test_boards.py -v
```

Generate coverage report

```bash
pytest --cov=app --cov-report=term-missing
```

---

# Testing Summary

### Integration Tests

* Authentication
* Boards
* Board Members
* Invitations
* Sections
* Tickets

**45 Integration Tests**

### Unit Tests

* AuthService
* BoardService
* InvitationService
* SectionService
* TicketService

**23 Unit Tests**

### Overall

* **68 Automated Tests**
* **All tests passing**

---

# Authentication

All protected endpoints require a JWT access token.

Example header

```
Authorization: Bearer <access_token>
```

---

# Database Migrations

Create a migration

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations

```bash
alembic upgrade head
```

Rollback one migration

```bash
alembic downgrade -1
```

---

# API Architecture

```
Client
   │
   ▼
FastAPI Router
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
SQLAlchemy ORM
   │
   ▼
PostgreSQL
```

---

# Project Highlights

* Layered architecture
* Repository pattern
* Service layer for business logic
* JWT authentication
* Role-based authorization
* RESTful API design
* Alembic migrations
* PostgreSQL
* Comprehensive unit testing
* Comprehensive integration testing

---

# Future Improvements

* Comments on tickets
* Audit logs
* File attachments
* Notifications
* Docker support
* CI/CD pipeline
* Deployment to a cloud platform

---

# License

This project was developed as a capstone project for educational purposes.
