# 🏦 Banking Core System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Security](https://img.shields.io/badge/Security-RateLimit%20%7C%20JWT%20%7C%20CSP-green)
![Status](https://img.shields.io/badge/Project-Active-success)

A **secure full-stack banking backend system** built using **Python, Flask, SQLite, and JavaScript**.

This project demonstrates **production-style backend architecture**, including authentication, layered design, security hardening, and REST API integration with a frontend dashboard.

---

# 📌 Project Overview

The **Banking Core System** simulates real-world banking operations while applying professional backend engineering practices.

The system supports:

- Account creation
- Deposit funds
- Withdraw funds
- Money transfer
- Transaction history
- Authentication
- Account locking
- Admin account unlock

Unlike basic CRUD projects, this system implements:

✔ Layered Architecture  
✔ Repository Pattern  
✔ Domain Entity Modeling  
✔ JWT Authentication  
✔ Token Refresh & Blacklisting  
✔ Rate Limiting  
✔ Security Headers  
✔ SQLite Persistence  
✔ Transaction Logging  

---

# 🏗 System Architecture

```
Frontend (HTML / JS)
        ↓
Flask REST API
        ↓
Service Layer (Business Logic)
        ↓
Repository Layer (Database Access)
        ↓
SQLite Database
```

This structure ensures:

- clean separation of responsibilities  
- scalable architecture  
- maintainable codebase  

---

# ⚙️ Tech Stack

## Backend

- Python
- Flask
- SQLite
- PyJWT
- Flask-Limiter
- Flask-Talisman
- python-dotenv

## Frontend

- HTML
- TailwindCSS
- Vanilla JavaScript
- Fetch API

---

# 🔐 Security Features

This project implements multiple backend security mechanisms.

## JWT Authentication

Two token system:

**Access Token**

```
Expires in 15 minutes
```

**Refresh Token**

```
Expires in 7 days
```

---

## Token Blacklisting

Refresh tokens include **JTI identifiers**.

Revoked tokens are stored in:

```
token_blacklist table
```

Used for:

- logout
- token revocation
- refresh security

---

## Rate Limiting

Implemented using **Flask-Limiter**.

Examples:

```
Login → 5 requests/minute
Transfer → 5 requests/minute
Deposit → 20 requests/minute
Withdraw → 20 requests/minute
```

Prevents brute-force and abuse attacks.

---

## Account Locking

Security mechanism for authentication.

```
3 incorrect PIN attempts → account locked
```

Unlock requires:

```
ADMIN_KEY
```

---

## HTTP Security Headers

Implemented using **Flask-Talisman**

Includes:

- HSTS
- X-Frame-Options
- X-Content-Type-Options
- Content Security Policy

---

# 🎯 Core Features

### Account Creation

- Name validation
- PIN hashing
- Unique account generation
- Initial transaction logging

---

### Deposit

- Validates account
- Ensures positive amount
- Updates balance atomically
- Logs transaction

---

### Withdrawal

- Validates account
- Prevents overdraft
- Logs withdrawal

---

### Transfer

- Atomic transfer operation
- Logs sender and receiver transactions

---

### Transaction History

Returns full transaction audit trail including:

- transaction type
- amount
- balance after transaction
- timestamp

---

# 🌐 REST API Endpoints

## Authentication

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/auth/login` | User login |
| POST | `/auth/refresh` | Refresh tokens |
| POST | `/auth/logout` | Logout |

---

## Account Operations

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/accounts` | Create account |
| GET | `/accounts/<id>` | View balance |
| POST | `/accounts/<id>/deposit` | Deposit money |
| POST | `/accounts/<id>/withdraw` | Withdraw money |
| POST | `/accounts/<id>/transfer` | Transfer money |
| GET | `/accounts/<id>/transactions` | Transaction history |

---

## Admin

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/accounts/<id>/unlock` | Unlock locked account |

---

# 💾 Database Schema

## Accounts Table

| Column | Description |
|------|-------------|
| account_number | Unique account identifier |
| account_holder_name | Owner name |
| pin_hash | Hashed PIN |
| balance | Current balance |
| created_at | Creation timestamp |
| failed_attempts | Failed login attempts |
| is_locked | Account lock state |
| role | user / admin |

---

## Transactions Table

| Column | Description |
|------|-------------|
| account_number | Related account |
| transaction_type | Deposit / Withdraw / Transfer |
| amount | Transaction amount |
| balance_after | Balance after operation |
| timestamp | Transaction time |

---

## Token Blacklist Table

| Column | Description |
|------|-------------|
| jti | Token identifier |
| revoked_at | Revocation time |

---

# 🎨 Frontend Interface

The project includes a simple banking dashboard.

### Pages

```
Login
Register
Dashboard
Transfer
Transactions
```

Frontend communicates with backend using:

```
Fetch API
```

---

# 📂 Project Structure

```
banking-core/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── auth.py
│   ├── config.py
│   ├── errors.py
│   └── extensions.py
│
├── entities/
│   ├── account.py
│   └── transaction.py
│
├── repository/
│   └── account_repository.py
│
├── services/
│   └── banking_services.py
│
├── exceptions/
│   └── custom exception classes
│
├── database/
│   └── accounts.db
│
├── frontend/
│   │
│   ├──── src/
│   │      │
│   │      ├──── css/
│   │      │        ├── input.css
│   │      │        └── output.css
│   │      │         
│   │      ├──── js/
│   │      │      ├── api.js
│   │      │      ├── index.js
│   │      │      ├── dashboard.js
│   │      │      ├── transfer.js
│   │      │      ├── transactions.js
│   │      │      └── register.js 
│   │      │ 
│   │      ├── index.html
│   │      ├── dashboard.html
│   │      ├── transfer.html
│   │      ├── transactions.html
│   │      └── register.html
│   │ 
│   └── package.json
├── run.py
├── requirements.txt
└── README.md
```

---

# 🚀 Running the Project

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 2️⃣ Configure environment variables

Create `.env`

```
SECRET_KEY=your_secret_key
ADMIN_KEY=your_admin_key
FLASK_DEBUG=true
```

---

### 3️⃣ Run the server

```
python run.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

# 🧠 Engineering Principles Applied

- Layered Architecture
- Repository Pattern
- Dependency Injection
- Domain Modeling
- RESTful Design
- JWT Authentication
- Security Hardening
- Atomic Transactions
- Centralized Error Handling
- Separation of Concerns

---

# 🔮 Future Enhancements

Possible improvements:

- Docker containerization
- CI/CD pipeline
- API documentation (Swagger)
- PostgreSQL migration
- Automated testing
- Role-based admin dashboard
- Request validation (Pydantic)

---

# 📘 Development Log

Full architectural evolution:

```
development_log.md
```

---

# ⚡ Philosophy

Start simple.  
Refactor intentionally.  
Separate responsibilities.  
Design for scale.

---

🏦 Built as a structured backend architecture project demonstrating real-world engineering practices.