
# User Authentication Service

This project involves implementing a simple user authentication system. It uses SQLAlchemy ORM for database management and includes functions for creating users, handling passwords, and implementing session-based authentication with tokens.

## Table of Contents
1. [Database Setup](#database-setup)
2. [Creating a User](#creating-a-user)
3. [Finding a User](#finding-a-user)
4. [Updating Passwords](#updating-passwords)
5. [Reset Tokens](#reset-tokens)
6. [API Endpoints](#api-endpoints)
7. [Repository Structure](#repository-structure)

---

## Database Setup

The `DB` class manages the database using SQLAlchemy. It handles creating and dropping tables, managing sessions, and interacting with the database.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class DB:
    def __init__(self):
        self._engine = create_engine("sqlite:///my_database.db")
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
```

> **Note:** The `_session` property is private and should **not** be accessed from outside the `DB` class.

---

## Creating a User

Implement the `add_user` method which takes two arguments:
- `email` (string)
- `hashed_password` (string)

The method should return a `User` object and save the user in the database.

Example:

```python
from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)
```

Output:
```
1
```

---

## Finding a User

The `find_user_by` method retrieves the first user that matches the given criteria. This method accepts keyword arguments (e.g., `email='example@example.com'`).

```python
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

try:
    user = my_db.find_user_by(email="test@test.com")
    print(user.id)
except NoResultFound:
    print("No user found")
except InvalidRequestError:
    print("Invalid request")
```

---

## Updating Passwords

The `update_password` method updates the password of a user given their `reset_token` and the new password. It hashes the new password and sets the `reset_token` to `None` after the update.

```python
def update_password(self, reset_token: str, new_password: str):
    user = self.find_user_by(reset_token=reset_token)
    if not user:
        raise ValueError("Invalid reset token")
    user.hashed_password = hash_password(new_password)
    user.reset_token = None
    self._session.commit()
```

---

## Reset Tokens

A reset token is a unique identifier generated for password recovery. The `get_reset_password_token` method generates this token and updates the user's `reset_token` field.

```python
def get_reset_password_token(self, email: str) -> str:
    user = self.find_user_by(email=email)
    if not user:
        raise ValueError("User not found")
    
    reset_token = str(uuid.uuid4())
    user.reset_token = reset_token
    self._session.commit()
    return reset_token
```

---

## API Endpoints

The API includes endpoints for user authentication, password recovery, and token management.

- **POST /reset_password**: Expects `email` in form data and responds with a reset token if the user exists.
- **PUT /reset_password**: Expects `email`, `reset_token`, and `new_password` in form data to update the user's password.

---

## Repository Structure

```
alx-backend-user-data/
│
├── db.py          # Contains the database and session handling
├── user.py        # Contains the User model definition
├── auth.py        # Handles authentication logic
├── app.py         # API routes for user management and authentication
├── main.py        # Main script to interact with the database
└── README.md      # Project documentation
```

---

## License

This project is part of the ALX Backend User Data module.

