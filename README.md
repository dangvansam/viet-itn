# Vietnamese Inverse Text Normalization API

A simple web API built with FastAPI and Docker to perform Inverse Text Normalization (ITN) for Vietnamese text using the `pynini` library and pre-built grammars.

## Features

*   **Inverse Text Normalization:** Converts spoken-form text to written form.
*   **REST API:** Exposes normalization via a simple `/normalize` POST endpoint.
*   **FastAPI:** Built using the modern and fast FastAPI framework.
*   **Dockerized:** Easy setup and deployment using Docker and Docker Compose.
*   **Health Check:** Includes a `/health` endpoint for monitoring.
*   **Interactive Docs:** Automatic Swagger UI documentation available at `/docs`.

## Setup and Running
1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/dangvansam/viet-itn.git
    cd viet-itn
    ```

2.  **Build and run the container using Docker Compose:**
    ```bash
    docker-compose build
    docker-compose up -d
    ```

4.  **Access the API:**
    The API will be available at `http://localhost:8000`.

## API Usage

### 1. Normalize Text

Send a POST request to the `/normalize` endpoint with a JSON payload containing the text.

**Endpoint:** `POST /normalize`

**Request Body:**

```json
{
  "text": "ngày hai mươi tháng mười một năm hai không hai ba",
}
```

Example using curl:
```bash
curl -X POST "http://localhost:8000/normalize" \
     -H "Content-Type: application/json" \
     -d '{"text": "ngày hai mươi tháng mười một năm hai không hai ba"}'
```

Example Response:

```json
{
  "normalized_text": "ngày 20 tháng 11 năm 2023"
}
```

### 2. Health Check
Send a GET request to the /health endpoint to check if the API is running.

**Endpoint:** `GET /health`
Example using curl:
```bash
curl http://localhost:8000/health
```

Example Response:
```json
{
  "status": "ok"
}
```

### 3. Interactive Documentation
FastAPI automatically generates interactive API documentation (Swagger UI). Access it in your browser:
http://localhost:8000/docs