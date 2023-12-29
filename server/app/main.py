from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"こんにちは": "Hello"}


class User(BaseModel):
    uid: str
    username: str

@app.post("/create_user")
def create_user(user: User):
    database_url = os.environ.get("DATABASE_URL", "postgresql://default:password@localhost/dbname")
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (uid, username) VALUES (%s, %s)",
                    (user.uid, user.username))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return {"message": "User created successfully"}