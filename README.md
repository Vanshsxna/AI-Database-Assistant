# AI Database Assistant

---

## Overview

**AI Database Assistant** is an evolution of a custom-built Mini Database Engine, written entirely in Python — no SQL, no external database server, no ORM.

Instead of writing queries, users describe what they want in plain English:

> *"Create a students table."*
> *"Insert a student named Magnus who scored 91."*
> *"Show all students."*

An OpenAI GPT model interprets the request and converts it into a structured command, which is validated and executed against a lightweight, from-scratch JSON database engine.

This project is **not** a wrapper around MySQL, PostgreSQL, or any existing database — the storage engine, schema system, constraint validation, and query logic are all custom-built. The goal is to demonstrate how LLMs can be layered on top of a traditional data engine to create a genuinely intelligent, conversational database assistant, built with clean separation of concerns throughout.

---

## Features

- **Natural language querying** — no SQL syntax to learn
- **AI-powered interpretation** — GPT converts text into structured commands
- **Custom database engine** — schemas, types, and constraints built from scratch
- **Modular, layered architecture** — each component has a single responsibility
- **Multiple interfaces** — CLI, FastAPI backend, and Streamlit UI
- **Zero external database dependency** — everything persists to JSON

### Supported operations

| Operation | Description |
|---|---|
| Create Table | Define a new table with typed, constrained columns |
| Insert | Add a new row |
| Select | Query rows, with optional filtering |
| Update | Modify existing rows matching a condition |
| Delete | Remove rows matching a condition |
| Count | Count matching rows |
| Show Tables | List all tables in the database |
| Table Info | Inspect a table's schema |
| Drop Table | Delete an entire table |
| Truncate | Clear all rows from a table |

---

## Architecture

```
                 ┌───────────────────────┐
                 │         User          │
                 │  (natural language)   │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │     AI Interpreter     │
                 │     (OpenAI GPT)       │
                 └───────────┬───────────┘
                             │  structured JSON
                             ▼
                 ┌───────────────────────┐
                 │    Command Dataclass   │
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │   Command Executor     │
                 └───────────┬───────────┘
                             │  validated call
                             ▼
                 ┌───────────────────────┐
                 │  Custom Database Engine│
                 │  (schema · constraints)│
                 └───────────┬───────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │      JSON Storage      │
                 └───────────────────────┘
```

Each layer only knows about the one directly beneath it — the AI layer never touches storage directly, and the database engine has no knowledge that AI is involved at all. This keeps every component independently testable and replaceable.

---

## Project Structure

```
AI-Database-Assistant/
│
├── ai/
│   ├── interpreter.py       # Natural language → structured Command
│   └── prompts.py           # System prompt for the AI interpreter
│
├── backend/
│   ├── main.py               # FastAPI app exposing /chat
│   └── models.py             # Request/response schemas
│
├── cli/
│   └── main.py               # Command-line interface
│
├── core/
│   ├── database.py           # Core database engine
│   ├── executor.py           # Executes structured commands
│   ├── parser.py             # Command validation helpers
│   ├── command.py            # Command dataclass
│   └── ...
│
├── data/
│   └── mydb.json             # JSON-backed storage
│
├── app.py                    # Streamlit chatbot interface
├── requirements.txt
├── .env.example
└── README.md
```

---

## Example Commands

```text
Create a students table with id, name, and marks.
Insert a student named Alice who scored 91.
Show all students.
Show students with marks above 80.
Update Alice's marks to 95.
Delete students whose marks are below 40.
Count all records.
Show me the schema for the students table.
```

The assistant interprets each of these automatically — no query syntax required.

---

## Workflow Explanation

1. **User enters natural language** — through the CLI, API, or chat UI.
2. **Interpreter converts text into a structured command** — GPT reads the request against a strict system prompt and returns a well-defined JSON object.
3. **Executor validates the command** — checks that required fields are present before touching the database (e.g. an `update` always requires a condition).
4. **Database engine performs the requested operation** — applying schema types and constraints (primary keys, uniqueness, nullability, defaults).
5. **Results are returned to the user** — as a structured response, rendered as text or a table depending on the interface.

---

## Technologies Used

| Category | Technology |
|---|---|
| Language | Python 3.10+ |
| AI | OpenAI GPT |
| Backend API | FastAPI |
| UI | Streamlit |
| Config | python-dotenv |
| Storage | JSON |
| Architecture | Modular, layered design |

---

## Design Principles

- **Separation of concerns** — AI, execution, and storage never overlap responsibilities
- **Modular design** — each file does one job well
- **Layered architecture** — clear, one-directional data flow
- **Reusable components** — the database engine works independently of AI
- **Easy extensibility** — new commands, interfaces, or storage backends can be added without touching existing layers

---

## Current Capabilities

- Natural language CRUD operations
- AI-powered command interpretation
- Custom JSON database engine
- Modular architecture
- CLI interface
- FastAPI backend
- Streamlit interface

---

## Future Improvements

- Multi-table relationships
- Joins across tables
- Transactions
- Authentication
- Support for multiple databases
- Richer filtering (AND/OR conditions)
- Query optimization
- Vector search & embeddings
- Full web dashboard

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please keep contributions consistent with the project's layered architecture — new features should extend a single layer rather than blur responsibilities across them.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built to explore what happens when language models meet database engines.**

If this project helped you learn something, consider giving it a ⭐ — and feel free to open an issue or PR with ideas, fixes, or improvements.

</div>