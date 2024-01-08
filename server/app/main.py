 #ブラウザでクリックしたらその流れで立案、立案内容をそのままブラウザに表示
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from .models import LLMAnswer, UserSetting, CourseDetail, User, Base,CompletedRecord, Record
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from typing import Dict, List
import openai
import os
import datetime
from datetime import date, datetime as dt , timedelta
from . import crud, schemas, models
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain # LLM チェーンをインポート
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
# from .database import SessionLocal, engine
from sqlalchemy import create_engine
import logging
import pytz  # pytzモジュールを使用してタイムゾーンを扱います
import psycopg2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
#データベーステーブルを作成
Base.metadata.create_all(bind=engine)
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


# CORSミドルウェアを追加・異なるオリジンからのリクエストを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここで許可するオリジンを指定  指定する場合"http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # ここで許可するHTTPメソッドを指定
    allow_headers=["*"],  # ここで許可するHTTPヘッダーを指定
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

# Pydanticモデルの定義（POSTリクエストのボディから受け取るデータ構造を定義する）
class Course(BaseModel):
    selectedCourse: str

class DeterminationInput(BaseModel):
    determinationText: str

# Pydanticモデルの定義（POSTリクエストのボディから受け取るデータ構造を定義する）
class StudyTime(BaseModel):
    studyTime: list[int]

#reloadされると配列の中身が空に
course_select_1 = []
learning_history_2 = []
target_level_3 = []
study_time_4 = []
determination_5 = []
day = []

@app.post("/api/course_select_1")
#ボディにはCourseモデルが使用され、同じデータがJSON形式でレスポンスとして返される
async def save_data(course:Course):
    course_select_1.append(course.selectedCourse)
    print(course_select_1)
    return course.selectedCourse

@app.post("/api/learning_history_2")
#ボディにはCourseモデルが使用され、同じデータがJSON形式でレスポンスとして返される
async def save_data(course:Course):
    learning_history_2.append(course.selectedCourse)
    print(learning_history_2)
    return course.selectedCourse

@app.post("/api/target_level_3")
#ボディにはCourseモデルが使用され、同じデータがJSON形式でレスポンスとして返される
async def save_data(course:Course):
    target_level_3.append(course.selectedCourse)
    print(target_level_3)
    return course.selectedCourse

# 学習時間データを保存するエンドポイント
@app.post("/api/study_time_4")
async def save_study_time(study_time: StudyTime):
    saved_data = {"message": "Study time data received and saved", "data": study_time.studyTime}
    # return saved_data
    study_time_4.append(study_time.studyTime)
    print(study_time_4)
    return study_time.studyTime

@app.post("/api/determination_5")
async def save_text(determination_input:DeterminationInput):
    determination_5.append(determination_input.determinationText)
    print(determination_5)
    return determination_input.determinationText

#配列データをDBに挿入するエンドポイント
@app.post("/api/setting_complete")
async def setting_complete():
# 日本のタイムゾーンを取得
    japan_timezone = pytz.timezone('Asia/Tokyo')
    insert_array = []
    insert_array.append("test-UID1234")
    today_date = dt.now(japan_timezone)
    print(today_date)
    # `today_date`を文字列に変換して格納
    insert_array.append(today_date.strftime("%Y-%m-%d %H:%M:%S"))
    insert_array.append(course_select_1[-1])
    insert_array.append(learning_history_2[-1])
    insert_array.append(target_level_3[-1])
    insert_array.append(study_time_4[-1][0]) #月
    insert_array.append(study_time_4[-1][1]) #火
    insert_array.append(study_time_4[-1][2]) #水
    insert_array.append(study_time_4[-1][3]) #木
    insert_array.append(study_time_4[-1][4]) #金
    insert_array.append(study_time_4[-1][5]) #土
    insert_array.append(study_time_4[-1][6]) #日
    insert_array.append(determination_5[-1])
    #print(course_select_1,learning_history_2,target_level_3,study_time_4,determination_5)
    print(insert_array)

    user_setting_data = {
        "uid"                 : insert_array[0],
        "current_date"        : insert_array[1],
        "target_period"       : insert_array[2],
        "learning_history"    : insert_array[3],   #プログラミング歴：未経験
        "target_level"        : insert_array[4],   #目標レベル：Must課題までをマスター
        "monday_study_time"   : insert_array[5],   #月曜日の学習時間：1
        "tuesday_study_time"  : insert_array[6],   #火曜日の学習時間：2
        "wednesday_study_time": insert_array[7],   #水曜日の学習時間：3
        "thursday_study_time" : insert_array[8],   #木曜日の学習時間：2
        "friday_study_time"   : insert_array[9],   #金曜日の学習時間：1
        "saturday_study_time" : insert_array[10],   #土曜日の学習時間：5
        "sunday_study_time"   : insert_array[11],  #日曜日の学習時間：5
        "motivation_statement": insert_array[12],  #意気込み：頑張ります
    }
    print("user_setting_data:",user_setting_data)
    db = SessionLocal()
    try:
        user_setting = UserSetting(**user_setting_data)
        print("aaaaaaaaa")
        db.add(user_setting)
        print("bbbbbbbbb")
        db.commit()
        print("cccccccccomit")
        db.refresh(user_setting)
        print("refreshhhhhhh")
        return {"message": "Setting completed successfully", "user_setting": user_setting}
    except Exception as e:
        print(f"An error occurred during commit: {e}")
    finally:
        db.close()

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
    print("user_setting_idddddddd:",user_setting_id)
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
            print("Parts after splitting:", parts)
            course_level = parts[0].strip()  # "レベルX" の "X" 部分
            date_str = parts[1].strip()  # "YYYY-MM-DD" 形式の日付文字列
            # date = parts[1].strip()  # "YYYY-MM-DD" の部分

            # " 1時間"を取り除いて日付部分だけを抽出
            date_str = date_str.split(' ')[0]  # 空白で分割して最初の部分（日付）を取得
            # 日付の文字列を datetime オブジェクトに変換
            date_obj = dt.strptime(date_str, "%Y-%m-%d")
            # datetime オブジェクトを YYYY-MM-DD 形式の文字列に再フォーマット
            formatted_date = date_obj.strftime("%Y-%m-%d")

            plan_items.append(schemas.PlanItem(course_level=course_level, date=formatted_date))
    print("plan_items",plan_items)
    return plan_items
   


@app.post("/llm-plan", response_model=schemas.LLMAnswer)
async def create_llm_plan(request: Request, db: Session = Depends(get_db)):
    try:
        print("Starting generate_study_plan...")  # 処理開始ログ
        # リクエストボディをJSONとして解析
        request_data = await request.json()

        # ユーザー設定とコース情報を取得
        request_data = await request.json()
        user_setting_id = request_data.get('user_setting_id')  # リクエストからuser_setting_idを取得
        if not user_setting_id:
            raise HTTPException(status_code=400, detail="User setting ID is required")
        # ユーザー設定をデータベースから取得する
        user_setting = crud.get_user_setting(db, user_setting_id)
        if not user_setting:
            raise HTTPException(status_code=404, detail="User setting not found")
        print("user_setting:",user_setting)
        print("Tuesday study time:", user_setting.tuesday_study_time)
        print("target_period:", user_setting.target_period)
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
            "learning_history":user_setting.learning_history,
            "course_detail": course_details_dicts
        }
        
        prompt = PromptTemplate(
            input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","learning_history","course_detail"],
            template="""
            あなたは目的を達成するための計画を立案する才能に長けています。
            今回の依頼は、{learning_history}の学習経験を持ち、プログラミングの勉強を始めた人が{target_period}内にlevel5-2までのコースを完了することを目指しています。各コースレベルの平均所要時間は{course_detail}です。

            ユーザーの1週間の勉強可能時間は以下の通りです。この時間を基に計画を立て、無駄なく効率的にコースを進められるようにしてください。
            - 月曜日: {monday_study_time}時間
            - 火曜日: {tuesday_study_time}時間
            - 水曜日: {wednesday_study_time}時間
            - 木曜日: {thursday_study_time}時間
            - 金曜日: {friday_study_time}時間
            - 土曜日: {saturday_study_time}時間
            - 日曜日: {sunday_study_time}時間

            各コースレベルが特定の日付に割り当てられる学習スケジュールを立案してください。計画は{current_date}の次の日から開始し、level5-2を含む全てのレベルが完了するまでの日程を示してください。計画中、ユーザーの勉強可能時間を超えないよう注意してください。また、各レベルの終了後には、予定に遅れた場合に備えてバッファータイムを設けてください。それぞれのレベルの所要時間を考慮し、スケジュールに反映させてください。

            スケジュールは以下のフォーマットで提示してください：
            レベル0: [日付]
            レベル1-1: [日付]
            レベル1-2: [日付]
            ... 以下、各レベルに対応する日付 ...

            各レベルの勉強時間をユーザーの勉強可能時間に合わせて調整し、最も効率的で実現可能な計画を提案してください。特に、勉強可能時間が0の日は計画を立てないようにしてください。計画はユーザーの目標、勉強可能時間、コース内容を考慮して最適化されるべきです。
            """
        )
        #level1-2, level2-3, level3-3, level4-3の終了後には、予定に遅れた場合に備えてバッファータイムを設けてください。
        # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
        chain = LLMChain(llm=llm, prompt=prompt)
        # LLM　チェーンを実行
        prediction = chain.run(input_data)
        print("Prediction:", prediction)
        # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
        plan_items = parse_llm_response(prediction.strip())
                # 計画内容をデータベースに保存
        for item in plan_items:
            new_llm_answer = LLMAnswer(
                course_level=item.course_level,
                date=dt.strptime(item.date, "%Y-%m-%d").date(),
                user_setting_id=user_setting_id  # 仮定: user_setting_idはユーザー設定ID
            )
            print("new_llm_answer:",new_llm_answer)
            db.add(new_llm_answer)
        
        db.commit()  # トランザクションのコミット

        # 保存した計画内容をフロントエンドに返す
        saved_plan = db.query(LLMAnswer).filter(LLMAnswer.user_setting_id == user_setting_id).all()
        print("save_plan:",save_plan)
        saved_llm_plans = schemas.LLMAnswer(plan=saved_plan) 
        print("saved_llm_plans:",saved_llm_plans)
        return saved_llm_plan

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

        # llm_answer = schemas.LLMAnswer(plan=plan_items)  # PlanItemリストをLLMAnswerのplanに割り当てる
        # return llm_answer  # これを返却する

    # except Exception as e:
    #     # # トランザクションが失敗した場合はロールバック
    #     # db.rollback()
    #     logger.error(f"Error in llm-plan: {e}")
    #     print("Error creating LLM Answer:", e) # エラーログ
    #     raise HTTPException(status_code=500, detail=str(e))    


# # LLM計画を保存するためのエンドポイント
# @app.post("/save-llm-plan/")
# async def save_llm_plan(plan: LLMAnswer, db: Session = Depends(get_db)):
#     try:
#         # 各計画項目をデータベースに挿入
#         for item in plan.plan:
#             new_plan = LLMAnswer(date=item.date, user_setting_id=plan.user_setting_id)  # LLMAnswerモデルを使用
#             db.add(new_plan)
#         db.commit()  # トランザクションをコミット
#     except Exception as e:
#         db.rollback()  # エラーが発生したらロールバック
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()  # セッションを閉じる

#     return {"status": "success", "message": "Plan saved successfully"}

#最新版
# import uvicorn
# from fastapi import FastAPI, Depends, HTTPException, Request
# from .models import LLMAnswer, UserSetting, CourseDetail, User, Base,CompletedRecord, Record
# from dotenv import load_dotenv
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from typing import Dict, List
# import openai
# import os
# import datetime
# from datetime import date, datetime as dt , timedelta
# from . import crud, schemas, models
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import LLMChain # LLM チェーンをインポート
# from sqlalchemy.orm import Session
# from sqlalchemy.orm import sessionmaker
# # from .database import SessionLocal, engine
# from sqlalchemy import create_engine
# import logging
# import pytz  # pytzモジュールを使用してタイムゾーンを扱います
# import psycopg2

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
# #データベーステーブルを作成
# Base.metadata.create_all(bind=engine)
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


# # CORSミドルウェアを追加・異なるオリジンからのリクエストを許可
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ここで許可するオリジンを指定  指定する場合"http://localhost:3000"
#     allow_credentials=True,
#     allow_methods=["*"],  # ここで許可するHTTPメソッドを指定
#     allow_headers=["*"],  # ここで許可するHTTPヘッダーを指定
# )

# class User(BaseModel):
#     uid: str
#     user_name: str

# @app.post("/create_user")
# def create_user(user: User):
#     logging.info("create_user関数が呼ばれました")



#     database_url = os.environ.get("DATABASE_URL", "postgresql://postgres:password@db:5432/postgres")
#     conn = psycopg2.connect(database_url)
#     cur = conn.cursor()

#     try:
#         cur.execute("INSERT INTO users (uid, user_name) VALUES (%s, %s)",
#                     (user.uid, user.user_name))
#         conn.commit()
#     except Exception as e:
#         logging.info("呼ばれました")
#         conn.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cur.close()
#         conn.close()

#     return {"message": "User created successfully"}

# # Pydanticモデルの定義（POSTリクエストのボディから受け取るデータ構造を定義する）
# class Course(BaseModel):
#     selectedCourse: str

# class DeterminationInput(BaseModel):
#     determinationText: str

# # Pydanticモデルの定義（POSTリクエストのボディから受け取るデータ構造を定義する）
# class StudyTime(BaseModel):
#     studyTime: list[int]

# #reloadされると配列の中身が空に
# course_select_1 = []
# learning_history_2 = []
# target_level_3 = []
# study_time_4 = []
# determination_5 = []
# day = []

# @app.post("/api/course_select_1")
# #ボディにはCourseモデルが使用され、同じデータがJSON形式でレスポンスとして返される
# async def save_data(course:Course):
#     course_select_1.append(course.selectedCourse)
#     print(course_select_1)
#     return course.selectedCourse

# @app.post("/api/learning_history_2")
# #ボディにはCourseモデルが使用され、同じデータがJSON形式でレスポンスとして返される
# async def save_data(course:Course):
#     learning_history_2.append(course.selectedCourse)
#     print(learning_history_2)
#     return course.selectedCourse

# @app.post("/api/target_level_3")
# #ボディにはCourseモデルが使用され、同じデータがJSON形式でレスポンスとして返される
# async def save_data(course:Course):
#     target_level_3.append(course.selectedCourse)
#     print(target_level_3)
#     return course.selectedCourse

# # 学習時間データを保存するエンドポイント
# @app.post("/api/study_time_4")
# async def save_study_time(study_time: StudyTime):
#     saved_data = {"message": "Study time data received and saved", "data": study_time.studyTime}
#     # return saved_data
#     study_time_4.append(study_time.studyTime)
#     print(study_time_4)
#     return study_time.studyTime

# @app.post("/api/determination_5")
# async def save_text(determination_input:DeterminationInput):
#     determination_5.append(determination_input.determinationText)
#     print(determination_5)
#     return determination_input.determinationText

# #配列データをDBに挿入するエンドポイント
# @app.post("/api/setting_complete")
# async def setting_complete():
# # 日本のタイムゾーンを取得
#     japan_timezone = pytz.timezone('Asia/Tokyo')
#     insert_array = []
#     insert_array.append("test-UID1234")
#     today_date = dt.now(japan_timezone)
#     print(today_date)
#     # `today_date`を文字列に変換して格納
#     insert_array.append(today_date.strftime("%Y-%m-%d %H:%M:%S"))
#     insert_array.append(course_select_1[-1])
#     insert_array.append(learning_history_2[-1])
#     insert_array.append(target_level_3[-1])
#     insert_array.append(study_time_4[-1][0]) #月
#     insert_array.append(study_time_4[-1][1]) #火
#     insert_array.append(study_time_4[-1][2]) #水
#     insert_array.append(study_time_4[-1][3]) #木
#     insert_array.append(study_time_4[-1][4]) #金
#     insert_array.append(study_time_4[-1][5]) #土
#     insert_array.append(study_time_4[-1][6]) #日
#     insert_array.append(determination_5[-1])
#     #print(course_select_1,learning_history_2,target_level_3,study_time_4,determination_5)
#     print(insert_array)

#     user_setting_data = {
#         "uid"                 : insert_array[0],
#         "current_date"        : insert_array[1],
#         "target_period"       : insert_array[2],
#         "learning_history"    : insert_array[3],   #プログラミング歴：未経験
#         "target_level"        : insert_array[4],   #目標レベル：Must課題までをマスター
#         "monday_study_time"   : insert_array[5],   #月曜日の学習時間：1
#         "tuesday_study_time"  : insert_array[6],   #火曜日の学習時間：2
#         "wednesday_study_time": insert_array[7],   #水曜日の学習時間：3
#         "thursday_study_time" : insert_array[8],   #木曜日の学習時間：2
#         "friday_study_time"   : insert_array[9],   #金曜日の学習時間：1
#         "saturday_study_time" : insert_array[10],   #土曜日の学習時間：5
#         "sunday_study_time"   : insert_array[11],  #日曜日の学習時間：5
#         "motivation_statement": insert_array[12],  #意気込み：頑張ります
#     }
#     print("user_setting_data:",user_setting_data)
#     db = SessionLocal()
#     try:
#         user_setting = UserSetting(**user_setting_data)
#         print("aaaaaaaaa")
#         db.add(user_setting)
#         print("bbbbbbbbb")
#         db.commit()
#         print("cccccccccomit")
#         db.refresh(user_setting)
#         print("refreshhhhhhh")
#         return {"message": "Setting completed successfully", "user_setting": user_setting}
#     except Exception as e:
#         print(f"An error occurred during commit: {e}")
#     finally:
#         db.close()

# # データベースセッションの取得
# def get_db():
#     print("Creating database session...") # セッション生成開始ログ
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         print("Closing database session...")  # セッション終了ログ

# @app.get("/user-settings/{user_setting_id}")  # パスパラメータの設定
# def read_user_setting(user_setting_id: int, db: Session = Depends(get_db)):  # 依存関係としてデータベースセッションを注入
#     user_setting = crud.get_user_setting(db, user_setting_id=user_setting_id)
#     if not user_setting:
#         raise HTTPException(status_code=404, detail="User setting not found")
#     return user_setting



# @app.get("/course-details", response_model=List[schemas.CourseDetail])
# def read_course_details(db: Session = Depends(get_db)):
#     course_details = crud.get_course_details(db)
#     return course_details  # ここでは直接データベースモデルを返しています。

# def parse_llm_response(llm_response: str) -> List[schemas.PlanItem]:
#     print("llm_response:",llm_response)
#     plan_items = []
#     for line in llm_response.split("\n"):
#         line = line.strip()
#         print("Processing line:", line)  # 処理している行を出力
#         # レスポンスの各行を処理する
#         if line.startswith("レベル"):
#             # print(line.startswith("レベル"))
#             parts = line.split(": ")
#             print("Parts after splitting:", parts)
#             course_level = parts[0].strip()  # "レベルX" の "X" 部分
#             date_str = parts[1].strip()  # "YYYY-MM-DD" 形式の日付文字列
#             # date = parts[1].strip()  # "YYYY-MM-DD" の部分

#             # " 1時間"を取り除いて日付部分だけを抽出
#             date_str = date_str.split(' ')[0]  # 空白で分割して最初の部分（日付）を取得
#             # 日付の文字列を datetime オブジェクトに変換
#             date_obj = dt.strptime(date_str, "%Y-%m-%d")
#             # datetime オブジェクトを YYYY-MM-DD 形式の文字列に再フォーマット
#             formatted_date = date_obj.strftime("%Y-%m-%d")

#             plan_items.append(schemas.PlanItem(course_level=course_level, date=formatted_date))
#     print("plan_items",plan_items)
#     return plan_items
   


# @app.post("/llm-plan", response_model=schemas.LLMAnswer)
# async def create_llm_plan(request: Request, db: Session = Depends(get_db)):
#     try:
#         print("Starting generate_study_plan...")  # 処理開始ログ
#         # リクエストボディをJSONとして解析
#         request_data = await request.json()

#         # ユーザー設定とコース情報を取得
#         user_setting_id = 11 #request_data['user_setting_id']
#         user_setting = crud.get_user_setting(db, user_setting_id) 
#         if not user_setting:
#             raise HTTPException(status_code=404, detail="User setting not found")
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
#         course_details_dicts = [
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
#             "course_detail": course_details_dicts
#         }
        
#         prompt = PromptTemplate(
#             input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_detail"],
#             template="""
#             今日は{current_date}です。ユーザーの目標は、{target_period}内にlevel5-2までのコースを完了することです。各コースレベルの所要時間は{course_detail}に記載されており、ユーザーの1週間の勉強可能時間は以下の通りです:

#             - 月曜日: {monday_study_time}時間
#             - 火曜日: {tuesday_study_time}時間
#             - 水曜日: {wednesday_study_time}時間
#             - 木曜日: {thursday_study_time}時間
#             - 金曜日: {friday_study_time}時間
#             - 土曜日: {saturday_study_time}時間
#             - 日曜日: {sunday_study_time}時間

#             これらの情報を基にして、各コースレベルが特定の日付に割り当てられる学習スケジュールを立案してください。スケジュールは以下のフォーマットで提示してください：

#             レベル0: [日付]
#             レベル1-1: [日付]
#             ベル1-2: [日付]
#             ... 以下、各レベルに対応する日付 ...

#             計画は現在の日付の次の日から開始し、level5-2を含む全てのレベルが完了するまでの日程を示してください。level1-2, level2-3, level3-3, level4-3の終了後には、予定に遅れた場合に備えてバッファータイムを設けてください。それぞれのレベルの所要時間を考慮し、スケジュールに反映させてください。
#             """
#         )
        
#         # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#         chain = LLMChain(llm=llm, prompt=prompt)
#         # LLM　チェーンを実行
#         prediction = chain.run(input_data)
#         print("Prediction:", prediction)
#         # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
#         plan_items = parse_llm_response(prediction.strip())
#         print("plan_items:",plan_items)
#         llm_answer = schemas.LLMAnswer(plan=plan_items)  # PlanItemリストをLLMAnswerのplanに割り当てる
#         return llm_answer  # これを返却する

#     except Exception as e:
#         # # トランザクションが失敗した場合はロールバック
#         # db.rollback()
#         logger.error(f"Error in llm-plan: {e}")
#         print("Error creating LLM Answer:", e) # エラーログ
#         raise HTTPException(status_code=500, detail=str(e))        

  
