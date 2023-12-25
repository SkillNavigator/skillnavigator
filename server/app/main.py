import uvicorn
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import openai
import os
import datetime
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from pydantic import BaseModel
# LLM チェーンをインポート
from langchain.chains import LLMChain #これをコメントアウトすると候補が１つしか出なくなる


# FastAPIアプリケーションが初期化
app = FastAPI()

# 環境変数を読み込む
load_dotenv()  

#OpenAIのAPIキーを環境変数から取得
openai_api_key = os.getenv("OPENAI_API_KEY") 
#初期化　temperature揺れる回答を小さい数字で揺れなくしてる
#llmのインスタンスを作るときにモデルを定義　text-davinci-003temperature=0.7
llm = OpenAI(model_name="text-davinci-003" , temperature=0.7)
# 今日の日付を取得
current_date = datetime.date.today().isoformat()  # YYYY-MM-DD形式

# CORSミドルウェアを追加・異なるオリジンからのリクエストを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ここで許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],  # ここで許可するHTTPメソッドを指定
    allow_headers=["*"],  # ここで許可するHTTPヘッダーを指定
)

# リクエストボディの構造を定義するPydanticモデルを作成します。
class CourseDetail(BaseModel):
    level: str # コースレベル
    duration: float # そのレベルを終えるのに必要な時間

class StudyPlanRequest(BaseModel):
    current_date: str # 現在の日付
    availability: Dict[str, int] # 利用可能な勉強時間（曜日ごと）
    course_duration: str #(３ヶ月・６ヶ月)
    course_details: List[CourseDetail] # コースの詳細（複数のレベル）
    buffer_time: int #バッファー時間　levelごとに２時間とる


@app.post("/generate-study-plan")
async def generate_study_plan(request_body: StudyPlanRequest):
    # try:
        # LLMに送るプロンプトを作成
        # prompt = (
        #     "私は、特定のユーザーのために個別化された学習スケジュールを作成したいと考えています。ユーザーは、{course_duration}のコース期間で、レベル0からレベル5までのコーディングコースを受講予定です。各レベルには異なる量のコース内容と所要時間があります。ユーザーは曜日によって異なる勉強可能時間を提供しており、最適な勉強スケジュールを希望しています。\n"
        #     "ユーザーは以下のような勉強可能時間を提供しています：{availability}。選択したコース期間は{course_duration}です。コース内容と所要時間は次のとおりです：{course_details}。\n"
        #     "ユーザーが計画より遅れた場合に備えて、各レベル終了後には2時間のバッファー時間を秘匿的に組み込んでください。これにより、計画は実際の勉強時間よりも柔軟性を持ち、ユーザーが予定に遅れた場合でも調整が可能です。\n"
        #     "これらの情報を基に、ユーザーが時間内で効率よくコースを完了できるような個別化された学習スケジュールを作成してください。計画には、各レベルをどのように配置するか、各日に何時間勉強するか、どのレベルをいつ学ぶか、そして各レベル終了後のバッファー時間の秘匿的な組み込みを含めてください。"
        # ).format(
        #     course_duration=request_body.course_duration,
        #     availability=request_body.availability,
        #     course_details=request_body.course_details,
        #     buffer_time=request_body.buffer_time
        # )


        # 実際のデータでプロンプトをフォーマット
        # prompt = prompt_template.format(
        #     course_duration="3ヶ月",  # または "6ヶ月"
        #     availability=str(user_availability),  # ユーザーの提供する曜日ごとの時間
        #     course_details=str(course_details),  # データベースから取得したコースの内容と所要時間
        #     buffer_time=str(buffer_time)
        # )
    # # プロンプトテンプレートの作成
    # prompt = PromptTemplate(
    #     input_variables=["product"],
    #     template="{product}を作る会社の社名として、何かいいものはないですか？日本語の社名でお願いします。",
    # )

    prompt = PromptTemplate(
        input_variables=["current_date","availability","course_duration","course_details","buffer_time"],
        template="""
        今日は{current_date}です。私は、特定のユーザーのために{course_duration}のコース期間内で完了する個別化された学習スケジュールを作成しています。各レベルのコース内容と所要時間は{course_details}で、ユーザーの勉強可能時間は{availability}です。

        私のタスクは、これらの情報を基にして、各コースレベルが特定の日付に割り当てられるようなスケジュールを立案することです。スケジュールは、具体的な日付と、その日に行うべきレベルを示す形式であるべきです。各レベルの勉強が終わるごとに次のレベルに進み、全てのレベルが終了するまでの計画を立ててください。各レベルに対して実際に勉強する日程は複数ある場合があります。

        以下のようにスケジュールを提示してください：

        レベル0: [日付]
        レベル1-1: [日付]
        レベル1-2: [日付]
        ... 以下、各レベルに対応する日付 ...

        各レベルの所要時間とユーザーの利用可能時間を考慮し、実際に勉強が行われる日を割り当ててください。計画のスタート日は現在の日付の次の日からにしてください。
        また、各レベル終了後には、ユーザーが予定に遅れた場合に備えてバッファー時間を秘匿的に組み込んでください。

        """


        # template="""
        # 今日は{current_date}です。私は、特定のユーザーのために{course_duration}のコース期間内で完了する個別化された学習スケジュールを作成したいと考えています。ユーザーはレベル0からレベル5までのコーディングコースを受講予定で、各レベルには異なるコース内容と所要時間があります。\n
        # ユーザーの勉強可能時間は以下の通りです：{availability}。\n
        # コース内容と各レベルの所要時間は次のとおりです：{course_details}。\n
        # 各レベルの学習には具体的な日付を割り当ててください。スケジュールは{current_date}の次の日から開始し、ユーザーの利用可能時間を考慮しつつ、各レベルを適切な日に割り当ててください。レベルが終了するごとに、バッファー時間{buffer_time}時間を秘匿的に組み込んで、計画の遅れに対応できるようにしてください。\n
        # 各レベルの勉強が終わるごとに次のレベルに進んでください。全てのレベルが終了した時点で、ユーザーが{course_duration}内に効率的にコースを完了できるような学習スケジュールを提案してください。スケジュールは具体的な日付と、その日に行うべきレベルと所要時間を示すこと。\n
        # 最終的なスケジュールは、実際のカレンダー日付を含む、完全な学習プランを示すべきです。
        # """
    )

    # # LLM チェーンを実行するための入力データ
    # input_data = {
    #     "current_date": "current_date", #datetime.date.today().isoformat()
    #     "availability": {"Monday": 1, "Tuesday": 1 ,"Wednesday": 2, "Thursday": 1,"Friday": 1, "Saturday": 5 , "Sunday":4},
    #     "course_duration": "3ヶ月",
    #     "course_details": [
    #         {"level": "0", "duration": 1},
    #         {"level": "1-1", "duration": 0.5},
    #         {"level": "1-2", "duration": 2.5},
    #         {"level": "2-1", "duration": 5},
    #         {"level": "2-2", "duration": 2},
    #         {"level": "2-3", "duration": 2},
    #         {"level": "3-1", "duration": 4},
    #         {"level": "3-2", "duration": 4},
    #         {"level": "3-3", "duration": 2},
    #         {"level": "4-1", "duration": 6},
    #         {"level": "4-2", "duration": 6},
    #         {"level": "4-3", "duration": 10},
    #         {"level": "5-1", "duration": 1},
    #         {"level": "5-2", "duration": 14}
    #     ],
    #     "buffer_time": 2
    #     }

    # LLM チェーンを実行するための入力データをユーザーのリクエストから構築(Next.jsができたらこっちに変更)
    input_data = {
        "current_date": request_body.current_date,
        "availability": request_body.availability,
        "course_duration": request_body.course_duration,
        "course_details": request_body.course_details,
        "buffer_time": request_body.buffer_time
    }


    # LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
    chain = LLMChain(llm=llm, prompt=prompt)

    # LLM　チェーンを実行
    prediction = chain.run(input_data)
    print(prediction.strip())

    response = prediction

    return response





# #下記大事


#     # # LLM から予測を受け取って表示
#     # prediction = llm(prompt)
#     # print(prediction.strip())

#     #     # レスポンスがテキストを含むかどうかをチェック
#     #     if not response.choices or not response.choices[0].text.strip():
#     #         raise HTTPException(status_code=500, detail="Failed to generate study plan")

#     # except Exception as e:
#     #     # 本番環境では、エラーの詳細をログに記録するなどの処理を行う
#     #     print(f"Error: {e}")
#     #     # 例えば: logger.error(f"Error: {e}")
#     #     # ユーザーには一般的なエラーメッセージを返す
#     #     raise HTTPException(status_code=500, detail="An error occurred while generating the study plan.")



# #テスト
# import uvicorn
# from fastapi import FastAPI, HTTPException
# from dotenv import load_dotenv
# from langchain.llms import OpenAI
# from langchain import PromptTemplate
# from typing import Dict, List
# import openai
# import os
# from langchain.chat_models import ChatOpenAI
# from pydantic import BaseModel
# # LLM チェーンをインポート
# from langchain.chains import LLMChain 

# # FastAPIアプリケーションが初期化
# app = FastAPI()

# # 環境変数を読み込む
# load_dotenv()  

# #OpenAIのAPIキーを環境変数から取得
# openai_api_key = os.getenv("OPENAI_API_KEY") 
# #初期化　temperature揺れる回答を小さい数字で揺れなくしてる
# #llmのインスタンスを作るときにモデルを定義　text-davinci-003
# llm = OpenAI(temperature=0.7)

# # リクエストボディの構造を定義するPydanticモデルを作成します。
# class CourseDetail(BaseModel):
#     level: str
#     duration: float

# class StudyPlanRequest(BaseModel):
#     availability: Dict[str, int]
#     course_duration: str
#     course_details: List[CourseDetail]
#     buffer_time: int

# @app.post("/generate-study-plan")
# async def generate_study_plan(request_body: StudyPlanRequest):
#      # プロンプトテンプレートの作成
#     prompt = PromptTemplate(
#         input_variables=["product"],
#         template="{product}を作る会社の社名として、何かいいものはないですか？日本語の社名でお願いします。",
#     )

#    # やり方１　テンプレートからプロンプトを作成
#     prompt = prompt.format(product="カラフルな靴下")
#     print(prompt)
#         #LLMにプロンプトを送信
#     response = llm(prompt)
#         #応答を返す
#     return response

    #　#やり方２　LLM チェーンを作成（LLM ラッパーとプロンプトテンプレートから構成する）
    # chain = LLMChain(llm=llm, prompt=prompt)

    # # LLM　チェーンを実行
    # prediction = chain.run("カラフルな靴下")
    # print(prediction.strip())

    # response = prediction
    # return response


# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

