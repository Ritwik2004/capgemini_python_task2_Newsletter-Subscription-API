# Newsletter Subscription API

A full-stack web application built with **Flask** and **MySQL** that allows users to subscribe, unsubscribe, and manage their newsletter email subscriptions through a clean browser interface.

---

## Project Structure

```
FLASK 2/
├── templates/
│   └── index.html       # Frontend UI (HTML, CSS, JavaScript)
├── .env                 # Environment variables (not committed to git)
├── .gitignore           # Git ignore rules
├── app.py               # Main Flask application & API routes
├── database.sql         # SQL schema for the database
└── requirements.txt     # Python dependencies
```

---

## Features

- Subscribe with a valid email address
- View all current subscribers
- Update an existing subscriber's email
- Unsubscribe / delete an email
- Email format validation (server-side)
- Duplicate email prevention (unique constraint)
- RESTful API design

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python, Flask           |
| Database   | MySQL                   |
| Frontend   | HTML, CSS, JavaScript   |
| Config     | python-dotenv           |

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

### 5. Set up the database

Run the SQL schema file in your MySQL client:

```bash
mysql -u your_mysql_username -p your_database_name < database.sql
```

Or manually create the table:

```sql
CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);
```

### 6. Run the application

```bash
python app.py
```

The app will be available at: **http://127.0.0.1:5000**

---

## 🔌 API Endpoints

| Method   | Endpoint          | Description                        |
|----------|-------------------|------------------------------------|
| `GET`    | `/`               | Serves the frontend HTML page      |
| `POST`   | `/subscribe`      | Add a new subscriber               |
| `GET`    | `/subscribers`    | Get all subscribers                |
| `PUT`    | `/updateEmail`    | Update an existing subscriber's email |
| `DELETE` | `/unsubscribe`    | Remove a subscriber                |

### Request & Response Examples

#### `POST /subscribe`
```json
// Request body
{ "email": "user@example.com" }

// Success (201)
{ "message": "add to database successfully" }

// Error (400)
{ "error": "The email already exist" }
```

#### `PUT /updateEmail`
```json
// Request body
{ "oldEmail": "old@example.com", "newEmail": "new@example.com" }

// Success (200)
{ "message": "Email updated successfully" }

// Error (404)
{ "message": "Old email not found" }
```

#### `DELETE /unsubscribe`
```json
// Request body
{ "email": "user@example.com" }

// Success (200)
{ "message": "Unsubscribed successfully" }
```

#### `GET /subscribers`
```json
// Success (200)
[
  { "email": "user1@example.com" },
  { "email": "user2@example.com" }
]
```

---

## Environment Variables

| Variable      | Description                    |
|---------------|--------------------------------|
| `DB_HOST`     | MySQL host (e.g., `localhost`) |
| `DB_USER`     | MySQL username                 |
| `DB_PASSWORD` | MySQL password                 |
| `DB_NAME`     | MySQL database name            |

> **Never commit your `.env` file to version control.**

---

## License

This project is open-source and available under the [MIT License](LICENSE).
