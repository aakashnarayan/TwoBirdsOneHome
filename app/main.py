from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users_db = {
    "alice": {"name": "Alice Smith", "location": "Northwest", "email": "alices2@illinois.edu"},
    "bob": {"name": "Bob Jones", "location": "Southwest", "email": "bobj2@illinois.edu"}
}

class User(BaseModel):
    name: str
    location: str
    email: str

@app.get("/user/{username}", response_model=User)
async def get_user(username: str):
    user = users_db.get(username)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/user", response_model=dict[str, dict[str, str]])
async def get_user():
    if users_db:
        return users_db
    else:
        raise HTTPException(status_code=404, detail="No users found")


@app.post("/add-user/")
async def add_user(username: str, user: User):
    #if user exists, then they need to be updated (put)
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    #add the user to the database
    users_db[username] = user.dict()
    return {"message": "User added successfully", "user": users_db[username]}

@app.put("/update-user/{username}")
async def update_user(username: str, user: User):
    #if user does not exist, then they need to be created (post)
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    #update the user in the database
    users_db[username] = user.dict()
    return {"message": "User updated successfully", "user": users_db[username]}

@app.delete("/delete-user/{username}")
async def delete_user(username: str):
    #if user does not exist, then they cannot be deleted
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    #remove the user from the database
    del users_db[username]
    return {"message": "User deleted successfully"}

@app.get("/")
def read_root():
    return {"Hello": "World"}
