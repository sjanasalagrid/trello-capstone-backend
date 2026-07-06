# Trello Capstone Backend

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Tests](https://img.shields.io/badge/Tests-68%20Passing-success)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

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

## Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy ORM
- PostgreSQL 17
- Alembic
- Pydantic v2
- JWT Authentication
- Pytest
- Docker
- Docker Compose
- Nginx

---

## Project Structure

```text
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

Dockerfile
docker-compose.yml
nginx.conf
Makefile

.env.example
.env.production.example

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

## Running with Docker

Build and start all services

```bash
docker compose up --build
```

Run in detached mode

```bash
docker compose up -d
```

Stop all containers

```bash
docker compose down
```

The application will be available through Nginx at:

```
http://localhost
```

Swagger UI

```
http://localhost/docs
```

The Docker Compose stack includes:

- FastAPI (Uvicorn)
- PostgreSQL 17
- Nginx Reverse Proxy

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

## Running Locally

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

## Testing Summary

### Integration Tests

- Authentication
- Boards
- Board Members
- Invitations
- Sections
- Tickets

**43 Integration Tests**

### Unit Tests

- AuthService
- BoardService
- InvitationService
- SectionService
- TicketService

**25 Unit Tests**

### Overall

- ✅ 68 Automated Tests
- ✅ All Tests Passing

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

## Architecture

```text
                Browser
                    │
                    ▼
              Nginx (Port 80)
                    │
                    ▼
          FastAPI + Uvicorn
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
             PostgreSQL 17
```

---

## Project Highlights

- Layered Architecture
- Repository Pattern
- Service Layer
- JWT Authentication
- Role-Based Authorization
- RESTful API Design
- PostgreSQL
- Alembic Database Migrations
- Dockerized Application
- Docker Compose Orchestration
- Nginx Reverse Proxy
- Unit Testing
- Integration Testing
- 68 Automated Tests

---

## Future Improvements

- Comments on Tickets
- File Attachments
- Activity Logs
- Email Notifications
- CI/CD Pipeline
- AWS Deployment
- Kubernetes Support
- Redis Caching

---

## Docker Architecture

```text
                Browser
                    │
             localhost:80
                    │
                    ▼
               Nginx Container
                    │
                    ▼
         FastAPI/Uvicorn Container
                    │
                    ▼
          PostgreSQL Container
```

---

# License

This project was developed as a capstone project for educational purposes.
