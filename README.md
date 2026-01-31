# sauth

Simple auth service on FastAPI

## Requirements

- Docker & Docker Compose
- Make

## Setup

1. Copy the example env file and edit it for your environment:
   ```bash
   cp env_example .env
   ```
2. Adjust variables in `.env` as needed

## Run

| Command       | Description                    |
|---------------|--------------------------------|
| `make run`    | Start services (detached)      |
| `make down`   | Stop services                  |
| `make destroy`| Stop and remove volumes        |
| `make rebuild`| Destroy, then build and start  |
| `make update` | `git pull` then rebuild & start|
