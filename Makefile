PROTO_DIR=proto
GATEWAY_DIR=services/gateway
USER_SERVICE_DIR=services/user_service
SERVICES_DIR=services

.PHONY: help proto run-user run-gateway

help:
	@echo "Available commands:"
	@echo "  make proto         - Compile protobuf files"
	@echo "  make run-user      - Start gRPC user service"
	@echo "  make run-gateway   - Start FastAPI gateway"

proto:
	python -m grpc_tools.protoc -I$(PROTO_DIR) \
	--python_out=$(SERVICES_DIR) \
	--grpc_python_out=$(SERVICES_DIR) \
	$(PROTO_DIR)/user.proto

run-user:
	PYTHONPATH=$(SERVICES_DIR) python $(USER_SERVICE_DIR)/server.py

run-gateway:
	PYTHONPATH=$(SERVICES_DIR) uvicorn services.gateway.main:app --reload --host 0.0.0.0 --port 8000

