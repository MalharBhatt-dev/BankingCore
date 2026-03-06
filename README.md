# 🏦 Banking Core System

A **secure full-stack banking backend system** built using **Python, Flask, SQLite, and Vanilla JavaScript**.

This project demonstrates **real-world backend architecture**, including authentication, security hardening, layered design, and REST API integration with a frontend dashboard.

The system simulates core banking operations such as account creation, deposits, withdrawals, transfers, and transaction history.

---

# 📌 Project Overview

The Banking Core System was built to simulate a **production-style backend architecture** while maintaining clean engineering principles.

It includes:

- Secure REST API
- JWT Authentication
- Rate limiting
- Account locking mechanism
- Admin account unlock
- Token refresh & blacklist
- SQLite persistent storage
- Transaction audit trail
- Frontend banking dashboard

The project follows **clean layered architecture** and demonstrates backend engineering best practices.

---

# 🏗 System Architecture

```
Frontend (HTML / JS)
        ↓
REST API (Flask Routes)
        ↓
Service Layer (Business Logic)
        ↓
Repository Layer (Data Access)
        ↓
SQLite Database
```

---

# ⚙️ Tech Stack

### Backend
- Python
- Flask
- SQLite
- PyJWT
- Flask-Limiter
- Flask-Talisman
- python-dotenv

### Frontend
- HTML
- TailwindCSS
- Vanilla JavaScript

---

# 🔐 Security Features

The system implements several backend security mechanisms:

### JWT Authentication
- Access Token (15 minutes)
- Refresh Token (7 days)

### Token Revocation
- Refresh tokens use **JTI**
- Revoked tokens stored in **token_blacklist table**

### Rate Limiting
Implemented using Flask-Limiter.

Examples:
```
Login → 5 requests/minute  
Transfer → 5 requests/minute  
Deposit/Withdraw → 20 requests/minute
```

### Account Locking
- 3 incorrect PIN attempts
- Account automatically locked

### Admin Unlock
Admin can unlock accounts using **ADMIN_KEY**.

### HTTP Security Headers
Implemented using Flask-Talisman.

Includes:
- HSTS
- X-Frame-Options
- X-Content-Type-Options
- Content Security Policy

---

# 🧱 Application Layers

## 1️⃣ Entities (Domain Models)

Entities represent business objects.

```
Account
Transaction
```

They decouple the service layer from database schema.

---

## 2️⃣ Service Layer (Business Logic)

`BankingServices`

Responsibilities:

- Business rule validation
- Transaction control
- Atomic operations
- Security checks
- Exception raising

Example operations:

- Create account
- Deposit
- Withdraw
- Transfer money
- Authenticate user
- Unlock account
- Token blacklist management

This layer contains **zero SQL code**.

---

## 3️⃣ Repository Layer (Data Access)

`AccountRepository`

Responsibilities:

- Database connection management
- SQL execution
- Entity mapping
- Commit / rollback handling

SQLite is configured for Flask threading:

```
sqlite3.connect(DB_PATH, check_same_thread=False)
```

---

## 4️⃣ API Layer

Flask routes expose the system as a REST API.

Endpoints handle:

- Request parsing
- Authentication
- Authorization
- Delegation to service layer

Global error handlers convert exceptions into HTTP responses.

---

# 🌐 REST API Endpoints

## Authentication

### Login
```
POST /auth/login
```

Returns:

```
access_token
refresh_token
```

### Refresh Token
```
POST /auth/refresh
```

### Logout
```
POST /auth/logout
```

---

## Account Operations

### Create Account
```
POST /accounts
```

### View Balance
```
GET /accounts/<account_number>
```

### Deposit
```
POST /accounts/<account_number>/deposit
```

### Withdraw
```
POST /accounts/<account_number>/withdraw
```

### Transfer
```
POST /accounts/<account_number>/transfer
```

### Transaction History
```
GET /accounts/<account_number>/transactions
```

### Unlock Account (Admin)
```
POST /accounts/<account_number>/unlock
```

---

# 💾 Database Schema

## accounts

| Column | Description |
|------|-------------|
| account_number | Unique account id |
| account_holder_name | Account owner |
| pin_hash | Hashed PIN |
| balance | Current balance |
| created_at | Creation timestamp |
| failed_attempts | Failed login attempts |
| is_locked | Account lock state |
| role | user/admin |

---

## transactions

| Column | Description |
|------|-------------|
| account_number | Associated account |
| transaction_type | DEPOSIT / WITHDRAW / TRANSFER |
| amount | Transaction amount |
| balance_after | Balance after transaction |
| timestamp | Transaction time |

---

## token_blacklist

| Column | Description |
|------|-------------|
| jti | Token identifier |
| revoked_at | Revocation timestamp |

---

# 🎯 Core Features

### Account Creation
- Validates name and PIN
- Generates unique account number
- Logs initial deposit

### Deposit
- Validates account existence
- Logs transaction
- Updates balance atomically

### Withdrawal
- Ensures sufficient balance
- Logs withdrawal

### Transfer
- Atomic balance update
- Logs transfer in both accounts

### Transaction History
- Full audit trail

---

# 🎨 Frontend Interface

Simple banking dashboard built with HTML and JavaScript.

Pages include:

```
Login Page
Register Account
Dashboard
Transfer Page
Transaction History
```

Frontend communicates with backend using **Fetch API**.

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

### Install dependencies

```
pip install -r requirements.txt
```

### Set environment variables

Create `.env`

```
SECRET_KEY=your_secret_key
ADMIN_KEY=your_admin_key
FLASK_DEBUG=true
```

### Run the server

```
python run.py
```

Server starts at:

```
http://127.0.0.1:5000
```

---

# 🧠 Engineering Principles Applied

- Layered Architecture
- Repository Pattern
- Dependency Injection
- Domain Modeling
- JWT Authentication
- Security Hardening
- Centralized Error Handling
- Atomic Transactions
- Separation of Concerns
- RESTful Design

---

# 🔮 Future Enhancements

Possible improvements:

- Role-based admin dashboard
- Docker containerization
- CI/CD pipeline
- Unit testing
- PostgreSQL migration
- Request validation (Pydantic)
- API documentation (Swagger)

---

# 📘 Development Log

For full development evolution:

```
development_log.md
```

---

# ⚡ Philosophy

Start simple.  
Refactor intentionally.  
Design for scale.  
Separate responsibilities.

---

🏦 Built as a structured backend architecture project demonstrating real-world engineering practices.