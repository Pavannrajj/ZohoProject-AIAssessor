# AI-Powered Zoho Projects Chatbot

## Overview

This project is a conversational AI chatbot that integrates with Zoho Projects using REST APIs. It allows users to log in with their own Zoho accounts and interact with projects and tasks using natural language.

The system is built using a multi-agent architecture powered by LangGraph, with FastAPI as the backend and Vite (React) as the frontend.

---

## Features

### 1. OAuth Authentication (Zoho)

* Authorization Code Grant flow
* User-specific access and refresh tokens
* Automatic token refresh handling
* Secure session-based authentication

### 2. Multi-Agent Architecture

* **Query Agent**: Handles read operations

  * List projects
  * List tasks
  * Get task details
  * Get project members
  * Task utilisation

* **Action Agent**: Handles write operations

  * Create task
  * Update task
  * Delete task
  * Requires human-in-the-loop confirmation

* **Router/Supervisor**: Routes user queries to the correct agent

---

## Tools Implemented

| Tool                 | Description                       |
| -------------------- | --------------------------------- |
| list_projects        | Fetch all projects                |
| list_tasks           | List tasks with filters           |
| get_task_details     | Get full task info                |
| create_task          | Create new task                   |
| update_task          | Update task fields                |
| delete_task          | Delete a task (with confirmation) |
| list_project_members | List members and roles            |
| get_task_utilisation | Task distribution summary         |


---

## Human-in-the-Loop (HIL)

* All write operations require explicit user confirmation
* Preview shown before execution
* Supports confirm and cancel actions

---

## Tech Stack

### Backend

* FastAPI (async)
* LangGraph
* Zoho Projects REST API

### Frontend

* React (Vite)
* Fetch API for communication


---

## Project Structure

```
backend/
 ├── main.py
 ├── graph/
 ├── agents/
 ├── tools/
 ├── auth/
 ├── memory/
 └── zoho_client/

frontend/
 ├── src/
 ├── components/
 └── services/
```

---

## Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/Pavannrajj/ZohoProject-AIAssessor.git
cd project
```

### 2. Backend Setup

```
cd backend
pip install -r requirements.txt
```

Create `.env` file:

```
ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
ZOHO_REDIRECT_URI=http://localhost:8000/auth/callback
ZOHO_AUTH_URL=
ZOHO_TOKEN_URL=
```

Run backend:

```
uvicorn main:app --reload
```

---

### 3. Frontend Setup

```
cd frontend
npm install
npm run dev
```

---

## OAuth Configuration Guide

1. Go to Zoho Developer Console
2. Create a new client
3. Set redirect URI:

   ```
   http://localhost:8000/auth/callback
   ```
4. Copy client ID and secret into `.env`
5. Enable required scopes:

   * Projects
   * Tasks

---

## API Endpoints

### Chat Endpoint

```
POST /chat
```

Request:

```
{
  "message": "user input"
}
```

Response:

```
{
  "response": "bot reply",
  "pending_action": null or object
}
```

---

### Auth Endpoints

```
GET /auth/login
GET /auth/callback
```

---

## Demo Flows Supported

* List projects
* List tasks using context memory
* Get task details
* Create task with confirmation
* Update task with confirmation
* Delete task with confirmation
* Task utilisation summary

---

## Known Limitations

* Depends on Zoho API availability
* Limited natural language understanding for complex queries
* UI is minimal and focused on functionality

---

## Future Improvements

* Better NLP understanding
* Improved UI/UX
* Caching for faster responses
* Role-based access control

---

## Environment Variables (.env.example)

```
ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
ZOHO_REDIRECT_URI=
ZOHO_AUTH_URL=
ZOHO_TOKEN_URL=
SESSION_SECRET=
```

---

## Author

Pavan
