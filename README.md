# Contact Book API (FastAPI + SQLite)

A backend application to manage personal contacts, built using FastAPI, SQLite, and SQLAlchemy. The project follows a clean, layered architecture with proper validation, structured responses, and error handling.

---

## Features

* Create a new contact
* Search contacts by name, phone, or email (partial match supported)
* Delete a contact
* Merge two contacts into one (combine non-null fields and remove duplicates)
* Structured API responses using `success_response` and `error_response`
* Input validation using Pydantic

---

## Project Structure

```
│── core/            # Database configuration
│── models/          # ORM models and Pydantic schemas
│── router/          # API routes
│── services/        # Business logic layer
│── utils/           # Helper functions (response wrapper)
│── main.py          # Application entry point
│── requirements.txt
│── README.md
```

---

## Tech Stack

* FastAPI
* SQLite
* SQLAlchemy
* Pydantic

---

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Linux/Mac
   venv\Scripts\activate         # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

5. Access API documentation:

   ```
   http://127.0.0.1:8000/docs
   ```

---

## API Endpoints

### Create Contact

**POST** `/contacts/`

Request Body:

```json
{
  "name": "Suhas",
  "phone": "9876543210",
  "email": "suhas@example.com"
}
```

---

### Search Contacts

**GET** `/contacts/search?q=value`

Example:

```
/contacts/search?q=suhas
```

---

### Delete Contact

**DELETE** `/contacts/{contact_id}`

---

### Merge Contacts

**PUT** `/contacts/merge?id1=1&id2=2`

Description:

* Combines two contacts into one
* Keeps non-null values
* Deletes the second contact

---

## Validation Rules

* At least one field (name, phone, email) must be provided
* Name must be between 2 and 100 characters
* Phone must be a valid 10-digit number
* Email must be a valid email format

---

## Response Format

### Success Response

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {}
}
```

### Error Response

```json
{
  "success": false,
  "message": "Error message",
  "data": null
}
```

---

## Design Decisions

* Layered architecture (router → service → model) for separation of concerns
* SQLite used for simplicity and quick setup
* SQLAlchemy ORM for database interactions
* Pydantic for validation and data serialization
* Custom response wrapper for consistent API responses

---

## Improvements for Production Deployment

If deployed as a scalable web application, the following changes would be made:

* Replace SQLite with PostgreSQL for better concurrency
* Add authentication (JWT-based user system)
* Use Redis for caching frequently accessed data
* Implement logging and monitoring (Prometheus, Grafana)
* Add rate limiting and security best practices (HTTPS, input sanitization)

---

## Author

Suhas
Python Full Stack Developer
