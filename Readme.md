# Role-Based Authentication App with Flask & JavaScript

A full-stack web application demonstrating a secure, role-based user authentication system. The backend is built with Python/Flask and uses JSON Web Tokens (JWT) for securing API endpoints, while the frontend is a dynamic single-page application powered by vanilla JavaScript.

---

## Features

-   🔐 **Secure User Authentication**: User registration and login functionality.
-   🔑 **JWT Session Management**: Uses Flask-JWT-Extended to manage user sessions with secure access tokens.
-   👤 **Role-Based Access Control (RBAC)**: Distinguishes between `admin` and `student` roles, restricting access to certain features based on user permissions.
-   🛠️ **Admin Dashboard**: A protected dashboard for administrators to perform CRUD (Create, Read, Delete) operations on users.
-   🚀 **RESTful API**: A clean API built with Flask-RESTful.
-   📄 **Single-Page Application (SPA)**: The frontend provides a smooth user experience by dynamically rendering content without page reloads.

## Tech Stack

-   **Backend**: Python, Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-JWT-Extended
-   **Database**: SQLite
-   **Frontend**: HTML, CSS, Vanilla JavaScript

## Setup and Installation

Follow these steps to get the project running on your local machine.

**1. Clone the repository:**
```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
```

**2. Create and activate a virtual environment:**
* **On macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
* **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the Flask application:**
```bash
python app.py
```
The application will start on `http://127.0.0.1:5000`. Open this URL in your web browser.

## How to Use

-   Navigate to `http://127.0.0.1:5000` in your browser.
-   You can register a new user (who will have the `student` role by default).
-   To access the admin dashboard, log in with the default administrator credentials:
    -   **Username**: `admin`
    -   **Password**: `admin123`
-   As an admin, you can view all users, create new users (with either `admin` or `student` roles), and delete existing users.

## API Endpoints

| Method   | Endpoint              | Description                               | Access       |
| -------- | --------------------- | ----------------------------------------- | ------------ |
| `POST`   | `/register`           | Registers a new user (as a student).      | Public       |
| `POST`   | `/login`              | Authenticates a user and returns a JWT.   | Public       |
| `GET`    | `/users`              | Gets a list of all users.                 | Admin Only   |
| `POST`   | `/create-user`        | Creates a new user with a specific role.  | Admin Only   |
| `DELETE` | `/users/<int:user_id>` | Deletes a specific user.                  | Admin Only   |
| `POST`   | `/change-password`    | Allows a logged-in user to change their password. | Authenticated User |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.