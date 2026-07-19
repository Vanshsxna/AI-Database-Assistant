# Mini Database Engine

A modular JSON-based database engine built entirely in Python without using any external database libraries.

This project implements a lightweight database system with support for table creation, CRUD operations, schema validation, constraints, and persistent JSON storage.

---

## Features

- Create and drop tables
- Insert records
- Select records
- Conditional queries (WHERE)
- Update records
- Delete records
- Count records
- Table schema inspection
- JSON-based persistent storage
- Data type validation
- Primary Key support
- Unique constraint
- Not Null constraint
- Default values
- Modular architecture

---

## Project Structure

```
AI_database_assistant/
│
├── core/
│   ├── database.py
│   ├── storage.py
│   ├── schema.py
│   ├── validator.py
│   └── constraints.py
│
├── data/
│   └── mydb.json
│
├── main.py
└── README.md
```

---

## Supported Commands

### Create a table

```text
CREATE students id:int:pk name:str:notnull age:int marks:float email:str:unique
```

### Insert a row

```text
INSERT students id=1 name=Vansh age=21 marks=95 email=vansh@gmail.com
```

### Select all rows

```text
SELECT students
```

### Select with condition

```text
SELECT students WHERE marks > 80
```

### Update records

```text
UPDATE students marks=98 WHERE id == 1
```

### Delete records

```text
DELETE students WHERE marks < 40
```

### Count records

```text
COUNT students
```

---

## Technologies Used

- Python
- JSON
- Object-Oriented Programming
- Modular Software Design

---

## Future Improvements

- SQL-like parser
- AI-powered natural language queries
- Web interface
- CSV import/export
- Aggregate functions
- Multiple condition queries
- Transactions

---

## Author

**Vansh Saxena**