# 🔐 FastAPI JWT Auth – Interview Crash README

A minimal, clean template for building **Authentication + Authorization** using FastAPI, JWT, and bcrypt.

---

# 🧠 1. Core Concepts (Don’t Mess This Up)

## Authentication = “Who are you?”

* User sends username + password
* Server verifies credentials
* Server returns a **JWT token**

## Authorization = “What are you allowed to access?”

* User sends JWT in request
* Server verifies token
* If valid → allow access to protected routes

---

# 🚂 2. Full Flow (End-to-End)

## Step 1: Login

```
POST /token
```

Input:

* username
* password

Output:

```
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## Step 2: Use Token

Every protected request must include:

```
Authorization: Bearer <token>
```

---

## Step 3: Access Protected Route

```
GET /users/me
```

Backend:

* Decode token
* Verify signature + expiry
* Extract user
* Return data

---

# 🧩 3. Important Components

## 1. Password Hashing

* Use **bcrypt**
* Never store plain passwords

## 2. JWT Token

* Contains:

  * `sub` → username
  * `exp` → expiry time

## 3. Dependency Injection (FastAPI Magic)

```
Depends(get_current_user)
```

* Automatically validates token
* Blocks unauthorized users

---

# 🔐 4. Key Rules (DO NOT BREAK THESE)

| Thing    | Why Important                    |
| -------- | -------------------------------- |
| `sub`    | Standard field for user identity |
| `exp`    | Token expiry (security)          |
| `Bearer` | Required auth header format      |
| `/token` | Login endpoint for OAuth2        |
| bcrypt   | Secure password hashing          |

---

# ⚔️ 5. How to Use This as a Template

## Scenario 1: Admin Panel

* Add role field in DB
* Check role inside dependency

## Scenario 2: Multi-user system

* Replace fake DB with real DB (Mongo/Postgres)

## Scenario 3: API Security Testing

* Try invalid token → should fail
* Try expired token → should fail
* Try tampered token → should fail

## Scenario 4: Add Features

* Refresh tokens
* Email verification
* Rate limiting

---

# 🧪 6. Testing Checklist (IMPORTANT)

* [ ] Login works
* [ ] Wrong password fails
* [ ] Token generated
* [ ] Protected route blocks without token
* [ ] Protected route works with valid token
* [ ] Expired token fails

---

# 🧠 7. Interview Answer (Memorize This)

> “I implemented JWT-based authentication where users log in to receive a signed token. Protected routes use dependency injection to validate tokens, ensuring only authenticated users can access resources. Passwords are securely stored using bcrypt.”

---

# 🧨 Final Note

This is not just a project.

This is:

> 🔥 Your entry point into backend + cybersecurity

If you understand this fully:

* You can build APIs
* You can secure APIs
* You can explain APIs

That’s enough to crack most intern interviews.
