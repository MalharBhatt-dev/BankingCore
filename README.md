# 🏦 Banking Core System

A **Full-Stack Banking Application** built using **Flask (Backend)** and **Vanilla JS + Tailwind CSS (Frontend)**.
This project simulates a real-world banking system with **secure authentication, role-based access, transactions, and service request workflows**.

---

## 🚀 Features

### 👤 User Features

* Account Registration
* Secure Login (JWT आधारित)
* View Balance & Account Info
* Deposit & Withdraw Money
* Transfer Funds between Accounts
* Transaction History
* Service Requests (Change PIN, Update Name)

### 🧑‍💼 Employee Features

* View Pending Service Requests
* Approve / Reject Requests
* Process Customer Changes

### 🛡️ Admin Features

* Dashboard with Banking Statistics
* View Security Events
* Lock/Unlock Accounts
* Monitor System Activity

---

## 🧱 Tech Stack

### Backend

* Python (Flask)
* REST APIs
* JWT Authentication
* Flask-Limiter (Rate Limiting)
* Flask-Talisman (Security Headers)
* Logging (Rotating File Handler)

### Frontend

* HTML + Tailwind CSS
* Vanilla JavaScript
* LocalStorage / SessionStorage

---

## 📂 Project Structure

```
BankingCore/
│
├── app/                          # Core Flask Application
│   ├── __init__.py               # App factory (create_app, DI, logging, security)
│   ├── config.py                 # Environment configuration (SECRET_KEY, ADMIN_KEY)
│   ├── routes.py                 # All API endpoints (accounts, auth, admin, requests)
│   ├── errors.py                 # Global error handlers
│   ├── auth.py                   # JWT handling, decorators (login_required, role_required)
│   ├── extensions.py             # Extensions (Limiter, etc.)
│
├── repository/                   # Data Access Layer (DAL)
│   ├── account_repository.py     # Account DB operations
│   ├── service_request_repository.py  # Service request DB operations
│
├── services/                     # Business Logic Layer
│   ├── banking_services.py       # Core banking logic (deposit, withdraw, transfer)
│   ├── service_request_service.py # Request lifecycle (approve, reject, submit)
│
├── models/ (optional / implicit) # DB Models (if using ORM)
│   ├── account.py
│   ├── transaction.py
│   ├── service_request.py
│
├── static/ or frontend/          # Frontend (HTML + JS + Tailwind)
│
│   ├── html/
│   │   ├── register.html         # Account creation UI
│   │   ├── dashboard.html        # User dashboard
│   │   ├── transfer.html         # Money transfer UI
│   │   ├── transactions.html     # Transaction history
│   │   ├── service_requests.html # User request management
│   │   │
│   │   ├── employee.html         # Employee login
│   │   ├── employee_dashboard.html  # Employee request panel
│   │   │
│   │   ├── admin.html            # Admin login
│   │   ├── admin_dashboard.html  # Admin analytics dashboard
│   │   ├── admin_unlock_account.html # Unlock accounts UI
│
│   ├── js/
│   │   ├── api.js                # Common API handler (fetch wrapper + JWT)
│   │   ├── login.js              # Login modal + role handling
│   │   ├── register.js           # Account registration logic
│   │   ├── dashboard.js          # User dashboard logic
│   │   ├── transfer.js           # Transfer logic
│   │   ├── transactions.js       # Transactions rendering
│   │   ├── service_requests.js   # Request lifecycle (user side)
│   │   │
│   │   ├── employee.js           # Employee login
│   │   ├── employee_dashboard.js # Approve/reject requests
│   │   │
│   │   ├── admin.js              # Admin login + unlock
│   │   ├── admin_dashboard.js    # Admin analytics & security events
│
│   ├── css/
│       └── output.css            # Tailwind compiled CSS
│
├── logs/                         # Application logs
│   └── banking_core.log
│
├── .env                          # Environment variables
├── index.html            # Landing page + Login modal
├── requirements.txt              # Python dependencies
├── app.py / wsgi.py              # Entry point to start server
├── README.md                     # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/MalharBhatt-dev/BankingCore.git
cd BankingCore
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
ADMIN_KEY=your_admin_key
FLASK_DEBUG=true
```

👉 Required because config validates them at startup 

---

### 5️⃣ Run Backend Server

```bash
python app.py
```

Server runs at:

```
http://127.0.0.1:5000
```

---

### 6️⃣ Run Frontend

Just open:

```
index.html
```

Frontend communicates with backend via:

```js
const API_BASE = "http://127.0.0.1:5000";
```



---

## 🔐 Authentication Flow

* Login returns:

  * Access Token
  * Refresh Token
* Stored in browser storage
* Used in API requests via Authorization header

---

## 📡 API Overview

### Account APIs

* `POST /accounts` → Create Account
* `GET /accounts/{id}` → Get Balance
* `POST /deposit`
* `POST /withdraw`
* `POST /transfer`

### Auth APIs

* `POST /auth/login`
* `POST /auth/refresh`
* `POST /auth/logout`

### Admin APIs

* `/admin/stats`
* `/admin/events`
* `/admin/unlock`

### Service Requests

* `POST /requests`
* `GET /requests/my`
* Employee Approval Flow

---

## 🔄 Service Request Flow

1. User creates request
2. Employee reviews (Approve/Reject)
3. User submits required data
4. System updates account
5. Request marked completed

---

## 🛡️ Security Features

* JWT Authentication
* Role-Based Access Control
* Rate Limiting (Login, Transfer)
* CSP Headers (via Talisman)
* Token Blacklisting (Logout)

---

## 📊 Admin Dashboard Includes

* Total Bank Balance
* Total Accounts
* Locked Accounts
* Security Events Log

---

## 🔥 Future Enhancements

* KYC Update Feature
* Contact Update
* Account Closure Flow
* Notifications System
* Docker Deployment
* CI/CD Pipeline

---

## 📸 Screens (Optional)

*Add screenshots here*

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📄 License

This project is for learning and demonstration purposes.

---

## 👨‍💻 Author

**Malhar Bhatt**
GitHub: https://github.com/MalharBhatt-dev

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
