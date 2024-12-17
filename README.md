# Local Setup

# Clone the repository:
```bash
git clone https://github.com/Mishakivskiy/CodeAiReview
cd CodeAiReview
```

# Copy the example environment file:

Copy the .env.example file to .env to set up the environment:
```bash
cp example.env .env
```
Then specify yours envs
# Build and run with Docker Compose:

Use Docker Compose to build and run the containers:
```bash
docker compose up --build
```
This will start all the necessary services described in docker-compose.yml and create the required containers.

# Check the application:

After Docker Compose finishes building the containers, the application will be available at http://localhost:8000

# Answers
As for scaling, in my opinion, the best option is to make the main endpoint asynchronous (it returns the task ID, by which the second request can be used to get the execution status, and if the status is done, the result), the tasks themselves should be thrown into a queue (for example - AMQ), on the main instance we leave only the api, we will pick up some celery workers that will process the tasks in the order of the queue.

At the expense of optimizing resources and bypassing restrictions, we do not necessarily need to store these files for processing, and if necessary, we can use a storage such as S3, with the task of automatically cleaning outdated files, token restrictions - we can use several keys with their alternate change, also add retries with waiting for errors related to these limitations
