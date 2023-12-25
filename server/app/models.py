from sqlalchemy import Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#SQLAlchemyモデルとしての表現を持つFastAPIモデル
class UserSetting(Base):
    __tablename__ = "User Setting"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
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