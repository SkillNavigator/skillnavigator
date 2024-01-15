#現在の正規コード
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
llm = OpenAI(model_name="gpt-3.5-turbo-instruct" , temperature=0.3)
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
        if line.startswith("level"):
            # if line.startswith("レベル")
            parts = line.split(": ")
            print("Parts after splitting:", parts)
            course_level = parts[0].strip()  # "レベルX" の "X" 部分
            # date_range = parts[1].strip().split(" - ")
            # start_date = dt.strptime(date_range[0], "%Y/%m/%d").strftime("%Y-%m-%d")
            # end_date = dt.strptime(date_range[1], "%Y/%m/%d").strftime("%Y-%m-%d")
            # plan_items.append(schemas.PlanItem(course_level=course_level, start_date=start_date, end_date=end_date))

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
            "course_detail": course_details_dicts
        }

           
            # "learning_history":user_setting.learning_history,
            # "target_level":user_setting.target_level,
        
        prompt=" "

        if(user_setting.target_period == "短期3か月"):
            if(user_setting.learning_history =="未経験"):
                if(user_setting.target_level == "Must課題までをマスター"):
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        User は下記のようなカリキュラムを受講します。

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。
                        - 出力フォーマット以外の情報は必要ありません。


                        ## 学習所要時間

                        {course_detail}

                        ## 開始日

                        {current_date}

                        ## 受講期間

                        {target_period}

                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間

                        ## 前提条件

                        - ユーザーは初めてプログラミングを学ぶため、理解に時間がかかり、学習の進捗ペースが遅いです。
                        - 学習所要時間より大幅に学習時間を必要としています。
                        - 学習可能な時間リソースの通り、学習可能時間が多いため開始日から3ヶ月以内でlevel5-2までを終了さてください。
                        

                        ## 依頼

                        - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 開始日より3ヶ月以内に `level5-2` までを終了する計画を算出してください。
                        - 学習所要時間と学習可能な時間リソースを考慮して、学習に必要な所要時間を再設定してください。
                        - ユーザーは学習の進捗ペースが遅いことを考慮して計画を立ててください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。
                        - 出力フォーマット以外の情報は必要ありません。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
                        """

                    )
                else: #未経験✖️advance課題の人
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。


                        ## 学習所要時間

                        {course_detail}

                        ## 開始日

                        {current_date}

                        ## 受講期間

                        {target_period}


                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間

                        ## Userの特徴

                        - ユーザーは初めてプログラミングを学ぶため、理解に時間がかかり、学習の進捗ペースが遅いです。
                        - 学習所要時間より大幅に学習時間を必要としています。
                        - 学習中、多くの課題に取り組むため、各levelごとに3時間のバッファー時間を設けてください。
                        - 学習可能な時間リソースの通り、学習可能時間が多いため開始日から3ヶ月以内でlevel5-2までを終了さてください。

                        ## 依頼

                        - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 開始日より3ヶ月以内に `level5-2` までを終了する計画を算出してください。
                        - 学習所要時間と学習可能な時間リソースを考慮して、学習に必要な所要時間を再設定してください。
                        - ユーザーは学習の進捗ペースが遅いことを考慮して計画を立ててください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。
                        - 出力フォーマット以外の情報は必要ありません。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
                        """

                    )
            else: #未経験以外のmust課題
                if(user_setting.target_level == "Must課題までをマスター"):
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        User は下記のようなカリキュラムを受講します。

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。


                        ## 学習所要時間
                        {course_detail}

                        ## 開始日

                        {current_date}

                        ## 受講期間

                        {target_period}


                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間

                        ## 必須要件
                        - 開始日より3ヶ月以内に `level5-2` までを修了する計画である必要があります。

                        ## Userの特徴

                        - すでにプログラミングを学習しているため、カリキュラムの進捗が早いことを考慮して計画をしてください。

                        ## 依頼

                        - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 学習所要時間と学習可能な時間リソースを考慮して、学習に必要な所要時間を再設定してください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。
                        - 出力フォーマット以外の情報は必要ありません。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
                        """

                    )
                else: #未経験者以外でadvance
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        User は下記のようなカリキュラムを受講します。

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。

                        ## 必須要件
                        - 受講期間内に `level5-2` までを修了する計画である必要があります。

                        ## 学習所要時間

                        {course_detail}

                        ## 開始日

                        {current_date}

                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間

                        ## 必須要件
                        - 開始日より3ヶ月以内に `level5-2` までを修了する計画である必要があります。

                        ## 依頼

                        - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 学習所要時間と学習可能な時間リソースを考慮して、学習に必要な所要時間を再設定してください。
                        - このユーザーは学習ペースが遅いことを考慮してください。
                        - 各レベルごとにバッファーとして3時間設けて、計画を立案してください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
                        """

                    )
    
        else: #6か月
            if(user_setting.learning_history =="未経験"):
                if(user_setting.target_level == "Must課題までをマスター"):
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        User は下記のようなカリキュラムを受講します。

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。

                        ## 学習所要時間

                        {course_detail}

                        ## 開始日

                        {current_date}

                        ## 受講期間

                        {target_period}


                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間


                        ## Userの特徴

                        - プログラミング学習が初めてなので、学習のペースが遅いです。
                        - 学習所要時間より大幅に学習時間を必要としています。
                        - 3月10日にlevel3-1を、4月20日に`level5-1` の学習が始められるよう、逆算して計画を立ててください。
                        

                        ## 依頼

                        - 開始日と学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 学習所要時間と学習可能な時間リソースとUserの特徴を考慮して、学習に必要な所要時間を再設定してください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。
                        - 出力フォーマット以外の情報は必要ありません。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
                        """

                    )
                else: #未経験✖️advance課題の人
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        User は下記のようなカリキュラムを受講します。

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。


                        ## 学習所要時間

                        {course_detail}

                        ## 開始日

                        {current_date}

                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間

                        ## 必須要件
                        - 開始日より6ヶ月以内に `level5-2` までを修了する計画である必要があります。

                        ## 依頼

                        - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 学習所要時間と学習可能な時間リソースを考慮して、学習に必要な所要時間を再設定してください。
                        - このユーザーは学習ペースが遅いことを考慮してください。
                        - 各レベルごとにバッファーとして5時間設けて、計画を立案してください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
                        """

                    )
            else: #未経験以外のmust
                if(user_setting.target_level == "Must課題までをマスター"):
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        User は下記のようなカリキュラムを受講します。

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。

                        ## 学習所要時間

                        {course_detail}

                        ## 開始日

                        {current_date}

                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間

                        ## 必須要件
                        - 開始日より6ヶ月以内に `level5-2` までを修了する計画である必要があります。

                        ## 依頼

                        - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 学習所要時間と学習可能な時間リソースを考慮して、学習に必要な所要時間を再設定してください。
                        - このユーザーは学習ペースと理解がとても早いので計画時に考慮してください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
                        """

                    )
                else: #未経験者以外でadvance
                    prompt = PromptTemplate(
                        input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","course_detail"],
                        template="""
                        あなたは User に最適な学習スケジュールを立案する役割を持っています。

                        ## カリキュラム情報

                        User は下記のようなカリキュラムを受講します。

                        - プログラミングの基礎的な内容を学習するカリキュラムです。
                        - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
                        - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
                        - User は曜日ごとに学習可能な時間リソースが異なります。

                        ## 学習所要時間
                        
                        {course_detail}


                        ## 開始日

                        {current_date}


                        ## 学習可能な時間リソース

                        - 月曜日: {monday_study_time}時間
                        - 火曜日: {tuesday_study_time}時間
                        - 水曜日: {wednesday_study_time}時間
                        - 木曜日: {thursday_study_time}時間
                        - 金曜日: {friday_study_time}時間
                        - 土曜日: {saturday_study_time}時間
                        - 日曜日: {sunday_study_time}時間

                        ## 必須要件
                        - 開始日より6ヶ月以内に `level5-2` までを修了する計画である必要があります。

                        ## 依頼

                        - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
                        - 学習所要時間と学習可能な時間リソースを考慮して、学習に必要な所要時間を再設定してください。
                        - このユーザーは学習所要時間は{course_detail}通りです。
                        - 各レベルごとにバッファーとして3時間設けて、計画を立案してください。
                        - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで300文字以内で提示してください。

                        ## 出力フォーマット

                        level0: [yyyy-MM-dd] 
                        level1-1: [yyyy-MM-dd]  
                        level1-2: [yyyy-MM-dd]  
                        level2-1: [yyyy-MM-dd]  
                        level2-2: [yyyy-MM-dd]  
                        level2-3: [yyyy-MM-dd]  
                        level3-1: [yyyy-MM-dd]  
                        level3-2: [yyyy-MM-dd]  
                        level3-3: [yyyy-MM-dd]  
                        level4-1: [yyyy-MM-dd] 
                        level4-2: [yyyy-MM-dd] 
                        level4-3: [yyyy-MM-dd]  
                        level5-1: [yyyy-MM-dd]  
                        level5-2: [yyyy-MM-dd] 
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
        
    #             # 計画内容をデータベースに保存はできるけど、フロントに表示できない。注意；これを使用するときはモデル定義のllm_
    #     for item in plan_items:
    #         new_llm_answer = LLMAnswer(
    #             course_level=item.course_level,
    #             date=dt.strptime(item.date, "%Y-%m-%d").date(),
    #             user_setting_id=user_setting_id  # 仮定: user_setting_idはユーザー設定ID
    #         )
    #         print("new_llm_answer:",new_llm_answer)
    #         db.add(new_llm_answer)
        
    #     db.commit()  # トランザクションのコミット

    #     # 保存した計画内容をフロントエンドに返す
    #     saved_plan = db.query(LLMAnswer).filter(LLMAnswer.user_setting_id == user_setting_id).all()
    #     print("save_plan:",save_plan)
    #     saved_llm_plans = schemas.LLMAnswer(plan=saved_plan) 
    #     print("saved_llm_plans:",saved_llm_plans)
    #     return saved_llm_plans

    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail=str(e))

        llm_answer = schemas.LLMAnswer(plan=plan_items)  # PlanItemリストをLLMAnswerのplanに割り当てる
        return llm_answer  # これを返却する

    except Exception as e:
        # # トランザクションが失敗した場合はロールバック
        # db.rollback()
        logger.error(f"Error in llm-plan: {e}")
        print("Error creating LLM Answer:", e) # エラーログ
        raise HTTPException(status_code=500, detail=str(e))    

# リスタートボタンを作成しようとしています
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
# llm = OpenAI(model_name="gpt-3.5-turbo-instruct" , temperature=0.2)
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
#     print("user_setting_idddddddd:",user_setting_id)
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
#         if line.startswith("level"):
#             # if line.startswith("レベル")
#             parts = line.split(": ")
#             print("Parts after splitting:", parts)
#             course_level = parts[0].strip()  # "レベルX" の "X" 部分
#             # date_range = parts[1].strip().split(" - ")
#             # start_date = dt.strptime(date_range[0], "%Y/%m/%d").strftime("%Y-%m-%d")
#             # end_date = dt.strptime(date_range[1], "%Y/%m/%d").strftime("%Y-%m-%d")
#             # plan_items.append(schemas.PlanItem(course_level=course_level, start_date=start_date, end_date=end_date))

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
#         request_data = await request.json()
#         user_setting_id = request_data.get('user_setting_id')  # リクエストからuser_setting_idを取得
#         if not user_setting_id:
#             raise HTTPException(status_code=400, detail="User setting ID is required")
#         # ユーザー設定をデータベースから取得する
#         user_setting = crud.get_user_setting(db, user_setting_id)
#         if not user_setting:
#             raise HTTPException(status_code=404, detail="User setting not found")
#         print("user_setting:",user_setting)
#         print("Tuesday study time:", user_setting.tuesday_study_time)
#         print("target_period:", user_setting.target_period)
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
#             "learning_history":user_setting.learning_history,
#             "target_level":user_setting.target_level,
#             "course_detail": course_details_dicts
#         }
        
#         prompt = PromptTemplate(
#             input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","learning_history","target_level","course_detail"],
#             template="""
#             あなたは User に最適な学習スケジュールを立案する役割を持っています。

#             ## カリキュラム情報

#             User は下記のようなカリキュラムを受講します。

#             - プログラミングの基礎的な内容を学習するカリキュラムです。
#             - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
#             - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
#             - ユーザの「学習経験」によって学習所要時間には誤差が発生することを想定します。
#             - カリキュラムには、「開始日」と「受講期間」が設けられています。
#             - User は曜日ごとに学習可能な時間リソースが異なります。
#             - 「課題設定」で`advance`課題までをマスターを指定したユーザーには各`level`ごとに3時間を追加した計画が必要です。

#             ## 必須要件
#             - `level` を修了するごとに次の `level`に進み、受講期間内に `level5-2` までを修了する計画である必要があります。


#             ## 学習所要時間
#             {course_detail}

#             ## 開始日

#             {current_date}

#             ## 受講期間

#             {target_period}

#             ## 学習可能な時間リソース

#             - 月曜日: {monday_study_time}時間
#             - 火曜日: {tuesday_study_time}時間
#             - 水曜日: {wednesday_study_time}時間
#             - 木曜日: {thursday_study_time}時間
#             - 金曜日: {friday_study_time}時間
#             - 土曜日: {saturday_study_time}時間
#             - 日曜日: {sunday_study_time}時間

#             ## 学習経験

#             {learning_history}

#             ## 課題設定

#             {target_level}

#             ## 依頼

#             - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
#             - 学習経験が未経験者の場合は計画に余裕を設けてください。
#             - 学習所要時間と学習経験を考慮して、学習に必要な所要時間を再設定してください。
#             - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで提示してください。

#             ## 出力フォーマット

#             - level0: [yyyy-MM-dd] 
#             - level1-1: [yyyy-MM-dd]  
#             - level1-2: [yyyy-MM-dd]  
#             - level2-1: [yyyy-MM-dd]  
#             - level2-2: [yyyy-MM-dd]  
#             - level2-3: [yyyy-MM-dd]  
#             - level3-1: [yyyy-MM-dd]  
#             - level3-2: [yyyy-MM-dd]  
#             - level3-3: [yyyy-MM-dd]  
#             - level4-1: [yyyy-MM-dd] 
#             - level4-2: [yyyy-MM-dd] 
#             - level4-3: [yyyy-MM-dd]  
#             - level5-1: [yyyy-MM-dd]  
#             - level5-2: [yyyy-MM-dd] 

#             """

#         )
#         #level1-2, level2-3, level3-3, level4-3の終了後には、予定に遅れた場合に備えてバッファータイムを設けてください。
#         # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#         chain = LLMChain(llm=llm, prompt=prompt)
#         # LLM　チェーンを実行
#         prediction = chain.run(input_data)
#         print("Prediction:", prediction)
#         # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
#         plan_items = parse_llm_response(prediction.strip())
        
#     #             # 計画内容をデータベースに保存はできるけど、フロントに表示できない。注意；これを使用するときはモデル定義のllm_
#     #     for item in plan_items:
#     #         new_llm_answer = LLMAnswer(
#     #             course_level=item.course_level,
#     #             date=dt.strptime(item.date, "%Y-%m-%d").date(),
#     #             user_setting_id=user_setting_id  # 仮定: user_setting_idはユーザー設定ID
#     #         )
#     #         print("new_llm_answer:",new_llm_answer)
#     #         db.add(new_llm_answer)
        
#     #     db.commit()  # トランザクションのコミット

#     #     # 保存した計画内容をフロントエンドに返す
#     #     saved_plan = db.query(LLMAnswer).filter(LLMAnswer.user_setting_id == user_setting_id).all()
#     #     print("save_plan:",save_plan)
#     #     saved_llm_plans = schemas.LLMAnswer(plan=saved_plan) 
#     #     print("saved_llm_plans:",saved_llm_plans)
#     #     return saved_llm_plans

#     # except Exception as e:
#     #     db.rollback()
#     #     raise HTTPException(status_code=500, detail=str(e))

#         llm_answer = schemas.LLMAnswer(plan=plan_items)  # PlanItemリストをLLMAnswerのplanに割り当てる
#         return llm_answer  # これを返却する

#     except Exception as e:
#         # # トランザクションが失敗した場合はロールバック
#         # db.rollback()
#         logger.error(f"Error in llm-plan: {e}")
#         print("Error creating LLM Answer:", e) # エラーログ
#         raise HTTPException(status_code=500, detail=str(e))    

# def create_new_plan_from_incomplete(replan_response: str)
#     print("replan_response:",replan_response)
#     replan_items = []
#     for line in replan_response.split("\n"):
#         line = line.strip()
#         print("Processing line:", line)  # 処理している行を出力
#         # レスポンスの各行を処理する
#         if line.startswith("level"):
#             # if line.startswith("レベル")
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
#     print("replan_items",replan_items)
#     return replan_items
   


# @app.post("/replan-llm-plan")
# async def replan_llm_plan(user_setting_id: int, db: Session = Depends(get_db)):
#     try:
#         print("Starting generate_study_plan...")  # 処理開始ログ
#         # リクエストボディをJSONとして解析
#         request_data = await request.json()

#         # ユーザー設定とコース情報を取得
#         request_data = await request.json()
#         user_setting_id = request_data.get('user_setting_id')  # リクエストからuser_setting_idを取得
#         if not user_setting_id:
#             raise HTTPException(status_code=400, detail="User setting ID is required")
#         # ユーザー設定をデータベースから取得する
#         user_setting = crud.get_user_setting(db, user_setting_id)
#         if not user_setting:
#             raise HTTPException(status_code=404, detail="User setting not found")
#         print("user_setting:",user_setting)
#         print("Tuesday study time:", user_setting.tuesday_study_time)
#         print("target_period:", user_setting.target_period)
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
#         input_data_tow = {
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
#             "learning_history":user_setting.learning_history,
#             "target_level":user_setting.target_level,
#             "course_detail": course_details_dicts
#         }
        
#         prompt = PromptTemplate(
#             input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","learning_history","target_level","course_detail"],
#             template="""
#             あなたは User に最適な学習スケジュールを立案する役割を持っています。
#             あなたのユーザーは作成した計画通りに学習を行うことができず、再立案を求めています。

#             ## カリキュラム情報

#             User は下記のようなカリキュラムを受講します。

#             - プログラミングの基礎的な内容を学習するカリキュラムです。
#             - カリキュラムは `level` で分割されていて、 `level5-2` まであります。
#             - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
#             - ユーザの「学習経験」によって学習所要時間には誤差が発生することを想定します。
#             - カリキュラムには、「開始日」と「受講期間」が設けられています。
#             - User は曜日ごとに学習可能な時間リソースが異なります。
#             - 「課題設定」で`advance`課題までをマスターを指定したユーザーには各`level`ごとに3時間を追加した計画が必要です。

#             ## 必須要件
#             - `level` を修了するごとに次の `level`に進み、受講期間内に `level5-2` までを修了する計画である必要があります。


#             ## 学習所要時間
#             {course_detail}

#             ## 開始日

#             {current_date}

#             ## 受講期間

#             {target_period}

#             ## 学習可能な時間リソース

#             - 月曜日: {monday_study_time}時間
#             - 火曜日: {tuesday_study_time}時間
#             - 水曜日: {wednesday_study_time}時間
#             - 木曜日: {thursday_study_time}時間
#             - 金曜日: {friday_study_time}時間
#             - 土曜日: {saturday_study_time}時間
#             - 日曜日: {sunday_study_time}時間

#             ## 学習経験

#             {learning_history}

#             ## 課題設定

#             {target_level}

#             ## 依頼

#             - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
#             - 学習経験が未経験者の場合は計画に余裕を設けてください。
#             - 学習所要時間と学習経験を考慮して、学習に必要な所要時間を再設定してください。
#             - 立案する内容は`level3-2`から`level5-2`までを行なってください。
#             - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで提示してください。

#             ## 出力フォーマット
  
#             - level3-2: [yyyy-MM-dd]  
#             - level3-3: [yyyy-MM-dd]  
#             - level4-1: [yyyy-MM-dd] 
#             - level4-2: [yyyy-MM-dd] 
#             - level4-3: [yyyy-MM-dd]  
#             - level5-1: [yyyy-MM-dd]  
#             - level5-2: [yyyy-MM-dd] 

#             """

#         )
#         # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#         chain = LLMChain(llm=llm, prompt=prompt)
#         # LLM　チェーンを実行
#         prediction_replan = chain.run(input_data_tow)
#         print("prediction_replan:", prediction_replan)
#         # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
#         replan_items = create_new_plan_from_incomplete(prediction_replan.strip())



# # LLM立案内容の日付がlevel0: [yyyy/MM/dd] - [yyyy/MM/dd]形になるために作ったコード schemasとmain.py変更必須

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
# llm = OpenAI(model_name="gpt-3.5-turbo-instruct" , temperature=0.2)
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
#     print("user_setting_idddddddd:",user_setting_id)
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
#         if line.startswith("level"):
#             parts = line.split(": ")
#             print("Parts after splitting:", parts)
#             course_level = parts[0].strip()  # "レベルX" の "X" 部分
#             date_range = parts[1].strip().split(" - ")
#             start_date = dt.strptime(date_range[0], "%Y/%m/%d").strftime("%Y-%m-%d")
#             end_date = dt.strptime(date_range[1], "%Y/%m/%d").strftime("%Y-%m-%d")
#             plan_items.append(schemas.PlanItem(course_level=course_level, start_date=start_date, end_date=end_date))

#             # date_str = parts[1].strip()  # "YYYY-MM-DD" 形式の日付文字列
#             # # date = parts[1].strip()  # "YYYY-MM-DD" の部分

#             # # " 1時間"を取り除いて日付部分だけを抽出
#             # date_str = date_str.split(' ')[0]  # 空白で分割して最初の部分（日付）を取得
#             # # 日付の文字列を datetime オブジェクトに変換
#             # date_obj = dt.strptime(date_str, "%Y-%m-%d")
#             # # datetime オブジェクトを YYYY-MM-DD 形式の文字列に再フォーマット
#             # formatted_date = date_obj.strftime("%Y-%m-%d")
#             # plan_items.append(schemas.PlanItem(course_level=course_level, date=formatted_date))
#     print("plan_items",plan_items)
#     return plan_items
   


# @app.post("/llm-plan", response_model=schemas.LLMAnswer)
# async def create_llm_plan(request: Request, db: Session = Depends(get_db)):
#     try:
#         print("Starting generate_study_plan...")  # 処理開始ログ
#         # リクエストボディをJSONとして解析
#         request_data = await request.json()

#         # ユーザー設定とコース情報を取得
#         request_data = await request.json()
#         user_setting_id = request_data.get('user_setting_id')  # リクエストからuser_setting_idを取得
#         if not user_setting_id:
#             raise HTTPException(status_code=400, detail="User setting ID is required")
#         # ユーザー設定をデータベースから取得する
#         user_setting = crud.get_user_setting(db, user_setting_id)
#         if not user_setting:
#             raise HTTPException(status_code=404, detail="User setting not found")
#         print("user_setting:",user_setting)
#         print("Tuesday study time:", user_setting.tuesday_study_time)
#         print("target_period:", user_setting.target_period)
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
#             "learning_history":user_setting.learning_history,
#             "target_level":user_setting.target_level,
#             "course_detail": course_details_dicts
#         }
        
#         prompt = PromptTemplate(
#             input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","learning_history","target_level","course_detail"],
#             template="""
#             あなたは User に最適な学習スケジュールを立案する役割を持っています。

#             ## カリキュラム情報

#             User は下記のようなカリキュラムを受講します。

#             - プログラミングの基礎的な内容を学習するカリキュラムです。
#             - カリキュラムは `level` で分割されていて、`level1-1` から `level5-2` まであります。
#             - カリキュラムは、`level` ごとに必要な「学習所要時間」が設定されています。
#             - ユーザの「学習経験」によって学習所要時間には誤差が発生することを想定します。
#             - カリキュラムには、「開始日」と「受講期間」が設けられています。
#             - User は曜日ごとに学習可能な時間リソースが異なります。
#             - 「課題設定」にて`advance`課題までをマスターを指定したユーザーには各`level`ごとに3時間を追加した計画が必要です。

#             ## 必須要件
#             - `level` を修了するごとに次の `level`に進み、受講期間内に `level5-2` までを修了する計画である必要があります。


#             ## 学習所要時間
#             {course_detail}

#             ## 開始日

#             {current_date}

#             ## 受講期間

#             {target_period}

#             ## 学習可能な時間リソース

#             - 月曜日: {monday_study_time}時間
#             - 火曜日: {tuesday_study_time}時間
#             - 水曜日: {wednesday_study_time}時間
#             - 木曜日: {thursday_study_time}時間
#             - 金曜日: {friday_study_time}時間
#             - 土曜日: {saturday_study_time}時間
#             - 日曜日: {sunday_study_time}時間

#             ## 学習経験

#             {learning_history}

#             ## 課題設定

#             {target_level}

#             ## 依頼

#             - 開始日と受講期間、学習可能な時間リソースから、使える時間リソースをステップバイステップで算出してください。
#             - 学習経験が未経験者の場合は計画に余裕を設けてください。
#             - 学習所要時間と学習経験を考慮して、学習に必要な所要時間を再設定してください。
#             - 上記を考慮して、User に最適な学習スケジュールを下記のフォーマットで提示してください。

#             ## 出力フォーマット

#             - level0: [yyyy-MM-dd] 
#             - level1-1: [yyyy-MM-dd]  
#             - level1-2: [yyyy-MM-dd]  
#             - level2-1: [yyyy-MM-dd]  
#             - level2-2: [yyyy-MM-dd]  
#             - level2-3: [yyyy-MM-dd]  
#             - level3-1: [yyyy-MM-dd]  
#             - level3-2: [yyyy-MM-dd]  
#             - level3-3: [yyyy-MM-dd]  
#             - level4-1: [yyyy-MM-dd] 
#             - level4-2: [yyyy-MM-dd] 
#             - level4-3: [yyyy-MM-dd]  
#             - level5-1: [yyyy-MM-dd]  
#             - level5-2: [yyyy-MM-dd] 

#             """

#         )
#         #level1-2, level2-3, level3-3, level4-3の終了後には、予定に遅れた場合に備えてバッファータイムを設けてください。
#         # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#         chain = LLMChain(llm=llm, prompt=prompt)
#         # LLM　チェーンを実行
#         prediction = chain.run(input_data)
#         print("Prediction:", prediction)
#         # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
#         plan_items = parse_llm_response(prediction.strip())
        
#     #             # 計画内容をデータベースに保存はできるけど、フロントに表示できない。注意；これを使用するときはモデル定義のllm_
#     #     for item in plan_items:
#     #         new_llm_answer = LLMAnswer(
#     #             course_level=item.course_level,
#     #             date=dt.strptime(item.date, "%Y-%m-%d").date(),
#     #             user_setting_id=user_setting_id  # 仮定: user_setting_idはユーザー設定ID
#     #         )
#     #         print("new_llm_answer:",new_llm_answer)
#     #         db.add(new_llm_answer)
        
#     #     db.commit()  # トランザクションのコミット

#     #     # 保存した計画内容をフロントエンドに返す
#     #     saved_plan = db.query(LLMAnswer).filter(LLMAnswer.user_setting_id == user_setting_id).all()
#     #     print("save_plan:",save_plan)
#     #     saved_llm_plans = schemas.LLMAnswer(plan=saved_plan) 
#     #     print("saved_llm_plans:",saved_llm_plans)
#     #     return saved_llm_plans

#     # except Exception as e:
#     #     db.rollback()
#     #     raise HTTPException(status_code=500, detail=str(e))

#         llm_answer = schemas.LLMAnswer(plan=plan_items)  # PlanItemリストをLLMAnswerのplanに割り当てる
#         return llm_answer  # これを返却する

#     except Exception as e:
#         # # トランザクションが失敗した場合はロールバック
#         # db.rollback()
#         logger.error(f"Error in llm-plan: {e}")
#         print("Error creating LLM Answer:", e) # エラーログ
#         raise HTTPException(status_code=500, detail=str(e))    



#一番古いコード　これ使いたい時はget-plan.tsxとschemas.pyの（class PlanItem）変更してね
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
# llm = OpenAI(model_name="gpt-3.5-turbo-instruct" , temperature=0.2)
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
#     print("user_setting_idddddddd:",user_setting_id)
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
#             # print(line.startswith("level"))
#             parts = line.split(": ")
#             print("Parts after splitting:", parts)
#             course_level = parts[0].strip()  # "レベルX" の "X" 部分
#             # date_range = parts[1].strip().split(" - ")
#             # start_date = dt.strptime(date_range[0], "%Y/%m/%d").strftime("%Y-%m-%d")
#             # end_date = dt.strptime(date_range[1], "%Y/%m/%d").strftime("%Y-%m-%d")
#             # plan_items.append(schemas.PlanItem(course_level=course_level, start_date=start_date, end_date=end_date))

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
#         request_data = await request.json()
#         user_setting_id = request_data.get('user_setting_id')  # リクエストからuser_setting_idを取得
#         if not user_setting_id:
#             raise HTTPException(status_code=400, detail="User setting ID is required")
#         # ユーザー設定をデータベースから取得する
#         user_setting = crud.get_user_setting(db, user_setting_id)
#         if not user_setting:
#             raise HTTPException(status_code=404, detail="User setting not found")
#         print("user_setting:",user_setting)
#         print("Tuesday study time:", user_setting.tuesday_study_time)
#         print("target_period:", user_setting.target_period)
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
#             "learning_history":user_setting.learning_history,
#             "course_detail": course_details_dicts
#         }
        
#         prompt = PromptTemplate(
#             input_variables=["current_date","monday_study_time","tuesday_study_time","wednesday_study_time","thursday_study_time","friday_study_time","saturday_study_time","sunday_study_time","target_period","learning_history","course_detail"],
#             template="""
#             あなたは目的を達成するための計画を立案する才能に長けています。
#             今回の依頼は、{learning_history}の学習経験を持ち、プログラミングの勉強を始めた人が{target_period}内にlevel5-2までのコースを完了することを目指しています。各コースレベルの平均所要時間は{course_detail}です。

#             ユーザーの1週間の勉強可能時間は以下の通りです。この時間を基に計画を立て、無駄なく効率的にコースを進められるようにしてください。
#             - 月曜日: {monday_study_time}時間
#             - 火曜日: {tuesday_study_time}時間
#             - 水曜日: {wednesday_study_time}時間
#             - 木曜日: {thursday_study_time}時間
#             - 金曜日: {friday_study_time}時間
#             - 土曜日: {saturday_study_time}時間
#             - 日曜日: {sunday_study_time}時間

#             各コースレベルが特定の日付に割り当てられる学習スケジュールを立案してください。計画は{current_date}の次の日から開始し、level5-2を含む全てのレベルが完了するまでの日程を示してください。計画中、ユーザーの勉強可能時間を超えないよう注意してください。また、各レベルの終了後には、予定に遅れた場合に備えてバッファータイムを設けてください。それぞれのレベルの所要時間を考慮し、スケジュールに反映させてください。

#             スケジュールは以下のフォーマットで提示してください：
#             レベル0: [日付]
#             レベル1-1: [日付]
#             レベル1-2: [日付]
#             ... 以下、各レベルに対応する日付 ...

#             各レベルの勉強時間をユーザーの勉強可能時間に合わせて調整し、最も効率的で実現可能な計画を提案してください。特に、勉強可能時間が0の日は計画を立てないようにしてください。計画はユーザーの目標、勉強可能時間、コース内容を考慮して最適化されるべきです。
#             """

#         )
#         #level1-2, level2-3, level3-3, level4-3の終了後には、予定に遅れた場合に備えてバッファータイムを設けてください。
#         # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
#         chain = LLMChain(llm=llm, prompt=prompt)
#         # LLM　チェーンを実行
#         prediction = chain.run(input_data)
#         print("Prediction:", prediction)
#         # 取得した予測結果を処理してレスポンスモデルに合う形に整形する
#         plan_items = parse_llm_response(prediction.strip())
        
#     #             # 計画内容をデータベースに保存はできるけど、フロントに表示できない。注意；これを使用するときはモデル定義のllm_
#     #     for item in plan_items:
#     #         new_llm_answer = LLMAnswer(
#     #             course_level=item.course_level,
#     #             date=dt.strptime(item.date, "%Y-%m-%d").date(),
#     #             user_setting_id=user_setting_id  # 仮定: user_setting_idはユーザー設定ID
#     #         )
#     #         print("new_llm_answer:",new_llm_answer)
#     #         db.add(new_llm_answer)
        
#     #     db.commit()  # トランザクションのコミット

#     #     # 保存した計画内容をフロントエンドに返す
#     #     saved_plan = db.query(LLMAnswer).filter(LLMAnswer.user_setting_id == user_setting_id).all()
#     #     print("save_plan:",save_plan)
#     #     saved_llm_plans = schemas.LLMAnswer(plan=saved_plan) 
#     #     print("saved_llm_plans:",saved_llm_plans)
#     #     return saved_llm_plans

#     # except Exception as e:
#     #     db.rollback()
#     #     raise HTTPException(status_code=500, detail=str(e))

#         llm_answer = schemas.LLMAnswer(plan=plan_items)  # PlanItemリストをLLMAnswerのplanに割り当てる
#         return llm_answer  # これを返却する

#     except Exception as e:
#         # # トランザクションが失敗した場合はロールバック
#         # db.rollback()
#         logger.error(f"Error in llm-plan: {e}")
#         print("Error creating LLM Answer:", e) # エラーログ
#         raise HTTPException(status_code=500, detail=str(e)) 
