# Task Management API (with LLaMa3.2-medieval SFT)

A RESTful API for managing tasks built with FastAPI, PostgreSQL, and Redis. With RAG capabilities using multiple PDF and EPUB files as knowledge base. To make the assignment a bit more unique, I fine-tuned the LLaMa 3.2-instruct model (see: https://huggingface.co/madks/llama-3.2-3b-medieval-arms-and-armor/tree/main) with a questions-answers knowledgebase (that I created from 8 books, see: https://huggingface.co/datasets/madks/medieval-qa-dataset) on medieval arms and armor (like swords, crossbows, chainmail, ...).

## Features

- Create, read, update, and delete tasks
- Task properties include title, description, status, creation time, and update time
- Redis caching for improved performance
- Fine-tuned LLaMa 3.2 with knowledge on Medieval arms and armor (from free books acquired from project Gutenberg).
- RAG (Retrieval Augmented Generation) using multiple PDF and EPUB files as knowledge base
- Containerized with Docker and Docker Compose

## API Endpoints

- `GET /tasks` - Retrieve all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Retrieve a specific task by ID
- `PUT /tasks/{id}` - Update an existing task
- `DELETE /tasks/{id}` - Delete a task
- `GET /tasks/{id}/summary` - Get AI-generated summary of a task
- `GET /tasks/{id}/knowledge/hints` - Get AI-generated hints for a task
- `POST /query` - Query the fine-tuned LLaMa 3.2-medieval model
- `POST /knowledge/query` - Query the fine-tuned LLaMa 3.2-medieval model with the knowledge base (PDF and EPUB files)
- `GET /knowledge/documents` - View all the contents of parsed PDF and EPUB files

## Running the Application

### Prerequisites

- Docker and Docker Compose installed on your system
- Ollama running locally with llama3.2-medieval model installed

### Steps to Run

1. Clone this repository
2. Navigate to the project directory
3. Create a `data` directory in the project root if it doesn't exist:
   ```bash
   mkdir -p data
   ```
4. Place your PDF and/or EPUB files in the `data` directory. The application will automatically load all supported files from this directory.
5. Run the following command to start the application:
   ```bash
   docker-compose up -d
   ```
6. The API will be available at http://localhost:8000
7. Access the API documentation at http://localhost:8000/docs

## Knowledge Base Management

The application automatically loads all PDF and EPUB files from the `data` directory into its knowledge base. To update the knowledge base:

1. Add or remove PDF/EPUB files in the `data` directory
2. Restart the application:
   ```bash
   docker-compose restart api
   ```

## API Usage Examples

### View All Document Contents

```bash
curl -X 'GET' 'http://localhost:8000/knowledge/documents'
```

### Query Knowledge Base

```bash
curl -X 'POST' \
  'http://localhost:8000/knowledge/query' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "What is the best sword type for duelling?"
}'
```

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
- **LangChain**: Framework for building LLM applications
- **FAISS**: Vector store for efficient similarity search
- **Ollama**: Local LLM integration 