# Flask User Management API

This project is a Flask-based REST API for managing users in an SQLite database. It allows for basic CRUD operations (Create, Read, Update, Delete) on a `users` table within the SQLite database.

## Features

- **Create Users**: Add new users to the database with a POST request.
- **Get Users**: Retrieve all users or a specific user by ID with a GET request.
- **Update Users**: Update existing users with PUT or PATCH requests.
- **Delete Users**: Remove a user from the database with a DELETE request.

The project is designed for learning and practice with APIs, SQLite, and testing via Postman.

---

## Endpoints

| HTTP Method | Endpoint                       | Description                           |
|-------------|--------------------------------|---------------------------------------|
| GET         | `/api/users`                   | Retrieves a list of all users         |
| GET         | `/api/users/<user_id>`         | Retrieves a specific user by ID       |
| POST        | `/api/users/add`               | Adds a new user                       |
| PUT         | `/api/users/update`            | Updates an existing user (complete update) |
| PATCH       | `/api/users/patch/<user_id>`   | Updates specific fields of a user (partial update) |
| DELETE      | `/api/users/delete/<user_id>`  | Deletes a user by ID                  |

---

## Prerequisites

- **Python 3.x**
- **Flask** and **SQLite3**
- **Postman** for API testing (or any other API testing tool)

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/flask-user-management-api.git
  ```
2. Activate the vitual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```
3.  Install Requirements
```bash
pip install Flask flask-cors db-sqlite3
```
3.  Run the server
```bash
python app.py
```

## How the API Works

### 1. Adding a User
The `POST /api/users/add` endpoint allows you to add a user. The JSON object sent in the request body should look like this:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "address": "123 Elm Street",
  "country": "USA"
}
```
The response will return the newly added user with the user_id.

### 2. Getting All Users or a Single User
- Use the `GET /api/users` endpoint to retrieve a list of all users.
- Use the `GET /api/users/<user_id>` endpoint to retrieve a specific user by their ID.

### 3. Updating a User
There are two options for updating a user:

- **PUT** (`/api/users/update`): Updates all fields of a user. You must provide all fields, even if you’re only changing a few of them.
- **PATCH** (`/api/users/patch/<user_id>`): Updates only the fields you specify in the request body.

Example of a PATCH request body:

```json
{
  "email": "newemail@example.com",
  "phone": "1112223333"
}
### 4. Deleting a User
Use the `DELETE /api/users/delete/<user_id>` endpoint to delete a user by their `user_id`.
