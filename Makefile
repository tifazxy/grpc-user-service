PROTO_DIR=proto
GATEWAY_DIR=services/gateway
USER_SERVICE_DIR=services/user_service
SERVICES_DIR=services


.PHONY: proto
proto:
	python -m grpc_tools.protoc -I$(PROTO_DIR) \
	--python_out=$(SERVICES_DIR) \
	--grpc_python_out=$(SERVICES_DIR) \
	$(PROTO_DIR)/user.proto

.PHONY: run-user
run-user:
	PYTHONPATH=$(SERVICES_DIR) python $(USER_SERVICE_DIR)/server.py

.PHONY: run-gateway
run-gateway:
	PYTHONPATH=$(SERVICES_DIR) uvicorn services.gateway.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: run-all
run-all: proto run-user run-gateway