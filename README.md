#DriftDater-Dating Application

##  Project Description

Drift Dater App is a full-stack dating web application built with **Vue 3 (frontend)** and **Flask (backend API)**. The platform allows users to create profiles, discover compatible matches based on shared criteria, and communicate through a messaging system once a mutual match is established.

The application demonstrates key concepts such as RESTful API development, relational database design, authentication, and frontend-backend integration.

---

## Team Members & Roles

| Name           | Role            | Responsibilities                                     |
| -------------- | --------------- | ---------------------------------------------------- |
| Nyishia Robinson | Project Manager and QA/Testing Lead | Coordinated tasks, ensured deadlines were met and Database  |
| Ravaughn Marsh   | Backend Lead                        | Developed Flask API, database models, authentication |
| Daniel England    | Frontend Lead                      | Built Vue components, UI/UX design                   |
| Ivanna Buckley | Testing Lead                          | Review documentation                   |

---
## Database Schema Documentation 

The dating app, DriftDater, its database consists of five (5) tables (users, profiles, matches, messages, and favorites), created to handle authentication, user profiles, matching logic, and communication. 

Table Name: users 

| Name          |  Data Type   | Responsibilities / Description         |
| ------------- | ------------ | -------------------------------------- |
| id            | Integer (PK) | Unique identifier for the account      |
| email         | String(120)  | User login identifier (Unique/Indexed) |
| password_hash | String(128)  | Secure hashed credentials (Bcrypt)     |
| created_at    | DateTime     | Timestamp of registration              |
| is_public     | Boolean      | Visibility control for discovery       |


Table Name: profiles
| Name            |  Data Type   | Responsibilities / Description             |
| --------------- | ------------ | ------------------------------------------ |
| id              | Integer (PK) | Unique profile identifier                  |
| user_id         | Integer (FK) | Reference to the users table (1:1)         |
| name            | String(80)   | User's display name                        |
| age             | Integer      | Age for matching/filtering                 |
| bio             | Text         | User biography/description                 |
| location        | String(120)  | Geographic location for proximity matching |
| interests       | JSON         | List of hobbies/interests for algorithm    |
| profile_pic_url | String(255)  | Path to user's uploaded profile image      |
| gender          | String(20)   | Custom field for identification            |
| looking_for     | String(20)   | Custom field for preferences               |

Table Name: matches 

| Name       | Data Type    | Responsibilities / Description            |
| ---------- | ------------ | ----------------------------------------- |
| id         | Integer (PK) | Unique match record identifier            |
| user1_id   | Integer (FK) | ID of the initiating user                 |
| user2_id   | Integer (FK) | ID of the target user                     |
| status     | String(20)   | Status: 'liked', 'matched', or 'rejected' |
| created_at | DateTime     | Timestamp of the interaction              |


Table Name: messages 

| Name        | Data Type    | Responsibilities / Description               |
| ----------- | ------------ | -------------------------------------------- |
| id          | Integer (PK) | Unique message identifier                    |
| sender_id   | Integer (FK) | ID of the user sending the message           |
| receiver_id | Integer (FK) | ID of the user receiving the message         |
| content     | Text         | The body text of the message                 |
| timestamp   | DateTime     | Exact time the message was sent              |
| is_read     | Boolean      | Tracks if the recipient has seen the message |

Table Name: favorites 

| Name             | Data Type    | Responsibilities / Description        |
| ---------------- | ------------ | ------------------------------------- |
| id               | Integer (PK) | Unique bookmark identifier            |
| user_id          | Integer (FK) | User who is bookmarking a profile     |
| favorite_user_id | Integer (FK) | The profile being bookmarked          |
| created_at       | DateTime     | Timestamp when the favorite was added |

## Normalization Explanation (3rd Normal Form) 

The database structure adheres to 3rd Normal Form (3NF) to limit the redundacy and prevent data anomalies, such as:

1. Elimination of Redundancy (1NF/2NF): All of the tables mainly focuess on a single entity. All the non-key attributes are seen to be fully dependent on the Primary key (PK).
2. Transitive Dependencies (3NF): The table users was separated from profiles. The attributes like bio or even profile_pic_url do not necessarily depend on the user's email or passowrd but rather on the user's ID. This separation encourages the privacy of sensitive login data from being exposed during profile updates.
3. Junction Tables: The relationships such as matches and favorites are used as a foreign key (FK) to connect users, ensureing that the user data is stayed at one particualr place.


## Indexing 

To gather a high performance and meet the requirement of less than two second load time, the following below are ways in which indexing is implemented:

1. Primary Indexes: The lookup for Users.id and users.email is O(1).
2. Foreign key Indexes: Indexes such as user_id and sender_id indicates a rapid retrieval of a user specific content.
3. Unique Constraint: The prevent data corruption and the duplication of entries at the database level, such as favorites and matches.


## ER Diagram Logic

Users ↔ Profiles: One-to-One (1:1).

Users ↔ Matches: One-to-Many (1:N) - One user can have many match entries.

Users ↔ Messages: One-to-Many (1:N) - One user can send/receive many messages.

Users ↔ Favorites: One-to-Many (1:N).



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

## API Documentation

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

## Limitations
* There was minimal major issues other than the UI responsiveness may have minor issues on very small screens. 

---

## Future Improvements For the Application
* Add email verification system
* Improve matching algorithm with weighted scoring
* Add user blocking/reporting feature

---
