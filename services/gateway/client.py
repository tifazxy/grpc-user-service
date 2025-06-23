import grpc
import user_pb2, user_pb2_grpc

def getUser(user_id):
    # build connection
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)

            print("\nGetting user...")
            req = user_pb2.GetUserRequest(id = user_id)
            resp = stub.GetUser(req)
            return  resp.user
    except grpc.RpcError as e:
        raise ConnectionError(status_code=500, detail=str(e))

def getUserbyEmail(email):
    # build connection
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)

            print("\nGetting user by email...")
            req = user_pb2.GetUserRequest(email = email)
            resp = stub.GetUserbyEmail(req)
            return  resp.user
    except grpc.RpcError as e:
        raise ConnectionError(status_code=500, detail=str(e))

def createUser(name:str, email:str, password:str):
    # build connection
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            print("Creating user...")
            create_response = stub.CreateUser(user_pb2.CreateUserRequest(name=name, email=email, password=password))
            return  create_response.user.id
    except grpc.RpcError as e:
        raise ConnectionError(status_code=500, detail=str(e))

def listUser(skip:int, limit:int):
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)

            print("\nListing users...")
            list_response = stub.ListUsers(user_pb2.ListUsersRequest(skip=skip, limit=limit))
            return list_response
    except grpc.RpcError as e:
        raise ConnectionError(status_code=500, detail=str(e))


# if __name__=='__main__':
#     run()