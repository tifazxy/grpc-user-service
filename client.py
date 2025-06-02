import grpc
import user_pb2
import user_pb2_grpc

def run():
    # build connection
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel=channel)

    # Create a user
    print("Creating user...")
    create_response = stub.CreateUser(user_pb2.CreateUserRequest(name='Alice', email="alice@example.com"))
    user_id = create_response.user.id
    print('User created:', create_response.user)

    print("\nGetting user...")
    get_response = stub.GetUser(user_pb2.GetUserRequest(id=user_id))
    print("User retrieved:", get_response.user)

    print("\nListing users...")
    list_response = stub.ListUsers(user_pb2.ListUsersRequest())
    for user in list_response.users:
        print(user)

if __name__=='__main__':
    run()