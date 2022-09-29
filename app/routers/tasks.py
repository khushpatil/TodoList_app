from fastapi import APIRouter, Depends, HTTPException
from .. import models,schema
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=['Tasks'])

task_complete = {"Status": "Completed"}

@router.get("/tasks", response_model=List[schema.TaskResponse])
def get_tasks(db : Session = Depends(get_db)):

    tasks = db.query(models.Task).all()
    return tasks

@router.post("/tasks", response_model=schema.TaskResponse, status_code=201)
def create_task(task: schema.Task, db : Session = Depends(get_db)):

    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/tasks/{id}", response_model=schema.TaskResponse)
def get_single_task(id: int, db : Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.Task_ID == id).first()

    if task == None:
        raise HTTPException(status_code = 404, detail="The requested task is not found")
    return task

@router.delete("/tasks/{id}", status_code=204)
def delete_task(id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.Task_ID == id)

    if not task.first():
        raise HTTPException(status_code=404, detail="The requested task doesn't exist")

    task.delete(synchronize_session=False)      
    db.commit()

    return {"message": "The resource has been deleted successfully"}

@router.put("/tasks/{id}",response_model=schema.TaskResponse, status_code=200)
def update_task(id: int, updated_task: schema.Task, db : Session = Depends(get_db)):

    task_query = db.query(models.Task).filter(models.Task.Task_ID == id)

    task = task_query.first()

    if not task:
        raise HTTPException(status_code=404, detail="The requested task does not exist")

    task_query.update(updated_task.dict(), synchronize_session=False)
    db.commit()

    return task_query.first()

@router.put("/tasks/complete/{id}",status_code=200, response_model=schema.TaskResponse)
def complete_task(id: int, db: Session = Depends(get_db)):

    task_query = db.query(models.Task).filter(models.Task.Task_ID==id)

    if not task_query.first():
        raise HTTPException(status_code=404, detail="The requested task doesn't exist")

    task_query.update(task_complete,synchronize_session=False)
    db.commit()

    return task_query.first()
    
