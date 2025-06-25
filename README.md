# Personal Habit Challenge League (Backend)

This is the **backend API** for the Personal Habit Challenge League — a productivity and wellness platform that allows users to track personal habits, create and join challenges, and monitor progress through entries. This RESTful API, built with **Flask** and **SQLAlchemy**, powers the full-stack application by managing data models and serving endpoints to the frontend.

> 🚀 The frontend repository is hosted [here](https://github.com/Christine-June/Personal-Habit-League-2)

---

## 📑 Table of Contents

- [Project Description](#project-description)
- [Models](#models)
- [Routes (Endpoints)](#routes-endpoints)
- [File Descriptions](#file-descriptions)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Contributors](#contributors)

---

## 📘 Project Description

The **Personal Habit Challenge League** is a web app that helps users:
- Track personal habit entries (e.g., drink water, read books)
- Create and join group challenges
- Monitor user and team progress
- Stay accountable through daily tracking

The backend is built with **Flask** and follows RESTful conventions. It interacts with a relational database via SQLAlchemy and supports CRUD functionality for users, habits, challenges, entries, and many-to-many relationships.

---

## 🧠 Models

Each model corresponds to a table in the database and has relationships mapped using SQLAlchemy:

### 1. `User`
- Attributes: `id`, `username`, `email`
- Relationships:
  - Has many `HabitEntries`, `UserHabits`, `ChallengeParticipants`

### 2. `Habit`
- Attributes: `id`, `name`, `category`
- Relationships:
  - Has many `UserHabits`, `HabitEntries`

### 3. `UserHabit`
- Join table between Users and Habits
- Attributes: `id`, `user_id`, `habit_id`, `target_frequency`

### 4. `HabitEntry`
- Tracks daily habit activity
- Attributes: `id`, `user_id`, `habit_id`, `date`, `value`, `notes`

### 5. `Challenge`
- Attributes: `id`, `title`, `description`, `start_date`, `end_date`
- Relationships:
  - Has many `ChallengeParticipants`, `ChallengeEntries`

### 6. `ChallengeParticipant`
- Join table between Users and Challenges
- Attributes: `id`, `user_id`, `challenge_id`

### 7. `ChallengeEntry`
- Logs contributions to a challenge
- Attributes: `id`, `user_id`, `challenge_id`, `date`, `value`, `notes`

---

## 🔗 Routes (Endpoints)

The following key routes power the API:

### `GET /users`
- Returns a list of all users

### `GET /habits`
- Returns a list of all available habits

### `GET /user_habits`
- Lists all user-habit relationships

### `GET /habit_entries`
- Returns all entries logged by users for habits

### `POST /habit_entries`
- Adds a new habit entry (includes validation)

### `GET /challenges`
- Lists all active challenges

### `POST /challenges`
- Creates a new challenge

### `GET /challenge_participants`
- Lists which users have joined which challenges

### `POST /challenge_entries`
- Logs a new entry in an active challenge

Each route uses proper error handling and returns data in JSON format.

---

## 📂 File Descriptions

### `app.py`
- Entry point for the Flask app.
- Registers blueprints and initializes the app config, DB, and CORS.

### `models.py`
- All database models are defined here using SQLAlchemy.
- Relationships are defined using `db.relationship()` and `db.ForeignKey`.

### `routes/`
- Modular blueprints for each resource (e.g. users, habits, entries).
- Each file defines RESTful route handlers and integrates with the models.

### `config.py`
- Manages environment config for Flask (development, testing, production).
- Connects to SQLite or PostgreSQL as needed.

### `db_seed.py`
- Seeds the database with sample data for testing/demo purposes.

---

## 🛠️ Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- SQLite3 (dev) / PostgreSQL (prod-ready)
- Marshmallow (for serialization)
- dotenv

---

## 🧪 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Christine-June/Personal-Habit-Challenge-League
cd Personal-Habit-Challenge-League

2. Create and activate virtual environment
- python3 -m venv venv
- source venv/bin/activate

. Run the server
- flask run

. Seed the database (optional)
- python db_seed.py

👥 Contributors
Christine Mworia (Team-Lead)

Brian Kaloki - Team Member

Eugene Wekesa - Team Member

Regina Kariuki - Team Member

Anderson Waithaka - Team Member

Priscillah Njai - Team Member

📎 Notes
The frontend is a separate repo, but fully integrated with this backend via HTTP.

Be sure to set CORS headers correctly when deploying.

Environment variables such as DATABASE_URI and FLASK_ENV are managed via .env.

