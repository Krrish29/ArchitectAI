# ArchitectAI

ArchitectAI is an AI-powered Software Architect that transforms software ideas into structured technical blueprints using a multi-agent architecture.

Instead of generating a single AI response, ArchitectAI orchestrates specialized AI agents to collaboratively produce requirements, system architecture, database design, API specifications, and an implementation roadmap.

---

## Features

* Multi-Agent AI Workflow
* Intelligent Supervisor Agent
* Requirement Analysis
* System Architecture Generation
* Database Schema Design
* REST API Specification Generation
* Implementation Roadmap
* Dependency-Aware Agent Execution
* Modern React Dashboard
* Project History Management
* Editable Blueprint Sections
* Local Project Persistence
* Responsive UI built with TailwindCSS

---

## Tech Stack

### Frontend

* React
* Vite
* TailwindCSS
* Context API
* LocalStorage
* Lucide React
* Axios

### Backend

* FastAPI
* Pydantic
* Ollama
* Qwen2.5:3B
* Python

---

# System Architecture

```text
User
 │
 ▼
FastAPI Backend
 │
 ▼
Supervisor Agent
 │
 ▼
Dependency Resolver
 │
 ▼
Requirement Agent
 │
 ▼
Architecture Agent
 │
 ▼
Database Agent
 │
 ▼
API Agent
 │
 ▼
Planner Agent
 │
 ▼
Blueprint Response
```

---

# AI Agents

## Supervisor Agent

* Analyzes the user's idea
* Selects only the required agents
* Resolves dependencies between agents

---

## Requirement Agent

Generates:

* Project Name
* Features
* Functional Requirements
* Non-Functional Requirements

---

## Architecture Agent

Generates:

* High-Level Architecture
* Technology Stack
* Major Components
* Communication Flow

---

## Database Agent

Generates:

* Database Selection
* Entities
* Relationships
* Index Recommendations

---

## API Agent

Generates:

* REST Endpoints
* Request Schemas
* Response Schemas

---

## Planner Agent

Generates:

* Development Phases
* Milestones
* Implementation Roadmap

---

# Project Structure

```text
ArchitectAI
│
├── backend
│   ├── agents
│   ├── orchestrator
│   ├── routes
│   ├── schemas
│   ├── services
│   └── main.py
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── context
│   │   ├── pages
│   │   ├── services
│   │   └── utils
│   └── package.json
│
└── README.md
```

---

# How It Works

1. User enters a software idea.
2. The Supervisor Agent analyzes the request.
3. Required AI agents are selected.
4. Dependencies are resolved.
5. Agents execute in the correct order.
6. A complete software blueprint is generated.
7. The blueprint is displayed in the React dashboard.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/ArchitectAI.git
cd ArchitectAI
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Start Ollama:

```bash
ollama serve
```

Pull the model:

```bash
ollama pull qwen2.5:3b
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# Future Roadmap

* AI Blueprint Updates
* Blueprint Chat
* Dynamic Blueprint Renderer
* React Flow Architecture Diagrams
* Server-Sent Events (Live Agent Progress)
* Export to PDF
* Export to Markdown
* Export to JSON
* Docker Project Generation
* README Generation

---

# Screenshots

Add screenshots here after deployment.

Example:

```
docs/images/home.png

docs/images/sidebar.png

docs/images/blueprint.png
```

---

# License

This project is licensed under the MIT License.

---

# Author

**Krrish Garg**

Final Year Computer Science Engineering Student

AI | Full Stack Development | Agentic AI | FastAPI | React | Python
