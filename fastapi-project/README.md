## User relationships

The ORM models demonstrate two relationships:

- A user has at most one profile. `UserProfile.user_id` is unique, and `User.profile` is scalar.
- A department has many users. `User.department_id` is nullable, and `Department.users` is a collection.

Example:

```python
department = Department(name="Engineering")
user = User(name="Alex", email="alex@example.com", department=department)
user.profile = UserProfile(bio="Backend developer")
```

The relationship migration follows the existing user-table revisions. Apply it with `uv run alembic upgrade head`.

### API

Open `/docs` to try these endpoints:

- `POST /departments` creates a department.
- `POST /departments/{department_id}/users` creates a user in that department.
- `GET /departments/{department_id}` returns the department and its users.
- `POST /users/{user_id}/profile` creates the user's profile.
- `GET /users/{user_id}/profile` returns that profile.

Example request bodies:

```json
{"name": "Engineering"}
```

```json
{"name": "Alex", "email": "alex@example.com"}
```

```json
{"bio": "Backend developer"}
```
