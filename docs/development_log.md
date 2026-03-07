# 📘 Banking Core – Development Evolution Log

This document tracks the architectural and structural evolution of the Banking Core project.

The goal of this log is:
- To document learning progression
- To preserve architectural decisions
- To serve as a reference guide for future backend projects
- To build professional development habits

---

# 🚀 Phase 1 – Basic CLI Banking (Initial Objective)

### Goal:
Build a simple CLI banking system with:

- Create account
- Deposit
- Withdraw
- Check balance
- Exit

### Characteristics:
- No database
- In-memory storage
- Basic class-based design
- Direct logic handling inside CLI

### Learning:
- Basic OOP
- Class structure
- Method interaction
- Simple validation

---

# 💾 Phase 2 – SQLite Integration

### Upgrade:
Replace in-memory storage with SQLite persistence.

### Changes:
- Introduced `sqlite3`
- Created `accounts` and `transactions` tables
- Implemented commit / rollback handling
- Ensured atomic transactions

### Architectural Impact:
- Data persists after application closes
- Introduced real database constraints
- Learned transaction safety

---

# 🏗 Phase 3 – Repository Pattern

### Problem:
Business logic and SQL were mixed.

### Solution:
Created `AccountRepository` layer.

### Responsibilities:
- Handle SQL queries
- Manage DB connection
- Map DB rows
- Commit / rollback

### Result:
- Separation of concerns
- Service layer isolated from SQL
- Cleaner architecture

---

# 🧠 Phase 4 – Service Layer (Business Logic Isolation)

### Introduced:
`BankingServices` layer

### Responsibilities:
- Input validation
- Business rules
- Transaction control
- Raising domain errors

### Benefits:
- No SQL in business logic
- Atomic operation control
- Clear responsibility separation

---

# 📦 Phase 5 – Domain Entities

### Added:
- `Account` entity
- `Transaction` entity

### Before:
Repository returned tuples.

### After:
Repository maps DB rows → Entity objects.

### Improvement:
- Removed tuple indexing (e.g., account[2])
- Improved readability (account.balance)
- Decoupled service layer from DB structure

---

# ⚠️ Phase 6 – Custom Exception Architecture

### Introduced:
Custom domain exception hierarchy:

- BankingException (Base)
- AccountNotFoundException
- InvalidAmountException
- InsufficientBalanceException
- InvalidAccountNameException

### Benefits:
- Clear domain error semantics
- Business errors separated from system errors
- REST API ready error mapping

---

# 🖥 Phase 7 – Thin CLI Controller

### Final CLI Structure:
- main.py acts as controller
- Only interacts with service layer
- No SQL in CLI
- Catches BankingException separately

### Architectural Model:

```bash
CLI → Service → Repository → SQLite  
            ↑  
         Entities  
```
---

# 🌐 Phase 8 – REST API Implementation (Flask Integration)

### Objective:
- Expose the banking backend as a RESTful API while preserving    clean layered architecture.

### Key Decisions:
- Reuse existing Service + Repository layers
- Keep API layer thin
- Maintain dependency injection
- Preserve atomic transaction handling

### 🔹 Endpoints Implemented

#### 1️⃣ Create Account
```bash
POST /accounts
```
#### 2️⃣ View Balance
```bash
GET /accounts/<int:account_number>
```
#### 3️⃣ Deposit
```bash
POST /accounts/<int:account_number>/deposit
```
#### 4️⃣ Withdraw
```bash
POST /accounts/<int:account_number>/withdraw
```

#### 5️⃣ View Transaction History
```bash
GET /accounts/<int:account_number>/transactions
```
### 🔹 REST Architectural Model
```bash
REST API (Flask)
        ↓
Service Layer
        ↓
Repository Layer
        ↓
SQLite Database
```
- CLI and REST now share the same backend core.

### 🔹 Threading Issue & Resolution
- Problem:
   - SQLite connection raised:
   ```bash
   SQLite objects created in a thread can only be used in that same thread
   ```
- Cause:
   - Flask runs in multi-threaded environment.

- Fix:
   - Enabled cross-thread usage:
   ```bash
   sqlite3.connect(DB_PATH, check_same_thread=False)
   ```
- Learning:
   - Web servers are multi-threaded
   - DB connection handling differs from CLI applications

### 🔹 Global Error Handling
- Before:
   - Each endpoint had repetitive try/except blocks.

- After:
   - Implemented Flask global error handlers:
   - BankingException → 400
   - Generic Exception → 500

- Benefits:
   - Cleaner endpoints
   - Centralized error logic
   - Professional API structure

### 🔹 Input Validation Refinement
- Enhanced domain validation:
   - Name must contain only alphabets and spaces (Regex enforced)
   - Prevented numeric and special-character names
   - Consistent JSON response structure
   - Standardized snake_case response keys
---

# 🧩 Final Architecture Summary

The system now follows:

- Clean layered architecture
- Repository pattern
- Domain modeling
- Atomic transactions
- Dependency injection
- Custom exception hierarchy
- SQLite persistence
- REST API exposure
- Global error handling
- Thread-aware DB integration

---

# 🧠 Key Engineering Lessons Learned

1. Separate business logic from database logic.
2. Never expose raw DB rows to service layer.
3. Use entities for domain modeling.
4. Use custom exceptions for semantic clarity.
5. Keep controllers (CLI/REST) thin.
6. Control transactions in service layer.
7. Web applications introduce threading complexity.
8. Centralized error handling improves maintainability.
9. Validation belongs in service layer, not controller.
10. Design for interface independence (CLI + REST)..

---

# 🎯 Current System State

The project is now:

- Resume-level backend system
- CLI + REST dual-interface architecture
- Structurally scalable
- Cleanly layered
- Transaction-safe
- Error-managed
- Database persistent
- Production-ready foundation

---

# 🚀 Next Possible Evolution Paths

- Add Authentication (PIN system)
- Implement account locking logic
- Introduce logging & monitoring
- Refactor into Blueprint / App Factory pattern
- Add request schema validation (Marshmallow / Pydantic)
- Dockerize application
- Add CI/CD pipeline
- Add unit & integration testing
- Migrate to MySQL/PostgreSQL

---

# 📌 Personal Reflection

The project began as a small CLI tool.

It evolved into a structured backend system with:

- A structured backend core
- A persistent database system
- A layered architecture implementation
- A REST-enabled service
- A thread-safe web backend

This marks the transition from beginner scripting to structured backend engineering.

The CLI phase built fundamentals.
The REST phase introduced real-world backend complexity.

This document represents the foundation of a scalable backend system.