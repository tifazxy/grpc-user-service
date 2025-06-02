# gRPC User Service (Python)

This project is a basic gRPC microservice in Python that manages user data. It supports creating, fetching, listing, updating, and deleting users.


- Define gRPC service using Protocol Buffers
- Python server and client implementation
- In-memory store (easily swappable with PostgreSQL/SQLite)

## Setup
### 1. Clone the repo

```bash
git clone [url]
cd grpc-user-service
```

### 2. Create virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
## Generate gRPC Code
```bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/user.proto
```
This generates:
- user_pb2.py
- user_pb2_grpc.py

## Run the Server
```bash
python server.py
```

## Open another terminal and Run the Client
```bash
python client.py
```
Expected output:
```bash
Creating user...
User created: id: "..."
name: "Alice"
email: "alice@example.com"


Getting user...
User retrieved: id: "..."
name: "Alice"
email: "alice@example.com"


Listing users...
id: "..."
name: "Alice"
email: "alice@example.com"
```

