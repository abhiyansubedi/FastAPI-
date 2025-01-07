from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from database import SessionLocal
import models


app = FastAPI()


class OurBaseModel(BaseModel):
    class Config:
        orm_mode =True


class TodoCreate(OurBaseModel) :
   
    name:str
    description:str
    done:bool

class Todo(TodoCreate):
    id: int  # For responses, we include the id field


db= SessionLocal()


@app.get('/todo', response_model = list[Todo],status_code=status.HTTP_200_OK)
def getAll_Todos():
    getAllTodos = db.query(models.Todo).all()
    return getAllTodos

@app.get('/todo/{todo_id}', response_model = Todo, status_code = status.HTTP_200_OK)
def getTodo_Id(todo_id:int, todo:Todo):
    find_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if find_todo is not None:
 
     return find_todo
    
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Todo is not found")






@app.post('/todo/add', response_model = Todo,status_code=status.HTTP_201_CREATED)
def add_Todo(todo:TodoCreate):
    
    newTodo = models.Todo(
        name = todo.name,
        description = todo.description,
        done = todo.done
    )

    db.add(newTodo)
    db.commit()
    db.refresh(newTodo)

    return newTodo


@app.put('/todo/update/{todo_id}',response_model= Todo,status_code =status.HTTP_202_ACCEPTED)
def updateTodo(todo_id:int, todo:Todo):
    find_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if find_todo is not None:
        find_todo.id = todo.id
        find_todo.name = todo.name
        find_todo.description = todo.description
        find_todo.done = todo.done

        db.commit()
        return find_todo
    

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Todo is not found")
    

@app.delete('/todo/{todo_id}', response_model=list[Todo],status_code=200)
def deletetodo(todo_id:int):
    find_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if find_todo is not None:
        db.delete(find_todo)
        getAllTodos = db.query(models.Todo).all()
        return getAllTodos
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Todo is not found")

# @app.get('/todo', status_code=200)
# def getTodo():
#     return {"message": "server is running"}


# @app.get('/todo/{todo_id}', status_code=200)
# def getTodo_By_Id(todo_id:int):
#     return {"message":f"Your Todo Id is {todo_id}"}


# @app.post('/todo/add',status_code=200)
# def posttodo(todo: Todo):
#     return {
#         "id" :todo.id,
#         "name":todo.name,
#         "description": todo.description,
#         "done" : todo.done
    # }

