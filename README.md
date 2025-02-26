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

## Cloud Deploy
This section describes the steps I took to deploy the FastAPI app on Google Cloud Run while using Google Cloud Storage for persistent JSON data storage.

### 1. Set up GCP Environment
- Create a project in Google Cloud Console
- Enable required APIs
Run the following command in your terminal to enable Cloud Run, Cloud Build, Container Registry, and Cloud Storage APIs:
```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com storage.googleapis.com
```

### 2. Grant cloud bucket permission
Grant the service account the Storage Object Admin role so it can read and write to your GCS bucket. Replace `[PROJECT_ID]` with your project ID and `[service_account@developer.gserviceaccount.com]` with your service account email.
```bash
gcloud projects add-iam-policy-binding [PROJECT_ID] --member="serviceAccount:[service_account@developer.gserviceaccount.com]" --role="roles/storage.objectAdmin"
```

### 3. In the cloud console, go to *Storage* and *Create a Bucket*
- Create a bucket name (e.g. `[BUCKETNAME]`) and select us-central1 with Standard Storage
- Upload the `users.json` into the bucket

### 4. Build the Docker Image
Build the Docker image and push it to Google Container Registry. Replace `[PROJECT_ID]` with your actual Google Cloud Project ID.
```bash
gcloud builds submit --tag gcr.io/[PROJECT_ID]/fastapi-gcs
```

### 5. Deploy to Cloud Run
Deploy the container to Cloud Run using the following command. Replace `[PROJECT_ID]` with your project ID, `[service_account@developer.gserviceaccount.com]` with your service account email and `[BUCKETNAME]` with your Bucket Name. The environment variables for your GCS bucket name and object name are also set.

```bash
gcloud run deploy fastapi-gcs --image gcr.io/[PROJECT_ID]/fastapi-gcs --platform managed --region us-central1 --allow-unauthenticated --service-account=[service_account@developer.gserviceaccount.com] --set-env-vars GCS_BUCKET_NAME=[BUCKETNAME] --set-env-vars GCS_OBJECT_NAME=users.json
```

### 6. Verify Your Deployment
Once deployed, Cloud Run will provide a service URL (e.g., https://fastapi-gcs-abcdef-uc.a.run.app). To verify:
- Open the URL in your browser.
- Append /docs to access the interactive FastAPI documentation (e.g., https://- fastapi-gcs-abcdef-uc.a.run.app/docs).
- Test the endpoints to ensure the app loads data from and writes data to your GCS bucket.



## Running the Application locally on Docker
1. Download service-account-key
2. Run docker
3. Build docker image
```bash
docker build -t fastapi-gcs .
```
4. Run docker image. Replace `[BUCKETNAME]` with your bucket name and `[path\to\service-account-key.json]` with service-account-key path.
```bash
docker run -p 8000:8000 -e PORT=8000 -e GCS_BUCKET_NAME="[BUCKETNAME]" -e GCS_OBJECT_NAME="users.json" -e GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-key.json" -v [path\to\service-account-key]:/app/service-account-key.json fastapi-gcs
```