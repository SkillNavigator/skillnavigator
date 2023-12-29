# import uvicorn
# from fastapi import FastAPI, HTTPException, Depends
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Dict, List
# from pydantic import BaseModel, ValidationError, validator , root_validator#LLM用　
# from sqlalchemy.orm import Session
# from .models import LLMAnswer, UserSetting, CourseDetail, User, Base# models.py からのモデルのインポート
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from sqlalchemy.orm import sessionmaker
# import openai
# import os
# import datetime
# import httpx #LLM用
# from langchain.llms import OpenAI
# from langchain import PromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain import LLMChain
# from langchain.chains import LLMChain # LLM チェーンをインポート

# # 環境変数からデータベースURLを取得
# DATABASE_URL = os.environ.get("DATABASE_URL")
# # SQLAlchemyエンジンを作成
# engine = create_engine(DATABASE_URL)
# # データベーステーブルを作成
# # Base.metadata.create_all(bind=engine)
# # connection = engine.connect()
# # セッションファクトリーを作成
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # FastAPIアプリケーションが初期化
# app = FastAPI()

# # 環境変数を読み込む
# load_dotenv()  
# #OpenAIのAPIキーを環境変数から取得
# openai_api_key = os.getenv("OPENAI_API_KEY") 
# #初期化　temperature揺れる回答を小さい数字で揺れなくしてる
# llm = OpenAI(model_name="text-davinci-003" , temperature=0.2)
# # 今日の日付を取得
# current_date = datetime.date.today().isoformat()  # YYYY-MM-DD形式


# # 依存性
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # CORSミドルウェアを追加・異なるオリジンからのリクエストを許可
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ここで許可するオリジンを指定
#     allow_credentials=True,
#     allow_methods=["*"],  # ここで許可するHTTPメソッドを指定
#     allow_headers=["*"],  # ここで許可するHTTPヘッダーを指定
# )

# # リクエストボディの構造を定義するPydanticモデルを作成します。
# class CourseDetail(BaseModel):
#     course_level: str # コースレベル
#     duration: float # そのレベルを終えるのに必要な時間

# class UserSetting(BaseModel):
#     user_setting_id: int
#     current_date: str # 現在の日付
#     target_period: str #(３ヶ月・６ヶ月)
#     monday_study_time:float
#     tuesday_study_time: float
#     wednesday_study_time: float
#     thursday_study_time: float
#     friday_study_time: float
#     saturday_study_time: float
#     sunday_study_time: float
#     uid: str
#     course_details: List[CourseDetail]  # コースの詳細（複数のレベル）


# @app.post("/generate-study-plan")
# async def generate_study_plan(request_body: UserSetting):
#     prompt = PromptTemplate(
#         input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_details"],
#         template="""
#         今日は{current_date}です。私は、特定のユーザーのために{target_period}のコース期間内で完了する個別化された学習スケジュールを作成しています。
#         各レベルのコース内容と所要時間は{course_details}で、ユーザーの勉強可能時間は{monday_study_time},{tuesday_study_time},{wednesday_study_time},{thursday_study_time},{friday_study_time},{saturday_study_time},{sunday_study_time}です。
#         私のタスクは、これらの情報を基にして、各コースレベルが特定の日付に割り当てられるようなスケジュールを立案することです。スケジュールは、具体的な日付と、その日に行うべきレベルを示す形式であるべきです。各レベルの勉強が終わるごとに次のレベルに進み、全てのレベルが終了するまでの計画を立ててください。各レベルに対して実際に勉強する日程は複数ある場合があります。
#         以下のようにスケジュールを提示してください：

#         レベル0: [日付]
#         レベル1-1: [日付]
#         レベル1-2: [日付]
#         ... 以下、各レベルに対応する日付 ...

#         各レベルの所要時間とユーザーの利用可能時間を考慮し、実際に勉強が行われる日を割り当ててください。計画のスタート日は現在の日付の次の日からにしてください。
#         また、各レベル終了後には、ユーザーが予定に遅れた場合に備えてバッファー時間を秘匿的に組み込んでください。
#         """
#     )

#     # LLM チェーンを実行するための入力データをユーザーのリクエストから構築(Next.jsができたらこっちに変更)
#     input_data = {
#         "current_date": request_body.current_date,
#         "uid":request_body.uid,
#         "monday_study_time":request_body.monday_study_time,
#         "tuesday_study_time": request_body.tuesday_study_time,
#         "wednesday_study_time": request_body.wednesday_study_time,
#         "thursday_study_time": request_body.thursday_study_time,
#         "friday_study_time": request_body.friday_study_time,
#         "saturday_study_time": request_body.saturday_study_time,
#         "sunday_study_time": request_body.sunday_study_time,
#         "target_period": request_body.target_period,
#         "course_details": request_body.course_details
#     }
    
#     # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#     chain = LLMChain(llm=llm, prompt=prompt)
#     # LLM　チェーンを実行
#     prediction = chain.run(input_data)
#     print(prediction.strip())

#     llm_response = prediction.strip()
#     return llm_response




# ポストマンよう
# {
#     "user_setting_id":1,
#     "current_date": "2023-12-23T15:00:00",
#     "monday_study_time":1,
#     "tuesday_study_time": 1,
#     "wednesday_study_time": 2,
#     "thursday_study_time": 1,
#     "friday_study_time": 1,
#     "saturday_study_time": 5,
#     "sunday_study_time": 4,
#     "target_period": "3ヶ月",
    # "course_details": [
    #     {"course_level": "level0 イントロダクション・基礎学習について", "duration": 1},
    #     {"course_level": "level1-1 環境構築", "duration": 0.5},
    #     {"course_level": "level1-2 データ型・演算子・変数", "duration": 2.5},
    #     {"course_level": "level2-1 関数", "duration": 5},
    #     {"course_level": "level2-2 より良いコードを書くには？", "duration": 2},
    #     {"course_level": "level2-3 比較", "duration": 2},
    #     {"course_level": "level3-1 条件分岐①", "duration": 4},
    #     {"course_level": "level3-2 条件分岐②", "duration": 4},
    #     {"course_level": "level3-3 スコープ", "duration": 2},
    #     {"course_level": "level4-1 配列", "duration": 6},
    #     {"course_level": "level4-2 オブジェクト", "duration": 6},
    #     {"course_level": "level4-3 forループ", "duration": 10},
    #     {"course_level": "level5-1 HTML・CSSの基礎知識", "duration": 1},
    #     {"course_level": "level5-2 HTML・CSS演習（My IRページ", "duration": 14}
    # ],
#     "uid":"test-UID1234"
# }

#以下進化系

# import uvicorn
# from fastapi import FastAPI, HTTPException, Depends
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Dict, List
# from pydantic import BaseModel, ValidationError, validator , root_validator#LLM用　
# from sqlalchemy.orm import Session
# from .models import LLMAnswer, UserSetting, CourseDetail, User, Base# models.py からのモデルのインポート
# from sqlalchemy import create_engine
# from sqlalchemy import Column, Integer,String
# from sqlalchemy.orm import Session
# from sqlalchemy.orm import sessionmaker
# import openai
# import os
# import datetime
# import httpx #LLM用
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain import LLMChain
# from langchain.chains import LLMChain # LLM チェーンをインポート

# # 環境変数からデータベースURLを取得
# DATABASE_URL = os.environ.get("DATABASE_URL")
# # SQLAlchemyエンジンを作成
# engine = create_engine(DATABASE_URL)
# # データベーステーブルを作成
# # Base.metadata.create_all(bind=engine)
# # connection = engine.connect()
# # セッションファクトリーを作成
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # FastAPIアプリケーションが初期化
# app = FastAPI()

# # 環境変数を読み込む
# load_dotenv()  
# #OpenAIのAPIキーを環境変数から取得
# openai_api_key = os.getenv("OPENAI_API_KEY") 
# #初期化　temperature揺れる回答を小さい数字で揺れなくしてる
# llm = OpenAI(model_name="text-davinci-003" , temperature=0.2)
# # 今日の日付を取得
# current_date = datetime.date.today().isoformat()  # YYYY-MM-DD形式


# # 依存性
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # CORSミドルウェアを追加・異なるオリジンからのリクエストを許可
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ここで許可するオリジンを指定
#     allow_credentials=True,
#     allow_methods=["*"],  # ここで許可するHTTPメソッドを指定
#     allow_headers=["*"],  # ここで許可するHTTPヘッダーを指定
# )

# # リクエストボディの構造を定義するPydanticモデルを作成します。
# class CourseDetail(BaseModel):
#     course_level: str # コースレベル
#     duration: float # そのレベルを終えるのに必要な時間

# class UserSetting(BaseModel):
#     user_setting_id: int
#     current_date: datetime # 現在の日付
#     target_period: str #(３ヶ月・６ヶ月)
#     monday_study_time:float
#     tuesday_study_time: float
#     wednesday_study_time: float
#     thursday_study_time: float
#     friday_study_time: float
#     saturday_study_time: float
#     sunday_study_time: float
#     motivation_statement: str
#     uid: str
#     course_details: List[CourseDetail]  # コースの詳細（複数のレベル）


# @app.post("/generate-study-plan")
# async def generate_study_plan(request_body: UserSetting, db: Session = Depends(get_db)):
#     print("generate-study-plan")
#     # データベースからユーザー設定を取得
#     user_setting = db.query(UserSetting).filter(UserSetting.uid == request_body.uid).first()
#     if not user_setting:
#         raise HTTPException(status_code=404, detail="UserSetting not found")

#     prompt = PromptTemplate(
#         input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_details"],
#         template="""
#         今日は{current_date}です。私は、特定のユーザーのために{target_period}のコース期間内で完了する個別化された学習スケジュールを作成しています。
#         各レベルのコース内容と所要時間は{course_details}で、ユーザーの勉強可能時間は{monday_study_time},{tuesday_study_time},{wednesday_study_time},{thursday_study_time},{friday_study_time},{saturday_study_time},{sunday_study_time}です。
#         私のタスクは、これらの情報を基にして、各コースレベルが特定の日付に割り当てられるようなスケジュールを立案することです。スケジュールは、具体的な日付と、その日に行うべきレベルを示す形式であるべきです。各レベルの勉強が終わるごとに次のレベルに進み、全てのレベルが終了するまでの計画を立ててください。各レベルに対して実際に勉強する日程は複数ある場合があります。
#         以下のようにスケジュールを提示してください：

#         レベル0: [日付]
#         レベル1-1: [日付]
#         レベル1-2: [日付]
#         ... 以下、各レベルに対応する日付 ...

#         各レベルの所要時間とユーザーの利用可能時間を考慮し、実際に勉強が行われる日を割り当ててください。計画のスタート日は現在の日付の次の日からにしてください。
#         また、各レベル終了後には、ユーザーが予定に遅れた場合に備えてバッファー時間を秘匿的に組み込んでください。
#         """
#     )

#     # LLM チェーンを実行するための入力データをユーザーのリクエストから構築(Next.jsができたらこっちに変更)
#     input_data = {
#         "current_date": request_body.current_date,
#         "uid":request_body.uid,
#         "monday_study_time":request_body.monday_study_time,
#         "tuesday_study_time": request_body.tuesday_study_time,
#         "wednesday_study_time": request_body.wednesday_study_time,
#         "thursday_study_time": request_body.thursday_study_time,
#         "friday_study_time": request_body.friday_study_time,
#         "saturday_study_time": request_body.saturday_study_time,
#         "sunday_study_time": request_body.sunday_study_time,
#         "target_period": request_body.target_period,
#         "course_details": request_body.course_details
#     }
    
#     # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#     chain = LLMChain(llm=llm, prompt=prompt)
#     # LLM　チェーンを実行
#     prediction = chain.run(input_data)
#     print(prediction.strip())

#     llm_response = prediction.strip()
#     # return llm_response

#     # レスポンスモデルに合わせたデータを返す
#     return StudyPlanResponse(message="Study Plan Generated!", details=llm_response)
