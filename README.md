## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Virtualenv
- Docker 

### Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/social_networking.git
    cd social_networking
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser (optional, for admin access):**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## API Documentation

### User Registration

**Endpoint:** `/signup/`

**Method:** `POST`

**Request Body:**

```json
{
    "email": "user@example.com",
    "password": "password123",
    "name": "User Name"
}
```
**Response (201 Created):**
```json
{
    "token": "user-token"
}
```
### User Login

**Endpoint:** `/login/`

**Method:** `POST`

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```
**Response (200 Ok):**
```json
{
    "token": "user-token"
}
```
### User Search

**Endpoint:** `/search/?q=<keyword>`

**Method:** `GET`
**Headers:**
```sql
Authorization: Token <user-token>
```
**Response (200 Ok):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "User@example.com",
        }
    ]
}

```
### Send Friend Request

**Endpoint:** `/friend-request/send/<to_user_id>/`

**Method:** `POST`
**Headers:**
```sql
Authorization: Token <user-token>
```
**Response (201 Created):**
```json
{
    "success": "Friend request sent."
}

```
**Response (429 Too Many Requests):**
```json
{
    "error": "You can only send 3 friend requests per minute."
}

```
### Respond to Friend Request

**Endpoint:** `/friend-request/respond/<request_id>/<response>/`

**Method:** `POST`
**Headers:**
```sql
Authorization: Token <user-token>
```
**Response (200 Ok):**
```json
{
    "success": "Friend request accepted."
}
```
**Response (404 Not Found):**
```json
{
    "error": "Friend request not found."
}
```
**Response (400 Bad Request):**
```json
{
    "error": "Invalid response."
}
```
### List Friends

**Endpoint:** `/friends/`

**Method:** `GET`

**Request Body:**
```sql
Authorization: Token <user-token>
```
**Response (200 Ok):**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "email": "friend1@example.com",
            "name": "Friend One"
        },
        {
            "id": 3,
            "email": "friend2@example.com",
            "name": "Friend Two"
        }
    ]
}
```

### List Pending Friend Requests

**Endpoint:** `/friend-requests/pending/`

**Method:** `GET`

**Request Body:**
```sql
Authorization: Token <user-token>
```
**Response (200 Ok):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "from_user": {
                "id": 2,
                "email": "requester@example.com",
                "name": "Requester"
            },
            "to_user": {
                "id": 1,
                "email": "currentuser@example.com",
                "name": "Current User"
            },
            "status": "pending",
            "created_at": "2024-06-09T11:49:49.123456Z"
        }
    ]
}
```
## Docker Deployment

To deploy the application using Docker, follow these steps:

1. Build the Docker image:
```sh 
docker build -t social_networking .
```
2. Run the Docker container:
```sh
docker run -d -p 8000:8000 social_networking
```
3. Access the application:

Open your web browser and go to http://localhost:8000.