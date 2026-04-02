<div align="center">
  
# 🏦 BankingCore System

**A monolithic, full-stack banking ecosystem simulating core financial operations natively through Flask & Vanilla JavaScript.**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-000000?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![JSON Web Tokens](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)](https://jwt.io/)
[![Authentication](https://img.shields.io/badge/Auth-RBAC-4CAF50?style=for-the-badge&logo=letsencrypt&logoColor=white)]()
[![Coverage](https://img.shields.io/badge/Coverage-90%25-brightgreen?style=for-the-badge)](https://pytest.org/)
<br>
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

## 🚀 Live Demo
**Experience the platform live:** [👉 https://bankingcore.onrender.com](https://bankingcore.onrender.com)

---

## 📖 Overview

**BankingCore** is a comprehensive, tier-based financial management platform developed to simulate real-world enterprise banking workflows. Built using a robust **Python/Flask** backend REST API and a lightning-fast static frontend powered by **Tailwind CSS v4** and native JavaScript. 

This project aims to showcase production-ready engineering patterns, featuring **Role-Based Access Control (RBAC)**, comprehensive **JWT-based authentication workflows**, robust **service request lifecycle management**, and a highly-polished, responsive user interface utilizing modern design principles like glassmorphism and automatic dark-mode handling.

---

## ✨ Features

- **Account & Auth:** Secure account creation and JWT-based authentication.
- **Financial Operations:** Real-time Deposit, Withdraw, and P2P Transfers.
- **Transaction Ledgers:** Comprehensive, immutable transaction history tracking.
- **Role-Based Dashboards:** Specialized views tailored for User, Employee, and Admin access levels.
- **Service Workflow:** Asynchronous service request pipeline managed by Bank Operations.
- **Admin Controls:** High-level system oversight including manual account lock/unlock capabilities.
- **Security-First:** Multi-layer rate limiting, sandboxing, and strict HTTP security headers.

## 🏗️ Architecture

- **Backend:** Flask (REST API)
- **Frontend:** HTML, TailwindCSS, Vanilla JS
- **Auth:** JWT-based stateless authentication
- **Roles:** User / Employee / Admin
- **Deployment:** Render (Monolithic Full-Stack)

---

## 🏦 Role-Based Workflows

BankingCore supports three distinct hierarchical roles, each with specialized interfaces and API restrictions.

### 👤 1. Customer Portal 
Designed around a sleek, modern consumer UI heavily focused on user experience and accessibility.
* **Wallet Management:** Real-time dashboards displaying account balances and comprehensive transactional history dynamically fetched via REST.
* **Secure Transfers:** Peer-to-peer account transferring logic with strict server-side validation to prevent self-transfers or overdrafts.
* **Service Request Engine:** Customers can initiate asynchronous requests (e.g., PIN reset, KYC update). These requests are tracked via a life-cycle state machine (`PENDING`, `APPROVED`, etc.).

### 👔 2. Employee Workstation (BankOps)
A specialized enterprise-grade slate/indigo themed dashboard engineered for high-throughput data processing.
* **Request Processing Pipeline:** Employees act as the intermediary abstraction layer. They asynchronously fetch pools of pending customer requests and make `Approve` or `Reject` network calls based on internal logic.
* **State Management:** Secure transition of database ledgers based on employee input without granting employees direct account access.

### 🛡️ 3. Admin Security Command (AdminCore)
A critical tier designed with a minimalist zinc/violet aesthetic, meant for system overseers enforcing platform security.
* **Active Threat Monitoring:** Procedurally generated database hooks log account locks and brute-force attempts in real-time.
* **Override Controls:** Admins operate safely behind a secondary Authorization token layer ("Admin Key") to forcefully unlock customer accounts flagged by the platform's security algorithms.
* **System Ledgers:** Complete oversight read-access of all transactional volume and active service requests.

---

## 🛠️ Technology Stack & Engineering Decisions

### Backend Infrastructure (Flask ecosystem)
- **Framework:** `Flask` — Chosen for its lightweight footprint and granular control over the HTTP request/response cycle.
- **Security:** `Flask-Talisman` (CSP and HSTS Headers), `Flask-Limiter` (IP-based rate throttling against brute force attempts).
- **Authentication:** Custom encoded JSON Web Tokens (`PyJWT`) utilizing short-lived access tokens mapped against refresh tokens.
- **Layered Architecture:** strict separation of concerns utilizing Controllers (`routes.py`), Services (`banking_services.py`), and Repositories (`account_repository.py`).
- **Testing & QA:** Comprehensive integration and unit testing powered by `pytest`, achieving **90% codebase coverage**.

### Frontend Architecture
- **Rendering:** Static `HTML5` strictly decoupled from backend rendering engines for potential CDN distribution.
- **Styling:** `Tailwind CSS v4` integrated via browser-script for rapid, responsive UI composition. Features dark/light mode synchronization utilizing localStorage. 
- **Application Logic:** Vanilla Modern `JavaScript` fetching REST APIs asynchronously. No heavy frontend frameworks used, keeping bundle size minimal and showcasing core DOM-manipulation skills.

---

## 🛡️ Key Security Implementations

As a financial simulate, security was heavily prioritized:
1. **Multi-layer Rate Limiting:** All authentication and high-risk endpoints (Transfers, Admin actions) are clamped by `Flask-Limiter` to mitigate timing attacks and credential stuffing.
2. **Account Sandboxing:** Repeated failed login attempts intrinsically lock accounts. Only an authenticated Admin entity with a secondary cryptographic key can revert this state.
3. **Stateless Auth:** Entirely JWT-driven. The backend retains no stateful sessions, removing vectors for session-hijacking while horizontally scaling effortlessly. 
4. **Input Sanitization:** Controller layers strictly validate JSON payloads before parsing them to the Service business layer.

---

## 🚀 Quick Start / Local Deployment

### 1. Clone & Environment Activation
```bash
git clone https://github.com/MalharBhatt-dev/BankingCore.git
cd BankingCore
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Dependency Resolution
```bash
pip install -r requirements.txt
```

### 3. Environment Variable Configuration
Create a `.env` file in the root directory to supply critical config properties:
```env
SECRET_KEY=generate_a_secure_random_string
ADMIN_KEY=your_secure_admin_override_key
FLASK_DEBUG=true
```

### 4. Bootstrapping
Launch the localized Flask server framework:
```bash
python app.py
```
> The API will listen on `http://127.0.0.1:5000`

### 5. Client Interaction
No build step is required for the frontend. Simply open `index.html` in your modern browser of choice to interact with the system lifecycle.

---

## 📈 Future Roadmap

- Migrating data persistence layer to **PostgreSQL** supported by `SQLAlchemy` ORM.
- Implement **WebSockets** for live push-notifications regarding Transfer resolutions.
- Containerization sequence via **Docker** & **docker-compose** for one-click microservice deployments.

---

<div align="center">
  <b>Developed by <a href="https://github.com/MalharBhatt-dev">Malhar Bhatt</a></b><br>
  <i>Built to demonstrate passion for structured software engineering, design principles, and backend topology.</i>
</div>
