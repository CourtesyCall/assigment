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

# Validation and Rules
- All inputs are validated to remove trailing whitespace.
- Posts and comments are limited to 1000 characters.
- Only authors of a post (and admin) can modify or delete it.

# Technologies Used
- Programming Language: Python (with FastAPI).
- Database: SQL (PostgreSQL preferred for relational structure).
- ORM: SQLAlchemy.
- Migration Tool: Alembic.
- Authentication: Basic Auth and JWT.
- Containerization: Docker Compose.


