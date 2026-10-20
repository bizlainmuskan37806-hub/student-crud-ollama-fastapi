# Student CRUD FastAPI Backend

A Python FastAPI backend that provides student CRUD operations using SQLite and answers questions using a local Ollama `llama3.2:1b` model.

## Features

- Create, retrieve, list, update, and delete student records.
- Validate request data using Pydantic.
- Store student and question records in SQLite.
- Ask questions using a local Ollama model.
- Optionally include student-record context when answering questions.
- Paginate the student list using `skip` and `limit`.

## Project Structure

```text
FASTAPI3/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── ollama_client.py
│   └── routes/
│       ├── __init__.py
│       ├── base.py
│       ├── create_students.py
│       ├── get_student.py
│       ├── update_student.py
│       └── delete_student.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Requirements

- Python 3.9 or a compatible version for this project
- Ollama installed locally
- The Ollama model `llama3.2:1b`

## Setup

Run these commands from the project root in Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Install Ollama from [the official Ollama website](https://ollama.com/), then download the model:

```powershell
ollama pull llama3.2:1b
```

If Ollama is not already running, start it in a separate terminal:

```powershell
ollama serve
```

## Environment Configuration

Create a `.env` file in the project root with the following settings:

```dotenv
DATABASE_URL=sqlite:///./app.db
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:1b
```

The database URL above matches the configuration verified during development. Keep `.env` out of version control.

## Run the API

Start the FastAPI server from the project root:

```powershell
uvicorn main:app --reload
```

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | List students with pagination |
| GET | `/students/{student_id}` | Retrieve one student |
| PUT | `/students/{student_id}` | Replace a student's fields |
| PATCH | `/students/{student_id}` | Partially update a student |
| DELETE | `/students/{student_id}` | Delete a student |
| POST | `/ask` | Ask a question using Ollama |
| GET | `/health` | Check API health |

## Asking Questions

The `/ask` endpoint accepts a question and optional settings:

- `save`: controls whether the question and answer are saved.
- `use_student_context`: controls whether student records are included as context.

Set either option to `false` when you do not want that behavior.

Student CRUD operations use SQLite and do not require Ollama to generate answers.

## Validation

Use Swagger UI at `/docs` to try the endpoints and inspect their request and response schemas. The API validates input data and returns appropriate HTTP status codes for successful operations and common errors.

## Security and Version Control

- Do not commit `.env` or secrets.
- Keep the virtual environment and local database files out of version control.
- Student context may include personal data. Only use it when appropriate for the question and protect access to the API and database.
