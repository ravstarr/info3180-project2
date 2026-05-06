#DriftDater-Dating Application

##  Project Description

Drift Dater App is a full-stack dating web application built with **Vue 3 (frontend)** and **Flask (backend API)**. The platform allows users to create profiles, discover compatible matches based on shared criteria, and communicate through a messaging system once a mutual match is established.

The application demonstrates key concepts such as RESTful API development, relational database design, authentication, and frontend-backend integration.

---

## Team Members & Roles

| Name           | Role            | Responsibilities                                     |
| -------------- | --------------- | ---------------------------------------------------- |
| Nyishia Robinson | Project Manager | Coordinated tasks, ensured deadlines were met and Database  |
| Ravaughn Marsh   | Backend Lead    | Developed Flask API, database models, authentication |
| Daniel England    | Frontend Lead   | Built Vue components, UI/UX design                   |
| Ivanna Buckley | QA/Testing Lead | Testing, validation, documentation                   |

---

## Setup Instructions

Follow these steps to run the application locally:

### 1. Clone Repository

```bash
git clone https://github.com/ravstarr/info3180-project2.git
cd info3180-project
```

### 2. Backend Setup (Flask)

```bash
python -m venv venv
```

Activate virtual environment:

* Mac/Linux:

```bash
source venv/bin/activate
```

* Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up database:

```bash
flask db init
flask db migrate
flask db upgrade
```

Run backend server:

```bash
flask --app app --debug run
```

Backend runs on: http://127.0.0.1:5000

---

### 3. Frontend Setup (Vue 3)

Open a new terminal:

```bash
npm install
npm run dev
```

Frontend runs on: http://127.0.0.1:5173

---

## 🔌 API Documentation

### Authentication

| Endpoint         | Method | Description       | Request Body    | Response                      |
| ---------------- | ------ | ----------------- | --------------- | ----------------------------- |
| /api/v1/register | POST   | Register new user | email, password | 201 Created / 400 Bad Request |
| /api/v1/login    | POST   | Login user        | email, password | 200 OK / 401 Unauthorized     |
| /api/v1/logout   | POST   | Logout user       | None            | 200 OK                        |

---

### Profile Management

| Endpoint              | Method | Description                  |
| --------------------- | ------ | ---------------------------- |
| /api/v1/profile       | GET    | Fetch logged-in user profile |
| /api/v1/profile       | PUT    | Update user profile          |
| /api/v1/profile/image | POST   | Upload profile image         |

---

### Matching System

| Endpoint        | Method | Description               |
| --------------- | ------ | ------------------------- |
| /api/v1/like    | POST   | Like another user         |
| /api/v1/dislike | POST   | Dislike a user            |
| /api/v1/matches | GET    | Get all matches           |
| /api/v1/browse  | GET    | Browse users with filters |

---

### Messaging

| Endpoint                    | Method | Description                    |
| --------------------------- | ------ | ------------------------------ |
| /api/v1/messages            | POST   | Send message (only if matched) |
| /api/v1/messages/{match_id} | GET    | Get messages for a match       |

---

## ⚠️ Known Issues / Limitations
* There was minimal major issues other than the UI responsiveness may have minor issues on very small screens. 

---

## Future Improvements For the Application
* Add email verification system
* Improve matching algorithm with weighted scoring
* Add user blocking/reporting feature

---
