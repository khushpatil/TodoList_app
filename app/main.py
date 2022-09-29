from fastapi import HTTPException, FastAPI
from .database import engine
import pymysql  
from .routers import tasks,users,auth
import time
from . import models

hostname = "localhost"
username = "root"
my_password = "KhushP@TIL70"
my_database = "todolist"

todo_app = FastAPI()

models.Base.metadata.create_all(bind=engine)

todo_app.include_router(tasks.router)
todo_app.include_router(users.router)
todo_app.include_router(auth.router)

while True:
    try:
        mydb_conn = pymysql.connect(host = hostname, user = username, password = my_password, database = my_database)
        print("Database connection was successfull")
        break
    except Exception as e:
        print(e)
        time.sleep(2)

