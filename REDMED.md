# MediMind AI Healthcare Backend (REDMED) 🚀

Welcome to the **MediMind AI Healthcare Assistant** backend service (internally referred to as **REDMED**). This is a production-ready, highly interactive documentation hub designed to guide you through setting up, inspecting, and testing the FastAPI & MongoDB-powered clinical assistant service.

---

## 🗺️ Interactive Navigation Map

Select any of the options below to expand details dynamically:

* **[⚡ Quick Navigation](#-quick-navigation)**
* **[🛠️ Interactive Workspace Setup Checklist](#%EF%B8%8F-interactive-workspace-setup-checklist)**
* **[🐳 Containerization with Docker](#-containerization-with-docker)**
* **[🔑 Interactive API Reference Accordeon](#-interactive-api-reference-accordeon)**
* **[🧬 Data Schema Blueprint](#-data-schema-blueprint)**
* **[🚨 Interactive Troubleshooting Guide](#-interactive-troubleshooting-guide)**

---

## ⚡ Quick Navigation

<details>
<summary><b>🔍 System Tech Stack Overview (Click to Expand)</b></summary>

### Core Technology Stack
*   **Framework**: Python 3.12+ / FastAPI (Asynchronous web engine)
*   **Database**: MongoDB via `Motor` Async Driver for Python
*   **Authentication**: Secure JWT (JSON Web Tokens) with `passlib` Bcrypt hashing
*   **Validation**: Pydantic v2 (Strict typing & data parsing)
*   **AI Integration**: Google Gemini AI Engine (`@google/genai`)
*   **Servers**: Uvicorn ASGI Server

</details>

<details>
<summary><b>📁 Interactive Folder Structure (Click to Expand)</b></summary>

```
backend/ (REDMED Root)
├── app/
│   ├── api/                  # FastAPI routers and endpoints
│   │   ├── admin.py          # Admin metrics and telemetry
│   │   ├── appointment.py    # Appointment scheduling
│   │   ├── auth.py           # JWT Authentication & Register
│   │   ├── chat.py           # Clinical AI chat & history
│   │   ├── disease.py        # Clinical condition guides
│   │   ├── medicine.py       # Drug knowledge search
│   │   ├── notification.py   # Patient alerts & reminders
│   │   └── users.py          # Patient profile management
│   ├── core/                 # App configurations & DB drivers
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── middleware/           # Logging & telemetry middleware
│   │   └── logging.py
│   ├── models/               # MongoDB models & collections schema
│   │   ├── appointment.py
│   │   ├── chat.py
│   │   └── ...
│   ├── schemas/              # Pydantic validation schemas
│   └── main.py               # Main FastAPI entrypoint
├── requirements.txt
└── docker-compose.yml
```

</details>

---

## 🛠️ Interactive Workspace Setup Checklist

Use this checklist to track your progress as you set up the environment. You can check off items as they are completed:

- [ ] **Step 1: Create Virtual Environment**
  ```bash
  python -m venv venv
  ```
- [ ] **Step 2: Activate Environment**
  - *On Windows:* `venv\Scripts\activate`
  - *On macOS/Linux:* `source venv/bin/activate`
- [ ] **Step 3: Install Core Dependencies**
  ```bash
  pip install -r requirements.txt
  ```
- [ ] **Step 4: Configure Environment Variables**
  Copy `.env.example` to `.env` and fill in secrets:
  ```bash
  cp .env.example .env
  ```
  <details>
  <summary><b>💡 Click to view Environment Configuration Schema</b></summary>

  | Variable Name | Description | Default Value | Required |
  | :--- | :--- | :--- | :--- |
  | `PROJECT_NAME` | Name of the backend application | `"MediMind AI Clinical API"` | No |
  | `SECRET_KEY` | JWT signature key | `"medimind_secret_key_change_me_in_production_123456789"` | Yes |
  | `MONGODB_URL` | MongoDB Connection URL | `"mongodb://localhost:27017"` | Yes |
  | `DATABASE_NAME` | Database identifier | `"medimind_db"` | No |
  | `GEMINI_API_KEY` | Google Gemini API Key | `""` | Yes |
  </details>

- [ ] **Step 5: Launch Local Server**
  ```bash
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
- [ ] **Step 6: Access API Documentation**
  - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
  - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐳 Containerization with Docker

<details>
<summary><b>📦 Run REDMED with Docker Compose (Click to Expand)</b></summary>

Deploy FastAPI and a localized MongoDB cluster simultaneously:

```bash
# Build & start containers in detached mode
docker-compose up --build -d

# Verify containers are running
docker-compose ps

# Tail container logs
docker-compose logs -f
```

</details>

---

## 🔑 Interactive API Reference Accordeon

Expand any section below to see active endpoints, descriptions, payloads, and mock options:

<details>
<summary><b>🔐 1. Authentication & Security (<code>/api/v1/auth</code>)</b></summary>

### Endpoints:
*   `POST /api/v1/auth/register` - Registers a new patient account.
*   `POST /api/v1/auth/login` - Authenticates credentials and returns a Bearer JWT Token.

#### Registration Payload Example:
```json
{
  "email": "patient@medimind.ai",
  "password": "SecurePassword123",
  "full_name": "Sarah Connor",
  "phone": "+1 555-987-6543"
}
```

#### Login Payload Example:
```json
{
  "email": "patient@medimind.ai",
  "password": "SecurePassword123"
}
```

#### 💡 Mock Fallback Login:
Don't have MongoDB configured yet? Use the mock credentials to test:
- **Email**: `demo@medimind.ai`
- **Password**: `password`

</details>

<details>
<summary><b>👤 2. Patient Profile Management (<code>/api/v1/users</code>)</b></summary>

### Endpoints:
*   `GET /api/v1/users/me` - Fetch authenticated patient profile, including clinical background.
*   `PUT /api/v1/users/me` - Update profile, allergies, or chronic conditions.

#### Profile Update Payload Example:
```json
{
  "full_name": "Sarah Connor",
  "phone": "+1 555-111-2222",
  "age": 29,
  "gender": "Female",
  "blood_group": "AB-",
  "allergies": ["Sulfa Drugs", "Penicillin"],
  "chronic_conditions": ["Mild Asthma"]
}
```

</details>

<details>
<summary><b>💬 3. Clinical AI Assistant Chat (<code>/api/v1/chat</code>)</b></summary>

### Endpoints:
*   `GET /api/v1/chat/sessions` - Retrieve all historical clinical consultation sessions.
*   `POST /api/v1/chat/message` - Send query to the Clinical AI Assistant (Gemini powered).
*   `DELETE /api/v1/chat/session/{session_id}` - Clear a specific consultation history.

#### Send Message Payload:
```json
{
  "message": "Explain what a lipid panel test measures and what high LDL signifies."
}
```

#### AI Response Structure:
```json
{
  "sender": "ai",
  "text": "...",
  "timestamp": "12:34:56",
  "suggested_actions": [
    "Explain lipid panel ranges",
    "Dietary advice for high LDL"
  ],
  "medical_disclaimer": true
}
```

</details>

<details>
<summary><b>💊 4. Medical Knowledge Base (<code>/api/v1/medicine</code>)</b></summary>

### Endpoints:
*   `GET /api/v1/medicine/search` - Search drugs, dosages, manufacturers, and warnings.

#### Query Parameter:
*   `q` (string, optional) - Query string (e.g., `Amlodipine`, `Metformin`, `Atorvastatin`).

#### Search Response Example:
```json
[
  {
    "id": "med_01",
    "name": "Amlodipine Besylate",
    "brand_names": ["Norvasc"],
    "category": "Antihypertensive",
    "dosage_form": "Tablet",
    "strength": "5mg",
    "requires_prescription": true
  }
]
```

</details>

<details>
<summary><b>🦠 5. Disease Guides (<code>/api/v1/disease</code>)</b></summary>

### Endpoints:
*   `GET /api/v1/disease/search` - Look up symptoms, risks, prevention, and treatment guides.

#### Query Parameter:
*   `q` (string, optional) - Query string (e.g., `Hypertension`, `Diabetes`).

</details>

<details>
  <summary><b>📅 6. Appointments & Scheduling (<code>/api/v1/appointment</code>)</b></summary>

### Endpoints:
*   `GET /api/v1/appointment/list` - List doctor appointments.
*   `POST /api/v1/appointment/create` - Schedule a new appointment.

#### Create Appointment Payload:
```json
{
  "doctor_name": "Dr. Sarah Jenkins, MD",
  "specialty": "Cardiology",
  "appointment_date": "2026-10-25T14:30:00Z",
  "location_or_link": "Metropolitan Health Tower Room 4",
  "notes": "Annual check-up"
}
```

</details>

<details>
<summary><b>🔔 7. Notifications & Alerts (<code>/api/v1/notification</code>)</b></summary>

### Endpoints:
*   `GET /api/v1/notification/list` - Fetch medication reminders and lab report alerts.
*   `PUT /api/v1/notification/mark-read/{notification_id}` - Mark an alert as read.

</details>

<details>
<summary><b>📈 8. Admin Telemetry & Metrics (<code>/api/v1/admin</code>)</b></summary>

### Endpoints:
*   `GET /api/v1/admin/summary` - View system telemetry, aggregate users, and AI usage logs. (Requires login token)

</details>

---

## 🧬 Data Schema Blueprint

<details>
<summary><b>👁️ Click to view Database Schemas & Collections</b></summary>

### User Collection (`users`)
```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "hashed_password": "string",
  "full_name": "string",
  "phone": "string",
  "age": "int",
  "gender": "string",
  "blood_group": "string",
  "allergies": "array[string]",
  "chronic_conditions": "array[string]",
  "avatar": "string (url)",
  "is_admin": "boolean",
  "created_at": "datetime"
}
```

### Chat Session Collection (`chat_history`)
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "title": "string",
  "messages": [
    {
      "sender": "user | ai",
      "text": "string",
      "timestamp": "string"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

</details>

---

## 🚨 Interactive Troubleshooting Guide

Click on any question to view its solution interactively:

<details>
<summary><b>❓ Port 8000 is already in use</b></summary>

Run the following command to identify and kill the process holding port `8000`:
*   **Linux/macOS:**
    ```bash
    kill -9 $(lsof -t -i:8000)
    ```
*   **Windows:**
    ```cmd
    for /f "tokens=5" %a in ('netstat -aon ^| findstr 8000') do taskkill /f /pid %a
    ```

</details>

<details>
<summary><b>❓ Database connection failed / "Mock In-Memory Mode" is active</b></summary>

Verify that:
1.  Your local MongoDB instance is running (`mongod` command).
2.  Your `MONGODB_URL` in `.env` matches your MongoDB connection string (e.g. `mongodb://localhost:27017` or MongoDB Atlas link).

</details>

<details>
<summary><b>❓ Gemini AI is not responding correctly</b></summary>

Make sure that:
1.  You have set `GEMINI_API_KEY` in your `.env` file.
2.  Your API Key is valid and has permissions to access the Gemini API.

</details>

---

*MediMind AI (REDMED) Backend is built with ❤️ for secure, production-grade medical analytics.*
