from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


app = FastAPI()

# @app.get("/")
# async def read_root():
#     logging.info("ルートエンドポイントが呼ばれました")
#     return {"Hello": "World"}


# @app.get("/")
# def read_root():
#     return {"こんにちは": "Hello"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンからのリクエストを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)


class User(BaseModel):
    uid: str
    user_name: str

@app.post("/create_user")
def create_user(user: User):
    logging.info("create_user関数が呼ばれました")



    database_url = os.environ.get("DATABASE_URL", "postgresql://postgres:password@db:5432/postgres")
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (uid, user_name) VALUES (%s, %s)",
                    (user.uid, user.user_name))
        conn.commit()
    except Exception as e:
        logging.info("呼ばれました")
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

    return {"message": "User created successfully"}