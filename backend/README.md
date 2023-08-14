# Backend part

## Decsription
Django project with basic CRUD functionality.

**Features**:
- Custom user model
- Password hashing with Argon2
- Swagger documentation
- OTP codes with Celery and RabbitMQ
- PostgreSQL database
- Custom permission

## Usage
1. Create virtual environment.
2. Install packages with `pip`.
3. Configure settings.py.
4. Create `.env` file according example.
5. Run Celery.
6. Run django server.

## Endpoints
**Documentation:**
- `swagger/` - swagger UI.

---

**JWT authentication + OTP code:**
- `api/v1/login/` - login in.
- `api/v1/validate/` - OTP code validation.
- `api/v1/token/refresh/` - refresh jwt tokens.
- `api/v1/token/verify/` - verify jwt token.

---

**CRUD operations:**
- `api/v1/user/create/` - creating.
- `api/v1/user/<int:pk>` - reading.
- `api/v1/user/update/<int:pk>` - updating.
- `api/v1/user/delete/<int:pk` - deleting.
