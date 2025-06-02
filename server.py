import grpc
from concurrent import futures
import time
import uuid

import user_pb2
import user_pb2_grpc

# Inmemory store
class UserStore:
    def __init__(self):
        self.users = {}

    def add_user(self, name, email):
        if any(u.email == email for u in self.users.values()):
            raise ValueError("Email already exists")
        user_id = str(uuid.uuid4())
        user = user_pb2.User(id = user_id, name = name, email = email)
        self.users[user_id] = user
        return user
    
    def update_user(self, user_id, name, email):
        if user_id not in self.users:
            return None
        user = self.users.get(user_id)
        user.name = name
        user.email = email
        self.users[user_id] = user
        return user
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def list_users(self):
        return list(self.users.values())
    
    def delete_user(self, user_id):
        return self.users.pop(user_id, None) is not None
    
# gRPC implementation
class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, store):
        self.store = store

    def CreateUser(self, request, context):
        try:    
            user = self.store.add_user(request.name, request.email)
            return user_pb2.CreateUserResponse(user=user)
        except ValueError as e:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(str(e))
            return user_pb2.CreateUserResponse()
        
    def UpdateUser(self, request, context):
        user = self.store.update_user(request.id, request.name, request.email)
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.UpdateUserResponse()
        return user_pb2.UpdateUserResponse(user=user)
    
    def GetUser(self, request, context):
        user = self.store.get_user(request.id)
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_pb2.GetUserResponse()
        return user_pb2.GetUserResponse(user=user)
    
    def ListUsers(self, request, context):
        users = self.store.list_users()
        return user_pb2.ListUsersResponse(users=users)
    
    def DeleteUser(self, request, context):
        success = self.store.delete_user(request.id)
        return user_pb2.DeleteUserResponse(success=success)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_store = UserStore()
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(user_store), server)

    server.add_insecure_port('[::]:50051')
    print("Starting server on port 50051...")

    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping server")
        server.stop(0)

if __name__ == '__main__':
    serve()