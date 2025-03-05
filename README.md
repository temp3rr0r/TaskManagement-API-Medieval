# Task Management API

A RESTful API for managing tasks built with FastAPI, PostgreSQL, and Redis.

## Features

- Create, read, update, and delete tasks
- Task properties include title, description, status, creation time, and update time
- Redis caching for improved performance
- Containerized with Docker and Docker Compose

## API Endpoints

- `POST /tasks` - Create a new task
- `GET /tasks` - Retrieve all tasks
- `GET /tasks/{id}` - Retrieve a specific task by ID
- `PUT /tasks/{id}` - Update an existing task
- `DELETE /tasks/{id}` - Delete a task

## Running the Application

### Prerequisites

- Docker and Docker Compose installed on your system

### Steps to Run

1. Clone this repository
2. Navigate to the project directory
3. Run the following command to start the application:

```bash
docker-compose up -d
```

4. The API will be available at http://localhost:8000
5. Access the API documentation at http://localhost:8000/docs

## API Usage Examples

### Create a Task

```bash
curl -X 'POST' \
  'http://localhost:8000/tasks' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Complete project",
  "description": "Finish the task management API project"
}'
```

### Get All Tasks

```bash
curl -X 'GET' 'http://localhost:8000/tasks'
```

### Get a Specific Task

```bash
curl -X 'GET' 'http://localhost:8000/tasks/1'
```

### Update a Task

```bash
curl -X 'PUT' \
  'http://localhost:8000/tasks/1' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "In Progress"
}'
```

### Delete a Task

```bash
curl -X 'DELETE' 'http://localhost:8000/tasks/1'
```

## Architecture

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Relational database for storing task data
- **Redis**: In-memory data store used for caching
- **Docker**: Containerization for easy deployment
- **SQLAlchemy**: SQL toolkit and ORM for database interactions
- **Pydantic**: Data validation and settings management 