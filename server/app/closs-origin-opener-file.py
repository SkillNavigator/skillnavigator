from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],  # 許可するオリジンを指定
    allow_credentials=True,  # 認証情報（CookieやHTTP認証）を含めるかどうか
    allow_methods=["*"],  # 許可するHTTPメソッドを指定　GET、POST、PUT、DELETEなど。
    allow_headers=["*"],  # 許可するHTTPヘッダーを指定
    # allow_headers=["https://skill-navigator-8feca.firebaseapp.com/"],  # 許可するHTTPヘッダーを指定
)

# エンドポイントの定義
@app.get("/")
async def read_root():
    return {"message": "Hello, CORS is allowed!"}
