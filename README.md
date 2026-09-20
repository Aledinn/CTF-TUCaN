# TUCaN CTF A Guided Offensive Security Scenario

TUCaN CTF is a beginner-friendly Capture The Flag challenge simulating the TU Darmstadt student portal.

This project can serve as an introduction to offensive security concepts and Capture The Flag (CTF) challenges.  

A beginner-friendly walkthrough is available for those who want guided progression.

The entire environment is containerized and runs locally using Docker.

---

## Learning Objectives

This CTF introduces the following security concepts:

- Information disclosure  
- SQL injection  
- Insecure Direct Object References (IDOR)  
- Authentication and authorization weaknesses  
- Port scanning and service enumeration  
- Weak password hashing  
- Linux privilege escalation  

---

## Scenario

A friend of yours claims to have achieved excellent academic results at TU Darmstadt but refuses to provide any proof.

Driven by curiosity, you decide to investigate and discover an online student portal named **TUCaN**.

---

## Project Structure

```text
.
ctf-tucan/
├── docker-compose.yml
│   # Starts the vulnerable web application and the internal Linux system.

├── vuln-linux/
│   ├── Dockerfile
│   │   # Builds the internal Linux container used for pivoting and privilege escalation.
│   │   # Contains intentionally vulnerable configurations.
│   │
│   ├── entrypoint.sh
│   │   # Container entrypoint script.
│   │   # Sets up users, permissions, services (SSH), and legacy components.
│   │
│   └── legacy_check.c
│       # Source code of a vulnerable SUID binary.
│       # Reads sensitive system files as part of a legacy compatibility feature.

├── web/
│   ├── Dockerfile
│   │   # Builds the web application container (Flask + PostgreSQL).
│   │
│   ├── app.py
│   │   # Main Flask application entry point.
│   │   # Handles routing, session management, and core logic.
│   │
│   ├── auth.py
│   │   # Authentication logic.
│   │   # Contains intentionally vulnerable login mechanisms.
│   │
│   ├── admin.py
│   │   # Admin portal management
│   │
│   ├── db.py
│   │   # Database connection and helper functions.
│   │
│   ├── utils.py
│   │   # Utility functions shared across the backend.
│   │
│   ├── grades.py
│   │   # Logic related to grade retrieval.
│   │   # Contains IDOR vulnerability by design.
│   │
│   ├── generate_users.py
│   │   # Script used to populate the database with test users.
│   │
│   ├── generate_grades.py
│   │   # Script generating academic grades for users.
│   │
│   ├── generate_courses.py
│   │   # Script generating courses and course identifiers.
│   │
│   ├── requirements.txt
│   │   # Python dependencies required by the web application.
│   │
│   ├── internal/
│   │   └── dev_todo.txt
│   │       # Developer notes accidentally exposed through edge cases.
│   │
│   ├── templates/
│   │   # HTML templates rendered by Flask.
│   │
│   └── static/
│       ├── css/
│       │   # Stylesheets.
│       │
│       ├── js/
│       │   # Frontend JavaScript files.
│       │
│       ├── icons/
│       │   # UI icons.
│       │
│       ├── logo.gif
│       ├── logoadmin.png
│       └── tu-logo.gif
│           # Static assets used by the web interface.

├── db/
│   └── init/
│       # PostgreSQL schema and challenge seed data.

├── wordlists/
│   ├── familynames.txt
│   │   # List of family names used for user generation.
│   │
│   ├── names.txt
│   │   # List of first names used for user generation.
│   │
│   └── passwords.txt
│       # Weak password list used to generate vulnerable credentials.

├── WALKTHROUGH.pdf
│   # Step-by-step walkthrough intended for beginners.
│   # Can be followed alongside the CTF.

├── WRITEUP.pdf
│   # Official write-up describing the intended solution path and vulnerabilities.

```
---

## Requirements

- Docker
- Docker Compose

---

## Installation & Setup

Clone the repository:

```bash
git clone https://github.com/AleddineAbsi/CTF-TUCaN.git
cd CTF-TUCaN
```

Build and start the environment:

```bash
docker-compose up --build
```

Once the containers are running, access the web application at: http://localhost:5000

An internal Linux system is reachable via SSH on port 2222.

The PostgreSQL service is reachable only from the private Compose network. Its
data is stored in the `postgres_data` Docker volume and initialized from
`db/init/001-schema-and-data.sql` on first startup.

To reset the complete challenge dataset:

```bash
docker compose down -v
docker compose up --build
```

In the final privilege-escalation stage, use the intentionally permitted
PostgreSQL client instead of the legacy SQLite command shown in older copies of
the walkthrough:

```bash
sudo psql -h db -U tucan -d tucan
```

---

## Disclaimer

This project is intended for educational purposes only.

---

## License

This project is intended for educational and experimental use and may be reused or adapted accordingly.
