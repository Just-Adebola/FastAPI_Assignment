from fastapi import FastAPI, status, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
import time


app = FastAPI()


@app.middleware("http")
async def process_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    end_time = time.perf_counter()
    duration = end_time - start_time
    # process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(duration)
    print(duration)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UsersModel(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    height: float

class User(UsersModel):
    id: int

my_users = []



@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_users(
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    age: Annotated[int, Form()],
    email: Annotated[str, Form()],
    height: Annotated[float, Form()]
):
    id = len(my_users) + 1
    new_user = User(
        id = id,
        first_name = first_name,
        last_name = last_name,
        age = age,
        email = email,
        height = height
        
    )
    my_users.append(new_user)
    return {"Message": "Successfully created."}