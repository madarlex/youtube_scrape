# YouTube Scraper API

This project is a FastAPI-based application that uses Celery and Redis to scrape data from YouTube videos. The application allows you to submit multiple YouTube video URLs and processes them asynchronously using Celery.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Getting Started

### Step 1: Input YouTube API Key

To use the YouTube API, you need to provide a valid API key. Follow these steps:

1. Open `youtube_api_key.txt` and paste your YouTube API key into the file. Make sure the key is on a single line without any extra spaces or newlines.

### Step 2: Build and Run the Application

With the API key in place, you can now build and run the Docker containers:

1. Open a terminal and navigate to the project directory.
2. Run the following command to build and start the application:

    ```bash
    docker compose up --build
    ```

    This command will build the Docker images for the FastAPI app and the Celery worker, and start the Redis container.

3. Once the containers are up and running, the FastAPI application will be available at `http://localhost:8000`.

### Step 3: Test the API

You can test the `/scrape` endpoint by sending a POST request with a JSON body containing the YouTube URLs you want to scrape.

#### Example Request

```bash
curl -X POST "http://localhost:8000/scrape" -H "Content-Type: application/json" -d '{
    "urls": ["https://www.youtube.com/watch?v=Q8rJ8yWmJkk", "https://www.youtube.com/watch?v=JtPvRA94FjY", "https://www.youtube.com/watch?v=0FtcHjI5lmw"]
}'
```

### Step 4: Test the API
Check output_db for scrape results