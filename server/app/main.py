from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import pytz  # pytzモジュールを使用してタイムゾーンを扱います

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ReactアプリケーションのURLに置き換えてください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base = declarative_base()

#SQLAlchemyモデルとしての表現を持つFastAPIモデル
class UserSetting(Base):
    __tablename__ = "User Setting"

    user_setting_id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(50), nullable=False)                   #外部キーを入れるかどうか           
    current_date = Column(DateTime, nullable=False)
    target_period = Column(String(10), nullable=False)         #あなたのコース：短期3か月
    learning_history = Column(String(30), nullable=False)      #プログラミング歴：未経験
    target_level = Column(String(30), nullable=False)          #目標レベル：Must課題までをマスター
    monday_study_time = Column(Integer, nullable=False)     #月曜日の学習時間：1
    tuesday_study_time = Column(Integer, nullable=False)    #火曜日の学習時間：2
    wednesday_study_time = Column(Integer, nullable=False)  #水曜日の学習時間：3
    thursday_study_time = Column(Integer, nullable=False)   #木曜日の学習時間：2
    friday_study_time = Column(Integer, nullable=False)     #金曜日の学習時間：1
    saturday_study_time = Column(Integer, nullable=False)   #土曜日の学習時間：5
    sunday_study_time = Column(Integer, nullable=False)     #日曜日の学習時間：5
    motivation_statement = Column(String(255), nullable=False)  #意気込み：頑張ります

#DB接続を設定する
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    insert_array.append("uid")
    today_date = datetime.now(japan_timezone)
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
    print(user_setting_data)
    db = SessionLocal()
    try:
        user_setting = UserSetting(**user_setting_data)
        db.add(user_setting)
        db.commit()
        db.refresh(user_setting)
        return {"message": "Setting completed successfully", "user_setting": user_setting}
    finally:
        db.close()


