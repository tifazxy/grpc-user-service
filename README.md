# Backend Architecture Project – FastAPI & gRPC (Python)

This project demonstrates a modular microservices backend architecture using FastAPI and gRPC, written in Python. It includes a user management service with authentication, persistent storage, and service orchestration.

## Features
- gRPC service defined with Protocol Buffers
- Python implementation for both gRPC server and client
- PostgreSQL-backed data store (and pluggable in-memory store for testing)
- FastAPI gateway to expose RESTful APIs and aggregate service calls
- OAuth2 + JWT-based authentication for secure access
- Extensible design for future services (e.g., assets, stats, etc.)

## Work In Progress

These features are being actively developed and will be included in the next version:

- Dockerized Setup: Dockerfile and Docker Compose to manage services and PostgreSQL.
- CI/CD with Jenkins: Automating build, test, and deploy pipelines using Jenkins.
- Testing Suite: Unit and integration tests for gRPC services and FastAPI gateway.
- Structured Logging: Add consistent log formats across services for observability.

## Setup
### 1. Clone the repo

```bash
git clone [url]
cd grpc-user-service
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
#### Install FastAPI gateway dependencies
```bash
pip install -r services/gateway/requirements.txt
```
#### Install user service dependencies
```bash
pip install -r services/user_service/requirements.txt
```
### 4. Add `.env` File
```bash
touch services/.env
```
#### Edit the file with the following content:
```bash
SECRET_KEY = '[secret_key]'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_URL = "postgresql://[username]:[password]@[db_ip]/[db_name]"
```
### 5. Create db tables
Ensure the ownership is updated:
```sql
ALTER TABLE public.users OWNER TO [your_db_user];
```
Then load the schema:
```sql
psql -U <username> -d <your_db_name> -f docs/schema.sql
```
## Generate gRPC Code
```bash
make proto
```
This generates:
- services/user_pb2.py
- services/user_pb2_grpc.py

## Run the Server
```bash
make run-user
```

## Open another terminal and Run the Gateway
```bash
make run-gateway
```

## Test via API Docs
Once the gateway is running:
Open your browser and go to:
```bash
http://localhost:8000/docs
```
![alt text](homepage.png?raw=true "API Docs")