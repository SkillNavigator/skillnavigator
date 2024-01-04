#ブラウザでクリックしたらその流れで立案、立案内容保存もされブラウザにも表示
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
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
from . import crud, schemas, models
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

# データベースセッションの取得
def get_db():
    print("Creating database session...") # セッション生成開始ログ
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("Closing database session...")  # セッション終了ログ

@app.get("/user-settings/{user_setting_id}")  # パスパラメータの設定
def read_user_setting(user_setting_id: int, db: Session = Depends(get_db)):  # 依存関係としてデータベースセッションを注入
    user_setting = crud.get_user_setting(db, user_setting_id=user_setting_id)
    if not user_setting:
        raise HTTPException(status_code=404, detail="User setting not found")
    return user_setting



@app.get("/course-details", response_model=List[schemas.CourseDetail])
def read_course_details(db: Session = Depends(get_db)):
    course_details = crud.get_course_details(db)
    return course_details  # ここでは直接データベースモデルを返しています。

def parse_llm_response(llm_response: str) -> List[schemas.PlanItem]:
    print("llm_response:",llm_response)
    plan_items = []
    for line in llm_response.split("\n"):
        line = line.strip()
        print("Processing line:", line)  # 処理している行を出力
        # レスポンスの各行を処理する
        if line.startswith("レベル"):
            # print(line.startswith("レベル"))
            parts = line.split(": ")
            course_level = parts[0].strip()  # "レベルX" の "X" 部分
            date = parts[1].strip()  # "YYYY-MM-DD" の部分
            plan_items.append(schemas.PlanItem(course_level=course_level, date=date))
    print("plan_items",plan_items)
    return plan_items
   


@app.post("/llm-plan", response_model=schemas.LLMAnswer)
async def create_llm_plan(request: Request, db: Session = Depends(get_db)):
    try:
        print("Starting generate_study_plan...")  # 処理開始ログ
        # リクエストボディをJSONとして解析
        request_data = await request.json()

        # ユーザー設定とコース情報を取得
        user_setting_id = 1 #request_data['user_setting_id']
        user_setting = crud.get_user_setting(db, user_setting_id) 
        if not user_setting:
            raise HTTPException(status_code=404, detail="User setting not found")
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
        course_details_dicts = [
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
            "course_detail": course_details_dicts
        }
        
        prompt = PromptTemplate(
            input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_detail"],
            template="""
            今日は{current_date}です。私は、特定のユーザーのために{target_period}のコース期間内にlevel5-2までを完了する個別化された学習スケジュールを作成しています。
            各レベルのコース内容と所要時間は{course_detail}で、ユーザーの勉強可能時間は{monday_study_time},{tuesday_study_time},{wednesday_study_time},{thursday_study_time},{friday_study_time},{saturday_study_time},{sunday_study_time}です。
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
        # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
        plan_items = parse_llm_response(prediction.strip())
        print("plan_items:",plan_items)
        llm_answer = schemas.LLMAnswer(plan=plan_items)  # PlanItemリストをLLMAnswerのplanに割り当てる
        return llm_answer  # これを返却する
        # # # ここからデータベース保存処理
        # for item in plan_items:
        #     print("Date type:", vars(item.date))  # 型の確認
        #     print("Date value:", item.date)  # 値の確認

        #     # コースレベルに基づいてcourse_details_idを取得
        #     course_details_id = course_level_to_id.get(item.course_level)
        #     if course_details_id is None:
        #         # 対応するcourse_details_idが見つからない場合の処理
        #         continue  # または適切なエラーハンドリングを行う
        #     # LLMAnswerCreateRequestモデルに基づいたデータ形式に整形
        #     user_setting_id == 1
        #     llm_answer_data = {
        #         "date": item.date,
        #         "user_setting_id": user_setting_id,
        #         "course_details_id": course_details_id,
        #     }
        #     print("user_setting_id type:", vars(user_setting_id))
        #     print("course_details_id type:", type(course_details_id))

        #     # データベースに保存
        #     crud.create_llm_answer(db, llm_answer_data)
        #     print("LLM Answer created:", llm_answer)

        # # StudyPlanResponseモデルのインスタンスを作成して返す
        # return StudyPlanResponse(plan=plan_items)
        
    except Exception as e:
        # # トランザクションが失敗した場合はロールバック
        # db.rollback()
        logger.error(f"Error in llm-plan: {e}")
        print("Error creating LLM Answer:", e) # エラーログ
        raise HTTPException(status_code=500, detail=str(e))        

# #下記、ブラウザに表示するためのエンドポイント
# @app.get("/user-settings/{user_setting_id}/llm-answers")
# def read_llm_answers(user_setting_id: int):
#     db = SessionLocal()
#     llm_answers = crud.get_llm_answers_by_user_setting(db, user_setting_id)
#     if not llm_answers:
#         raise HTTPException(status_code=404, detail="LLMAnswers not found")
#     return llm_answers


# @app.get("/course-details", response_model=List[CourseDefault])
# def read_course_details(db: Session = Depends(get_db)):
#     course_details = crud.get_course_details(db)
#     return course_details  # ここでは直接データベースモデルを返しています。







# # ただのpost　表示可能
# import uvicorn
# from fastapi import FastAPI, HTTPException, Depends
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Dict, List
# from pydantic import BaseModel#,ValidationError, validator , root_validator#LLM用　
# from sqlalchemy.orm import Session
# from .models import LLMAnswer, UserSetting, CourseDetail, User, Base# models.py からのモデルのインポート
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import openai
# import os
# import datetime
# # import httpx #LLM用
# from langchain.llms import OpenAI
# from langchain import PromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain # LLM チェーンをインポート
# # main.pyには入っててmain2.pyに入ってないやつ
# # from . import crud
# # from datetime import date 
# # import logging

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


# # 依存性
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# @app.post("/generate-study-plan")
# async def generate_study_plan(request_body: UserSetting):
#     prompt = PromptTemplate(
#         input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_details"],
#         template="""
#         今日は{current_date}です。私は、特定のユーザーのために{target_period}のコース期間内にlevel5-2までを完了する個別化された学習スケジュールを作成しています。
#         各レベルのコース内容と所要時間は{course_details}で、ユーザーの勉強可能時間は{monday_study_time},{tuesday_study_time},{wednesday_study_time},{thursday_study_time},{friday_study_time},{saturday_study_time},{sunday_study_time}です。
#         私のタスクは、これらの情報を基にして、各コースレベルが特定の日付に割り当てられるようなスケジュールを立案することです。スケジュールは、具体的な日付と、その日に行うべきレベルを示す形式であるべきです。各レベルの勉強が終わるごとに次のレベルに進み、計画は最終レベルまで網羅されている必要があり、各レベルに対して実際に勉強する日程は複数ある場合があります。
#         以下のようにスケジュールを提示してください：

#         レベル0: [日付]
#         レベル1-1: [日付]
#         レベル1-2: [日付]
#         ... 以下、各レベルに対応する日付 ...

#         各レベルの所要時間とユーザーの利用可能時間を考慮し、実際に勉強が行われる日を割り当ててください。計画のスタート日は現在の日付の次の日からにしてください。
#         全てのレベルが完了するまでのスケジュールを提案してください。
#         また、level1-2,level2-3,level3-3,level4-3の終了後には、ユーザーが予定に遅れた場合に備えてバッファーとして各2時間を各レベルの後に秘匿的に組み込んでください。
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


# # ポストマンよう
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
#     "course_details": [
#         {"course_level": "level0 イントロダクション・基礎学習について", "duration": 1},
#         {"course_level": "level1-1 環境構築", "duration": 0.5},
#         {"course_level": "level1-2 データ型・演算子・変数", "duration": 2.5},
#         {"course_level": "level2-1 関数", "duration": 5},
#         {"course_level": "level2-2 より良いコードを書くには？", "duration": 2},
#         {"course_level": "level2-3 比較", "duration": 2},
#         {"course_level": "level3-1 条件分岐①", "duration": 4},
#         {"course_level": "level3-2 条件分岐②", "duration": 4},
#         {"course_level": "level3-3 スコープ", "duration": 2},
#         {"course_level": "level4-1 配列", "duration": 6},
#         {"course_level": "level4-2 オブジェクト", "duration": 6},
#         {"course_level": "level4-3 forループ", "duration": 10},
#         {"course_level": "level5-1 HTML・CSSの基礎知識", "duration": 1},
#         {"course_level": "level5-2 HTML・CSS演習（My IRページ", "duration": 14}
#     ],
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
