import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from .models import LLMAnswer, UserSetting, CourseDetail, User, Base
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from typing import Dict, List
import openai
import os
from datetime import date 
import datetime
from . import crud
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain # LLM チェーンをインポート
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
# from .database import SessionLocal, engine
from sqlalchemy import create_engine
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# FastAPIアプリケーションが初期化
app = FastAPI()

# 環境変数からデータベースURLを取得
DATABASE_URL = os.environ.get("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL) 
# SQLAlchemyエンジンを作成
engine = create_engine(DATABASE_URL)
# データベーステーブルを作成
# Base.metadata.create_all(bind=engine)
# セッションファクトリーを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 環境変数を読み込む
load_dotenv()  
#OpenAIのAPIキーを環境変数から取得
openai_api_key = os.getenv("OPENAI_API_KEY") 
#初期化　temperature揺れる回答を小さい数字で揺れなくしてる
llm = OpenAI(model_name="text-davinci-003" , temperature=0.2)
# 今日の日付を取得
current_date = datetime.date.today().isoformat()  # YYYY-MM-DD形式

# # CORSミドルウェアの設定
# origins = [
#     "http://localhost:3000",  # Next.jsが動作しているURL（開発時は通常このURL）
#     # "https://your-deployment.frontend.com", # 本番のフロントエンドURL
# ]

# CORSミドルウェアを追加・異なるオリジンからのリクエストを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここで許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],  # ここで許可するHTTPメソッドを指定
    allow_headers=["*"],  # ここで許可するHTTPヘッダーを指定
)

# リクエストボディの構造を定義するPydanticモデルを作成。
#　llmに投げるデータを保証
class CourseDefault(BaseModel):
    course_details_id: int
    course_level: str # コースレベル
    duration: float # そのレベルを終えるのに必要な時間

class StudyPlanRequest(BaseModel):
    user_setting_id: int
    current_date: str # 現在の日付
    monday_study_time:float
    tuesday_study_time: float
    wednesday_study_time: float
    thursday_study_time: float
    friday_study_time: float
    saturday_study_time: float
    sunday_study_time: float
    target_period: str #(３ヶ月・６ヶ月)
    course_default: List[CourseDefault] # コースの詳細（複数のレベル）

#llmの返答の形を固定(PlaniItem,StudyPlanRespone)
class PlanItem(BaseModel):
    course_level: str  # コースのレベル
    date: str  # 日付（YYYY-MM-DD形式）

class StudyPlanResponse(BaseModel):
    plan: List[PlanItem]

#保存のために型を保証
class LLMAnswerCreateRequest(BaseModel):
    date: date 
    user_setting_id: int
    course_details_id: int

# データベースセッションの取得
def get_db():
    print("Creating database session...") # セッション生成開始ログ
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("Closing database session...")  # セッション終了ログ

def parse_llm_response(llm_response: str) -> List[PlanItem]:
    plan_items = []
    for line in llm_response.split("\n"):
        # レスポンスの各行を処理する
        if line.startswith("レベル"):
            parts = line.split(": ")
            course_level = parts[0].strip()  # "レベルX" の "X" 部分
            date = parts[1].strip()  # "YYYY-MM-DD" の部分
            plan_items.append(PlanItem(course_level=course_level, date=date))
    return plan_items

@app.get("/generate-study-plan", response_model=StudyPlanResponse)
async def generate_study_plan(user_setting_id: int, db: Session = Depends(get_db)):
    print("Starting generate_study_plan...")  # 処理開始ログ
    try:
        logger.info("Starting generate_study_plan...")
        # UserSettingから特定のユーザー設定を取得
        user_setting = crud.get_user_setting(db, user_setting_id)
        if not user_setting:
            raise HTTPException(status_code=404, detail="UserSetting not found")
        print("user_setting:", vars(user_setting))
        # CourseDetailからデータを取得
        course_details = crud.get_course_details(db)
        
        # コースレベルとIDのマッピングを作成
        course_level_to_id = {detail.course_level: detail.course_details_id for detail in course_details}
        if not course_details:
            raise HTTPException(status_code=404, detail="Course details not found")
       # course_detailsの内容をログに出力
        for detail in course_details:
            print("Course Detail:", vars(detail))
        # CourseDetailオブジェクトのリストを辞書のリストに変換
        course_default_dicts = [
            {
                "course_level": detail.course_level,
                "duration": detail.duration
            }
            for detail in course_details
        ]
        # LLM チェーンを実行するための入力データ
        #UserSettingから取得する他のLLMに必要なデータを加える
        input_data = {
            "current_date": user_setting.current_date,
            "user_setting_id":user_setting.user_setting_id,
            "monday_study_time":user_setting.monday_study_time,
            "tuesday_study_time": user_setting.tuesday_study_time,
            "wednesday_study_time": user_setting.wednesday_study_time,
            "thursday_study_time": user_setting.thursday_study_time,
            "friday_study_time": user_setting.friday_study_time,
            "saturday_study_time": user_setting.saturday_study_time,
            "sunday_study_time": user_setting.sunday_study_time,
            "target_period": user_setting.target_period,
            "course_default": course_default_dicts
        }
        
        prompt = PromptTemplate(
            input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_default"],
            template="""
            今日は{current_date}です。私は、特定のユーザーのために{target_period}のコース期間内にlevel5-2までを完了する個別化された学習スケジュールを作成しています。
            各レベルのコース内容と所要時間は{course_default}で、ユーザーの勉強可能時間は{monday_study_time},{tuesday_study_time},{wednesday_study_time},{thursday_study_time},{friday_study_time},{saturday_study_time},{sunday_study_time}です。
            私のタスクは、これらの情報を基にして、各コースレベルが特定の日付に割り当てられるようなスケジュールを立案することです。スケジュールは、具体的な日付と、その日に行うべきレベルを示す形式であるべきです。各レベルの勉強が終わるごとに次のレベルに進み、計画は最終レベルまで網羅されている必要があり、各レベルに対して実際に勉強する日程は複数ある場合があります。

            以下のようにスケジュールを提示してください：

            レベル0: [日付]
            レベル1-1: [日付]
            レベル1-2: [日付]
            ... 以下、各レベルに対応する日付 ...

            各レベルの所要時間とユーザーの利用可能時間を考慮し、実際に勉強が行われる日を割り当ててください。計画のスタート日は現在の日付の次の日からにしてください。
            全てのレベルが完了するまでのスケジュールを提案してください。
            また、level1-2,level2-3,level3-3,level4-3の終了後には、ユーザーが予定に遅れた場合に備えてバッファーとして各2時間を各レベルの後に秘匿的に組み込んでください。
            """
        )
        
        # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
        chain = LLMChain(llm=llm, prompt=prompt)
        # LLM　チェーンを実行
        prediction = chain.run(input_data)
        print(prediction.strip())
        # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
        plan_items = parse_llm_response(prediction.strip())
        
        # ここからデータベース保存処理
        for item in plan_items:
            print("Date type:", vars(item.date))  # 型の確認
            print("Date value:", item.date)  # 値の確認

            # コースレベルに基づいてcourse_details_idを取得
            course_details_id = course_level_to_id.get(item.course_level)
            if course_details_id is None:
                # 対応するcourse_details_idが見つからない場合の処理
                continue  # または適切なエラーハンドリングを行う
            # LLMAnswerCreateRequestモデルに基づいたデータ形式に整形
            user_setting_id == 1
            llm_answer_data = {
                "date": item.date,
                "user_setting_id": user_setting_id,
                "course_details_id": course_details_id,
            }
            print("user_setting_id type:", vars(user_setting_id))
            print("course_details_id type:", type(course_details_id))

            # データベースに保存
            crud.create_llm_answer(db, llm_answer_data)
            print("LLM Answer created:", llm_answer)

        # StudyPlanResponseモデルのインスタンスを作成して返す
        return StudyPlanResponse(plan=plan_items)
        
    except Exception as e:
        # # トランザクションが失敗した場合はロールバック
        # db.rollback()
        logger.error(f"Error in generate_study_plan: {e}")
        print("Error creating LLM Answer:", e) # エラーログ
        raise HTTPException(status_code=500, detail=str(e))        

@app.get("/user-settings/{user_setting_id}/llm-answers")
def read_llm_answers(user_setting_id: int):
    db = SessionLocal()
    llm_answers = crud.get_llm_answers_by_user_setting(db, user_setting_id)
    if not llm_answers:
        raise HTTPException(status_code=404, detail="LLMAnswers not found")
    return llm_answers


@app.get("/course-details", response_model=List[CourseDefault])
def read_course_details(db: Session = Depends(get_db)):
    course_details = crud.get_course_details(db)
    return course_details  # ここでは直接データベースモデルを返しています。


#変更前
# import uvicorn
# from fastapi import FastAPI, Depends, HTTPException
# from .models import LLMAnswer, UserSetting, CourseDetail, User, Base
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from typing import Dict, List
# import openai
# import os
# from datetime import date 
# import datetime
# from . import crud
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain # LLM チェーンをインポート
# from sqlalchemy.orm import Session
# from sqlalchemy.orm import sessionmaker
# # from .database import SessionLocal, engine
# from sqlalchemy import create_engine
# import logging

# # ロギングの設定
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# # FastAPIアプリケーションが初期化
# app = FastAPI()

# # 環境変数からデータベースURLを取得
# DATABASE_URL = os.environ.get("DATABASE_URL")
# print("DATABASE_URL:", DATABASE_URL) 
# # SQLAlchemyエンジンを作成
# engine = create_engine(DATABASE_URL)
# # データベーステーブルを作成
# # Base.metadata.create_all(bind=engine)
# # セッションファクトリーを作成
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # 環境変数を読み込む
# load_dotenv()  
# #OpenAIのAPIキーを環境変数から取得
# openai_api_key = os.getenv("OPENAI_API_KEY") 
# #初期化　temperature揺れる回答を小さい数字で揺れなくしてる
# llm = OpenAI(model_name="text-davinci-003" , temperature=0.2)
# # 今日の日付を取得
# current_date = datetime.date.today().isoformat()  # YYYY-MM-DD形式

# # # CORSミドルウェアの設定
# # origins = [
# #     "http://localhost:3000",  # Next.jsが動作しているURL（開発時は通常このURL）
# #     # "https://your-deployment.frontend.com", # 本番のフロントエンドURL
# # ]

# # CORSミドルウェアを追加・異なるオリジンからのリクエストを許可
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ここで許可するオリジンを指定
#     allow_credentials=True,
#     allow_methods=["*"],  # ここで許可するHTTPメソッドを指定
#     allow_headers=["*"],  # ここで許可するHTTPヘッダーを指定
# )

# # リクエストボディの構造を定義するPydanticモデルを作成。
# #　llmに投げるデータを保証
# class CourseDefault(BaseModel):
#     course_details_id: int
#     course_level: str # コースレベル
#     duration: float # そのレベルを終えるのに必要な時間

# class StudyPlanRequest(BaseModel):
#     user_setting_id: int
#     current_date: str # 現在の日付
#     monday_study_time:float
#     tuesday_study_time: float
#     wednesday_study_time: float
#     thursday_study_time: float
#     friday_study_time: float
#     saturday_study_time: float
#     sunday_study_time: float
#     target_period: str #(３ヶ月・６ヶ月)
#     course_default: List[CourseDefault] # コースの詳細（複数のレベル）

# #llmの返答の形を固定(PlaniItem,StudyPlanRespone)
# class PlanItem(BaseModel):
#     course_level: str  # コースのレベル
#     date: str  # 日付（YYYY-MM-DD形式）

# class StudyPlanResponse(BaseModel):
#     plan: List[PlanItem]

# #保存のために型を保証
# class LLMAnswerCreateRequest(BaseModel):
#     date: date 
#     user_setting_id: int
#     course_details_id: int

# # データベースセッションの取得
# def get_db():
#     print("Creating database session...") # セッション生成開始ログ
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         print("Closing database session...")  # セッション終了ログ

# def parse_llm_response(llm_response: str) -> List[PlanItem]:
#     plan_items = []
#     for line in llm_response.split("\n"):
#         # レスポンスの各行を処理する
#         if line.startswith("レベル"):
#             parts = line.split(": ")
#             course_level = parts[0].strip()  # "レベルX" の "X" 部分
#             date = parts[1].strip()  # "YYYY-MM-DD" の部分
#             plan_items.append(PlanItem(course_level=course_level, date=date))
#     return plan_items

# @app.get("/generate-study-plan", response_model=StudyPlanResponse)
# async def generate_study_plan(user_setting_id: int, db: Session = Depends(get_db)):
#     print("Starting generate_study_plan...")  # 処理開始ログ
#     try:
#         logger.info("Starting generate_study_plan...")
#         # UserSettingから特定のユーザー設定を取得
#         user_setting = crud.get_user_setting(db, user_setting_id)
#         if not user_setting:
#             raise HTTPException(status_code=404, detail="UserSetting not found")
#         print("user_setting:", vars(user_setting))
#         # CourseDetailからデータを取得
#         course_details = crud.get_course_details(db)
        
#         # コースレベルとIDのマッピングを作成
#         course_level_to_id = {detail.course_level: detail.course_details_id for detail in course_details}
#         if not course_details:
#             raise HTTPException(status_code=404, detail="Course details not found")
#        # course_detailsの内容をログに出力
#         for detail in course_details:
#             print("Course Detail:", vars(detail))
#         # CourseDetailオブジェクトのリストを辞書のリストに変換
#         course_default_dicts = [
#             {
#                 "course_level": detail.course_level,
#                 "duration": detail.duration
#             }
#             for detail in course_details
#         ]
#         # LLM チェーンを実行するための入力データ
#         #UserSettingから取得する他のLLMに必要なデータを加える
#         input_data = {
#             "current_date": user_setting.current_date,
#             "user_setting_id":user_setting.user_setting_id,
#             "monday_study_time":user_setting.monday_study_time,
#             "tuesday_study_time": user_setting.tuesday_study_time,
#             "wednesday_study_time": user_setting.wednesday_study_time,
#             "thursday_study_time": user_setting.thursday_study_time,
#             "friday_study_time": user_setting.friday_study_time,
#             "saturday_study_time": user_setting.saturday_study_time,
#             "sunday_study_time": user_setting.sunday_study_time,
#             "target_period": user_setting.target_period,
#             "course_default": course_default_dicts
#         }
        
#         prompt = PromptTemplate(
#             input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_default"],
#             template="""
#             今日は{current_date}です。私は、特定のユーザーのために{target_period}のコース期間内にlevel5-2までを完了する個別化された学習スケジュールを作成しています。
#             各レベルのコース内容と所要時間は{course_default}で、ユーザーの勉強可能時間は{monday_study_time},{tuesday_study_time},{wednesday_study_time},{thursday_study_time},{friday_study_time},{saturday_study_time},{sunday_study_time}です。
#             私のタスクは、これらの情報を基にして、各コースレベルが特定の日付に割り当てられるようなスケジュールを立案することです。スケジュールは、具体的な日付と、その日に行うべきレベルを示す形式であるべきです。各レベルの勉強が終わるごとに次のレベルに進み、計画は最終レベルまで網羅されている必要があり、各レベルに対して実際に勉強する日程は複数ある場合があります。

#             以下のようにスケジュールを提示してください：

#             レベル0: [日付]
#             レベル1-1: [日付]
#             レベル1-2: [日付]
#             ... 以下、各レベルに対応する日付 ...

#             各レベルの所要時間とユーザーの利用可能時間を考慮し、実際に勉強が行われる日を割り当ててください。計画のスタート日は現在の日付の次の日からにしてください。
#             全てのレベルが完了するまでのスケジュールを提案してください。
#             また、level1-2,level2-3,level3-3,level4-3の終了後には、ユーザーが予定に遅れた場合に備えてバッファーとして各2時間を各レベルの後に秘匿的に組み込んでください。
#             """
#         )
        
#         # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#         chain = LLMChain(llm=llm, prompt=prompt)
#         # LLM　チェーンを実行
#         prediction = chain.run(input_data)
#         print(prediction.strip())
#         # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
#         plan_items = parse_llm_response(prediction.strip())
        
#         # ここからデータベース保存処理
#         for item in plan_items:
#             print("Date type:", vars(item.date))  # 型の確認
#             print("Date value:", item.date)  # 値の確認

#             # コースレベルに基づいてcourse_details_idを取得
#             course_details_id = course_level_to_id.get(item.course_level)
#             if course_details_id is None:
#                 # 対応するcourse_details_idが見つからない場合の処理
#                 continue  # または適切なエラーハンドリングを行う
#             # LLMAnswerCreateRequestモデルに基づいたデータ形式に整形
#             user_setting_id == 1
#             llm_answer_data = {
#                 "date": item.date,
#                 "user_setting_id": user_setting_id,
#                 "course_details_id": course_details_id,
#             }
#             print("user_setting_id type:", vars(user_setting_id))
#             print("course_details_id type:", type(course_details_id))

#             # データベースに保存
#             crud.create_llm_answer(db, llm_answer_data)
#             print("LLM Answer created:", llm_answer)

#         # StudyPlanResponseモデルのインスタンスを作成して返す
#         return StudyPlanResponse(plan=plan_items)
        
#     except Exception as e:
#         # # トランザクションが失敗した場合はロールバック
#         # db.rollback()
#         logger.error(f"Error in generate_study_plan: {e}")
#         print("Error creating LLM Answer:", e) # エラーログ
#         raise HTTPException(status_code=500, detail=str(e))        

# @app.get("/user-settings/{user_setting_id}/llm-answers")
# def read_llm_answers(user_setting_id: int):
#     db = SessionLocal()
#     llm_answers = crud.get_llm_answers_by_user_setting(db, user_setting_id)
#     if not llm_answers:
#         raise HTTPException(status_code=404, detail="LLMAnswers not found")
#     return llm_answers

