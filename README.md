# Vendor Management System

This is a Django application for managing vendors and purchase orders.

## Features

- Allows creating, updating, and deleting vendors.
- Tracks vendor performance.
- Manages purchase orders.
- Supports authentication using JWT tokens.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/howdyrahuldev/VendorManagementSystem.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd VendorManagementSystem
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

## Authentication Setup

This project uses JWT (JSON Web Tokens) for authentication. To access the APIs, you need to obtain a token by sending a POST request to the token endpoint with valid credentials.

**Example request:**

```http
POST /api/token/ HTTP/1.1
Host: yourdomain.com
Content-Type: application/json

{
    "username": "yourusername",
    "password": "yourpassword"
}
```

**Example response:**

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

To access protected endpoints, include the token in the Authorization header as follows:

```http
GET /api/vendors/ HTTP/1.1
Host: yourdomain.com
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## Testing

This project includes unit tests to ensure the correctness of API endpoints. To run the tests, execute the following command:

```bash
python manage.py test
```

The tests cover various scenarios, including creating, updating, and deleting vendors, managing purchase orders, and authenticating users.
