# 🏦 Banking Core System

A production-structured backend banking system built using **Python, SQLite, and Flask**.

This project evolved from a simple CLI application into a layered backend architecture supporting both:

- 🖥 CLI Interface  
- 🌐 REST API Interface  

It demonstrates clean architecture principles, database persistence, structured exception handling, and scalable backend design.

---

## 📌 Overview

The Banking Core System simulates real-world banking operations while applying professional backend engineering practices.

The system supports:

- Account creation
- Deposit funds
- Withdraw funds
- View account balance
- View transaction history

Unlike basic tutorial projects, this system implements:

- Layered Architecture
- Repository Pattern
- Domain Entity Modeling
- Custom Exception Hierarchy
- SQLite Persistence
- Atomic Transaction Handling
- RESTful API Exposure
- Global Error Handling

All data is stored in SQLite, ensuring persistence across application restarts.

---

## 🏗 System Architecture

The application follows a clean layered structure:

```bash
Interface Layer (CLI / REST)
        ↓
Service Layer (Business Logic)
        ↓
Repository Layer (Data Access)
        ↓
SQLite Database
```

---
## 🌐 Dual Interface Support
### 🖥 CLI Interface

- Console-driven interaction
- Menu-based operation
- Thin controller structure
- Exception-aware handling

### 🌐 REST API (Flask)

- JSON-based communication
- Proper HTTP status codes
- Centralized global error handling
- Thread-safe SQLite configuration
- Clean endpoint structure

---
## 🔹 REST API Endpoints

###  Create Account
```http
POST /accounts
```
### View Balance
```http
GET /accounts/<int:account_number>
```
### Deposit
```http
POST /accounts/<int:account_number>/deposit
```
###  Withdraw
```http
POST /accounts/<int:account_number>/withdraw
```

### View Transaction History
```http
GET /accounts/<int:account_number>/transactions
```
All endpoints return structured JSON responses with proper HTTP status codes.

---
## 🧱 Application Layers
### 1️⃣ Entities (Domain Models)

- `Account`
-  `Transaction`

    #### Purpose:

    - Represent business objects
    - Decouple service layer from database schema
    - Improve readability and maintainability

### 2️⃣ Service Layer (BankingServices)

#### Responsibilities:
- Input validation
- Business rule enforcement
- Transaction coordination
- Atomic commit / rollback control
- Raising domain-specific exceptions

This layer contains zero SQL code.

### 3️⃣ Repository Layer (AccountRepository)

#### Responsibilities:

- SQLite connection management
- SQL execution
- CRUD operations
- Mapping DB rows → Entity objects
- SQLite connection configured with:
```bash
sqlite3.connect(DB_PATH, check_same_thread=False)
```
Ensures compatibility with Flask's multi-threaded environment.

### 4️⃣ Interface Layer
#### CLI Controller (`main.py`)

- Handles user interaction
- Catches domain exceptions
- Calls service methods only

#### REST Controller (`api.py`)

- Receives HTTP requests
- Delegates logic to service layer
- Uses global error handlers

---

## 💾 Database Design

### SQLite is used for persistent storage.

### `accounts` Table
```bash
| Column              | Description                |
| ------------------- | -------------------------- |
| id                  | Primary key                |
| account_number      | Unique account identifier  |
| account_holder_name | Account owner name         |
| balance             | Current account balance    |
| created_at          | Account creation timestamp |
```
### `transactions` Table
```bash
| Column         | Description                          |
| -------------- | ------------------------------------ |
| id             | Primary key                          |
| account_number | Foreign key reference                |
| type           | INITIAL DEPOSIT / DEPOSIT / WITHDRAW |
| amount         | Transaction amount                   |
| balance_after  | Balance after transaction            |
| timestamp      | Transaction timestamp                |
```
### This design provides:

- Persistent storage
- Full audit trail
- Transaction history tracking
- Migration-ready schema

---
## 🎯 Core Features
### ✅ Account Creation

- Validates account holder name (alphabet + spaces only)
- Validates initial deposit ≥ 0
- Auto-generates unique account number
- Logs initial deposit transaction

### ✅ Deposit

- Validates account existence
- Validates positive amount
- Updates balance atomically
- Logs transaction

### ✅ Withdrawal

- Validates account existence
- Validates positive amount
- Ensures sufficient balance
- Updates balance atomically
- Logs transaction

### ✅ View Balance

- Retrieves current balance from database

### ✅ View Transaction History

- Returns full transaction log
- Includes type, amount, balance_after, timestamp

---

## ⚠️ Exception Architecture

###  Custom domain exception hierarchy:

- `BankingException` (Base)
- `AccountNotFoundException`
- `InvalidAmountException`
- `InsufficientBalanceException`
- `InvalidAccountNameException`

#### REST API uses global error handlers to convert exceptions into proper HTTP responses.

---

## 🧪 Validation Rules

- Account name must contain only letters and spaces
- Initial deposit must be ≥ 0
- Deposit amount must be > 0
- Withdrawal amount must be > 0
- Withdrawal must not exceed balance
- Account must exist before operation

---
## 📂 Project Structure
```bash
banking-core/
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
│   ├── base_exception.py
│   ├── account_not_found_exception.py
│   ├── invalid_amount_exception.py
│   ├── insufficient_balance_exception.py
│   └── invalid_account_name_exception.py
│
├── database/
│   └── accounts.db
│
├── docs/
│   └── development_log.md
│
├── api.py
├── main.py
└── README.md
```

---
## 🚀 Development Evolution
### Phase 1 – CLI Foundation
- Basic operations with in-memory storage.

### Phase 2 – SQLite Integration
- Persistent database + transaction safety.

### Phase 3 – Repository Pattern
- Separation of business logic from SQL.

### Phase 4 – Entity Modeling
- Mapping DB rows to domain objects.

### Phase 5 – Custom Exception Hierarchy
- Domain-driven error handling.

###Phase 6 – REST API Implementation
- Flask integration, JSON endpoints, HTTP status codes.

### Phase 7 – Global Error Handling
- Centralized exception management for clean API design.

---
## 🧠 Engineering Principles Applied

- Object-Oriented Programming
- Separation of Concerns
- Single Responsibility Principle
- Repository Pattern
- Layered Architecture
- Dependency Injection
- At mic Transactions
- Domain Modeling
- RESTful Design
- Centralized Error Handling

---

## 🎓 Learning Outcomes

### This project demonstrates:

- Backend system architecture
- Database persistence handling
- Service-layer business modeling
- Exception hierarchy design
- REST API construction
- Thread-aware SQLite integration
- Clean layered engineering

---

## 🔮 Future Enhancements

- PIN-based authentication
- Account locking mechanism
- Logging & monitoring layer
- Unit & integration testing
- Blueprint & App Factory refactor
- MySQL/PostgreSQL migration
- Dockerization
- CI/CD pipeline integration

---
## 📘 Development Log

### For full architectural evolution details:
```bash
docs/development_log.md
```

---
### ⚡ Philosophy
Start simple.
Refactor intentionally.
Separate responsibilities.
Persist safely.
Design for evolution.

---
🏦 Built as a structured backend architecture project demonstrating real-world engineering practices.