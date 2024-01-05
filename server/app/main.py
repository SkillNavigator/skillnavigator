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
        user_setting_id = 9 #request_data['user_setting_id']
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

    except Exception as e:
        # # トランザクションが失敗した場合はロールバック
        # db.rollback()
        logger.error(f"Error in llm-plan: {e}")
        print("Error creating LLM Answer:", e) # エラーログ
        raise HTTPException(status_code=500, detail=str(e))    

  
#全部繋がってる
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
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Float 
# # from sqlalchemy import DateTime
# # from sqlalchemy.orm import relationship, backref
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


# # db = SessionLocal() #セッションの作成
# # #DBにコンテンツを登録する
# # new_sample_schedule = [
# #     CourseDetail(course_level='level0-1 イントロダクション・基礎学習について',duration=1),
# #     CourseDetail(course_level='level1-1 環境構築',duration=0.5),
# #     CourseDetail(course_level='level1-2 データ型・演算子・変数',duration=2.5),
# #     CourseDetail(course_level='level2-1 関数',duration=5),
# #     CourseDetail(course_level='level2-2 より良いコードを書くには？',duration=2),
# #     CourseDetail(course_level='level2-3 比較',duration=2),
# #     CourseDetail(course_level='level3-1 条件分岐①',duration=4),
# #     CourseDetail(course_level='level3-2 条件分岐②・演算子・変数',duration=4),
# #     CourseDetail(course_level='level3-3 スコープ',duration=2),
# #     CourseDetail(course_level='level4-1 配列',duration=6),
# #     CourseDetail(course_level='level4-2 オブジェクト',duration=6),
# #     CourseDetail(course_level='level4-3 forループ',duration=10),
# #     CourseDetail(course_level='level5-1 HTML・CSSの基礎知識',duration=1),
# #     CourseDetail(course_level='level5-2 HTML・CSS演習（My IRページ）',duration=14)
# # ]
# # print("new_sample_schedule:",new_sample_schedule)
# # # セッションに追加
# # db.add_all(new_sample_schedule)
# # # トランザクションの確定
# # db.commit()
# # # セッションのクローズ
# # db.close()

# # Base = declarative_base()

# # #SQLAlchemyモデルとしての表現を持つFastAPIモデル
# # class UserSetting(Base):
# #     __tablename__ = "user_setting"

# #     user_setting_id = Column(Integer, primary_key=True, index=True)
# #     uid = Column(String(50), ForeignKey('users.uid')) #firebase等で使用するid 外部キー
# #     current_date = Column(DateTime, nullable=False)            #ユーザーが入力した日付と時間
# #     target_period = Column(String(10), nullable=False)         #あなたのコース：短期3か月
# #     learning_history = Column(String(30), nullable=False)      #プログラミング歴：未経験
# #     target_level = Column(String(30), nullable=False)          #目標レベル：Must課題までをマスター
# #     monday_study_time = Column(Integer, nullable=False)     #月曜日の学習時間：1
# #     tuesday_study_time = Column(Integer, nullable=False)    #火曜日の学習時間：2
# #     wednesday_study_time = Column(Integer, nullable=False)  #水曜日の学習時間：3
# #     thursday_study_time = Column(Integer, nullable=False)   #木曜日の学習時間：2
# #     friday_study_time = Column(Integer, nullable=False)     #金曜日の学習時間：1
# #     saturday_study_time = Column(Integer, nullable=False)   #土曜日の学習時間：5
# #     sunday_study_time = Column(Integer, nullable=False)     #日曜日の学習時間：5
# #     motivation_statement = Column(String(255), nullable=False)  #意気込み：頑張ります
# #     llm_answers = relationship("LLMAnswer", back_populates="user_setting")
# #     uid_user = relationship("User", back_populates="user_setting")



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
#             course_level = parts[0].strip()  # "レベルX" の "X" 部分
#             date = parts[1].strip()  # "YYYY-MM-DD" の部分
#             plan_items.append(schemas.PlanItem(course_level=course_level, date=date))
#     print("plan_items",plan_items)
#     return plan_items
   


# @app.post("/llm-plan", response_model=schemas.LLMAnswer)
# async def create_llm_plan(request: Request, db: Session = Depends(get_db)):
#     try:
#         print("Starting generate_study_plan...")  # 処理開始ログ
#         # リクエストボディをJSONとして解析
#         request_data = await request.json()

#         # ユーザー設定とコース情報を取得
#         user_setting_id = 9 #request_data['user_setting_id']
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
#             今日は{current_date}です。私は、特定のユーザーのために{target_period}のコース期間内にlevel5-2までを完了する個別化された学習スケジュールを作成しています。
#             各レベルのコース内容と所要時間は{course_detail}で、ユーザーの勉強可能時間は{monday_study_time},{tuesday_study_time},{wednesday_study_time},{thursday_study_time},{friday_study_time},{saturday_study_time},{sunday_study_time}です。
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

  
