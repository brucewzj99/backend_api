# Backend API

This is a Python FastAPI application with 3 endpoints written for `Backend Take Home Assignment`

1. **Get users** (by a list of IDs)
2. **Add users**
3. **Delete users**

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/backend_api.git
    cd backend_api
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to see the interactive API documentation.

## Usage
### 1. Get an Object Based on a List of IDs
- **Method**: `POST`
- **Path**: `/users/get_users`
- **Body (JSON)**: An array of objects, each containing an `id`:
```json
    [
        {"id": 1},
        {"id": 2}
    ]
```
- **Response**: Returns a list of user objects that match any provided IDs.


### 2. Add a New User
- **Method**: `POST`
- **Path**: `/users/`
- **Body (JSON)**:
```json
    {
    "name": "Test User",
    "email": "testuser@gmail.com",
    "contact_number": "99887766"
    }
```
- `name` (string)
- `email` (string, optional)
- `contact_number` (string, optional)
- Must provide at least one contact method (`email` or `contact number`)
- **Response**: Returns a JSON object of the newly created user (including an auto-generated `id`).


### 3. Delete a User by ID
- **Method**: `DELETE`
- **Path**: `/users/{user_id}`
- **Response**: Returns a success message if the user was found and deleted; otherwise a 404 error.

## Running Tests
```
pytest
```
This will run all the tests in the `test/` directory.