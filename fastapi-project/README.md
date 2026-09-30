## User relationships

The ORM models demonstrate several relationship patterns:

- A user has at most one profile. `UserProfile.user_id` is unique, and `User.profile` is scalar.
- A department has many users. `User.department_id` is nullable, and `Department.users` is a collection.
- A user can have many skills, and a skill can belong to many users. This is implemented through the `user_skills` association table.

Example:

```python
department = Department(name="Engineering")
user = User(name="Alex", email="alex@example.com", department=department)
skill = Skill(name="FastAPI")
user.skills.append(skill)
user.user_skills[0].level = "advanced"
user.profile = UserProfile(bio="Backend developer")
```

The relationship migration follows the existing user-table revisions. Apply it with `uv run alembic upgrade head`.

### API

Open `/docs` to try these endpoints:

- `POST /users` registers a user with `name`, `email`, and a password of at least 8 characters.
- `POST /auth/token` accepts OAuth2 form fields (`username` is the email) and returns a bearer token.
- `GET /auth/me` returns the authenticated user.
- Include `Authorization: Bearer <token>` for user management, relationships, and skills endpoints.
- `POST /departments` creates a department.
- `POST /departments/{department_id}/users` creates a user in that department.
- `GET /departments/{department_id}` returns the department and its users.
- `POST /users/{user_id}/profile` creates the user's profile.
- `GET /users/{user_id}/profile` returns that profile.
- `POST /skills` creates a skill.
- `GET /skills` lists all skills.
- `POST /users/{user_id}/skills` assigns a skill to a user.
- `GET /users/{user_id}/skills` returns the user's skills.

Example request bodies:

```json
{"name": "Engineering"}
```

```json
{"name": "Alex", "email": "alex@example.com", "password": "a-long-password"}
```

```json
{"bio": "Backend developer"}
```

```json
{"name": "FastAPI"}
```

```json
{"skill_id": 1, "level": "advanced"}
```

Set `JWT_SECRET_KEY` to a strong random value before deployment. Existing user records have no password hash and must be re-registered or otherwise assigned credentials before they can log in.
