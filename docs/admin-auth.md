# Admin Authentication API

This document describes the authentication API endpoints for admin users.

## Admin Login

Admin users can log in using their username and password. Admin users must be created using either the Django admin interface or the `create_admin_user` management command.

### Creating an Admin User

To create an admin user from the command line, use:

```bash
python manage.py create_admin_user --username admin --password secure_password --email admin@example.com --first-name Admin --last-name User
```

### Endpoint: `/api/v1/auth/login/`

**Method**: POST

**Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
  "username": "admin",
  "password": "secure_password"
}
```

**Success Response**: 
- Status: 200 OK
```json
{
  "refresh": "<JWT refresh token>",
  "access": "<JWT access token>",
  "exp": "<access token expiration timestamp>"
}
```

**Error Response**:
- Status: 400 Bad Request
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```

or

```json
{
  "non_field_errors": ["User is not authorized to use this endpoint."]
}
```

### Using JWT Tokens

After successful authentication, use the provided access token in the Authorization header for subsequent requests:

```
Authorization: Bearer <access token>
```

When the access token expires, use the refresh token to obtain a new access token:

```
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh token>"
}
```
