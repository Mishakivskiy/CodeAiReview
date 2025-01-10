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

