from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users_db = {
    "alice": {"name": "Alice Smith", "location": "Northwest", "email": "alices2@illinois.edu"},
    "bob": {"name": "Bob Jones", "location": "Southwest", "email": "bobj2@illinois.edu"}
}

class UserResponse(BaseModel):
    name: str
    location: str
    email: str

@app.get("/user/{username}", response_model=UserResponse)
def get_user(username: str):
    user = users_db.get(username)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/")
def read_root():
    return {"Hello": "World"}
