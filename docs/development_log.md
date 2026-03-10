# 📘 Banking Core – Development Log

This document tracks the architectural evolution of the Banking Core system.

The project began as a simple banking script and evolved into a secure full-stack backend system.

---

# 🚀 Phase 1 — Basic Banking Logic

Initial goal was to simulate banking operations.

Features implemented:

- Create account
- Deposit
- Withdraw
- Check balance

Characteristics:

- No database
- Data stored in memory
- Basic class structure

Learning outcomes:

- Object oriented programming
- Basic validation
- Method interactions

---

# 💾 Phase 2 — SQLite Integration

To persist data, SQLite was introduced.

Changes:

- Created database schema
- Introduced accounts table
- Introduced transactions table
- Implemented commit and rollback

Benefits:

- Data persistence
- Transaction safety
- Real database structure

---

# 🏗 Phase 3 — Repository Pattern

Problem identified:

Business logic and SQL queries were mixed.

Solution:

Created `AccountRepository`.

Responsibilities:

- Handle SQL queries
- Manage database connection
- Return entity objects

Benefits:

- Separation of concerns
- Cleaner architecture
- Easier maintenance

---

# 🧠 Phase 4 — Service Layer

Introduced `BankingServices`.

Responsibilities:

- Business rules
- Validation
- Transaction control
- Raising domain exceptions

Important rule:

Service layer contains **no SQL code**.

---

# 📦 Phase 5 — Domain Entities

Added:

```
Account
Transaction
```

Before:

Repository returned tuples.

After:

Repository maps rows to objects.

Example improvement:

```
account.balance
```

instead of

```
account[3]
```

Benefits:

- Better readability
- Domain abstraction

---

# ⚠️ Phase 6 — Custom Exception Architecture

Introduced domain exception hierarchy.

Examples:

- BankingException
- AccountNotFoundException
- InvalidAmountException
- InsufficientBalanceException
- InvalidPINException

Benefits:

- Clear domain error semantics
- Better API responses
- Easier debugging

---

# 🌐 Phase 7 — REST API Implementation

Flask was introduced to expose backend functionality.

Endpoints added:

```
POST /accounts
GET /accounts/<account>
POST /deposit
POST /withdraw
GET /transactions
```

Benefits:

- External interface support
- JSON communication
- HTTP status codes

---

# 🔐 Phase 8 — Authentication System

Added secure authentication using JWT.

Two token types introduced:

Access Token

```
valid for 15 minutes
```

Refresh Token

```
valid for 7 days
```

Benefits:

- Stateless authentication
- Secure session handling

---

# 🚫 Phase 9 — Token Blacklisting

Refresh tokens now include JTI.

Revoked tokens stored in:

```
token_blacklist
```

Used for:

- Logout
- Token revocation

---

# 🛡 Phase 10 — Security Hardening

Added security mechanisms:

Rate limiting

```
Flask-Limiter
```

Security headers

```
Flask-Talisman
```

Includes:

- HSTS
- X-Frame-Options
- Content Security Policy

Benefits:

- Protection against abuse
- Improved API security

---

# 🔐 Phase 11 — Account Locking

Security feature added.

Rules:

```
3 failed PIN attempts → account locked
```

Unlock requires:

```
ADMIN_KEY
```

Benefits:

- Prevent brute force attacks

---

# 🎨 Phase 12 — Frontend Dashboard

A simple banking UI was built.

Pages:

```
Login
Register
Dashboard
Transfer
Transaction History
```

Frontend communicates with backend using:

```
Fetch API
```

---

# 🧩 Final System Architecture

```
Frontend (HTML / JS)
        ↓
Flask API
        ↓
Service Layer
        ↓
Repository Layer
        ↓
SQLite Database
```

---

# 🧠 Key Engineering Lessons

1. Separate business logic from database logic.
2. Keep controllers thin.
3. Use entities instead of tuples.
4. Implement centralized error handling.
5. Design APIs with security in mind.
6. Use layered architecture for scalability.
7. Web applications introduce concurrency challenges.
8. Authentication should be stateless.
9. Logging and monitoring are essential for production systems.

---

# 🎯 Current System State

The project is now:

- Full REST backend
- Secure authentication system
- Persistent database
- Layered architecture
- Transaction-safe
- Rate-limited
- Token-based authentication
- Frontend dashboard enabled

---

# 🔮 Future Improvements

Possible next steps:

- Docker containerization
- CI/CD pipeline
- API documentation
- Automated testing
- PostgreSQL migration
- Role-based admin dashboard
- API schema validation

---

# 📌 Personal Reflection

The project began as a small CLI banking script.

It evolved into a structured backend system featuring:

- Clean layered architecture
- Secure authentication
- REST API
- Database persistence
- Frontend interface

This marks the transition from basic scripting to **structured backend engineering**.