from pydantic import BaseModel
class LoginForm(BaseModel):
    username: str
    password:str

class AddUser(BaseModel):
    name:str
    email:str
    password:str

class User(BaseModel):
    id:str
    name:str
    email:str  
    password:str
    disabled:bool

def user_to_dict(u):
    return {
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "password": u.password,
        # "disabled": u.disabled
    }

def list_users_response_to_dict(resp):
    return {
        "users": [user_to_dict(u) for u in resp.users],
        "total": resp.total
    }