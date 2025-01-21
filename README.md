## Dcoya Blog Backend Assignment
# Introduction
This project is a backend server for a blog platform that allows registered users to:

- Post blogs.
- Comment on other users' blogs.
- Like blogs and comments .
The server ensures proper user authentication and authorization, with input validation and database management for a seamless blogging experience.

## Features
# Core Features
1. # Blog Management:

- Registered users can post, edit, and delete their blog posts.
- Users can view all posted blogs.
2. # Comments and Likes:

- Users can like and remove their likes from blog posts.
- Comments can be added to blog posts by registered users.
3. # User Management:

- Basic user registration.
- Authentication using JWT.

# API Documentation Once running, visit:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

# Validation and Rules
- All inputs are validated to remove trailing whitespace.
- Posts and comments are limited to 1000 characters.
- Only authors of a post (and admin) can modify or delete it.

# Technologies Used
- Programming Language: Python (with FastAPI).
- Database: SQL (PostgreSQL preferred for relational structure).
- ORM: SQLAlchemy.
- Migration Tool: Alembic and Poetry.
- Authentication: Basic Auth and JWT.
- Containerization: Docker Compose.

## Why PostgreSQL?
- One of the main reasons is that Postgres is usually used in my workflow and I'm more used to working with it.
- The second reason is that it's famous in SQL databases.
- Third - control, scalability and ACID, as well as security, make it easier to work with data through ORM. The relational structure of PostgreSQL provides more guarantees of data integrity and flexibility with increasing application complexity.

# Secret files
- .env (APP_CONFIG__DB__URL=postgresql+asyncpg://name:password:5432/database-name)
- certs (jwt-private.pem and jwt-public.pem)


### Installation and Setup
# Prerequisites
Ensure the following are installed:

- Python 3.10 or later
- Docker and Docker Compose
- PostgreSQL

1. Clone the Repository
  ```bash
   git clone https://github.com/CourtesyCall/assigment.git
   cd repository
```
2. Create .env in app folder
```bash
  APP_CONFIG__DB__URL=postgresql+asyncpg://name:password:5432/database-name
```

3. create certs folder in the first folder 
In certs folder create 2 files (jwt-private.pem and jwt-public.pem) , there you can put you secret and private key

4. install all dependencies
   ```bash
poetry install
```
5. alembic database install
```bash
  alembic upgrade head
```
6. run localy using uvicorn
```bash
  uvicorn app.main:app --reload
```
7. Build and Run with Docker
```bash
  docker-compose up --build
```
