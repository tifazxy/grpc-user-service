from fastapi import FastAPI, HTTPException, Depends, status
from services.gateway import client
from typing import Annotated
from services.gateway.auth import(
    authenticate_user,
    get_password_hash,
    create_access_token,
    get_current_user,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta
from services.gateway import utils
from fastapi.security import OAuth2PasswordRequestForm
from pathlib import Path
import logging.config
import json

def initialize_logging(config_filename: str = 'logging_config.json'):
    """load json logging configuration"""
    current_file_path = Path(__file__).resolve() # using absolute path to find the file
    current_dir = current_file_path.parent
    config_path = current_dir.parent / config_filename

    if Path(config_path).exists():
        with open(config_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config=config)

        global logger
        logger = logging.getLogger("app_logger")
        logger.info("Logging initialize succeed!")
    else:
        # no config file the logging should work at least
        logging.basicConfig(level=logging.WARNING)
        print(f"warning:cannot find the logging configuration file in path {config_path}")


initialize_logging()
app = FastAPI()


@app.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password) # TODO this username is actually email
    logger.info(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token = create_access_token(
        data={'sub': user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token":access_token, "token_type":"bearer"}


@app.get("/me", response_model=dict)
async def read_users_me(current_user: Annotated[dict, Depends(get_current_user)]):
    logger.info("read_users_me:",current_user)
    return current_user

@app.post("/users/add")
async def add_user(user: utils.AddUser):
    try:
        resp_id = client.createUser(user.name, user.email, get_password_hash(user.password))
        return{
            "message": "Success",
            "ID":resp_id
        }
    except ConnectionError as e:
        raise HTTPException(500, detail=str(e))

@app.get("/users/list")
async def list_user(current_user: Annotated[dict, Depends(get_current_user)], skip:int = 0, limit:int = 10):
    try:
        resp = client.listUser(skip=skip, limit=limit)
        return utils.list_users_response_to_dict(resp=resp)
    except ConnectionError as e:
        raise HTTPException(500, detail=str(e))

@app.get("/test")
async def test():
    return {
        "message": "Hello!"
    }

# Because *path operations* are evaluated in order, you need to make sure that the path for `/users/me` 
# is declared before the one for `/users/{user_id}`
# Otherwise, the path for `/users/{user_id}` would match also for `/users/me`, 
# "thinking" that it's receiving a parameter `user_id` with a value of `"me"`
@app.get("/users/{user_id}")
async def get_user(current_user: Annotated[dict, Depends(get_current_user)], user_id: str):
    try:
        user_resp = client.getUser(user_id)
        return utils.user_to_dict(user_resp)
    except ConnectionError as e:
        raise HTTPException(status_code=500, detail=str(e))