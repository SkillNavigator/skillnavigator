from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Float  
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime

Base = declarative_base()

#SQLAlchemyモデルとしての表現を持つFastAPIモデル
class UserSetting(Base):
    __tablename__ = "user_setting"

    user_setting_id = Column(Integer, primary_key=True, index=True)
    current_date = Column(DateTime)                       #ユーザーが入力した日付と時間
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
    llm_answers = relationship("LLMAnswer", back_populates="user_setting")
    uid = Column(String(50), ForeignKey('users.uid')) #firebase等で使用するid 外部キー
    users = relationship("User", back_populates="user_setting")
    # users_id =Column(Integer, ForeignKey('users.users_id'))  # 正しい外部キーの設定
    # user = relationship("User", back_populates="user_setting")

class CourseDetail(Base):
    __tablename__ = "course_details"

    course_details_id = Column(Integer, primary_key=True, index=True)
    course_level = Column(String(255), unique=True)  # レベルは一意の値
    duration = Column(Float, nullable=False)  # 所要時間
    llm_answers = relationship("LLMAnswer", back_populates="course_details")


class LLMAnswer(Base):
    __tablename__ = "llm_answers"

    llm_answers_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    user_setting_id = Column(Integer, ForeignKey('user_setting.user_setting_id')) 
    user_setting = relationship("UserSetting", back_populates="llm_answers")
    course_details_id = Column(Integer, ForeignKey('course_details.course_details_id'))  # 正しい外部キーの設定
    course_details = relationship("CourseDetail", back_populates="llm_answers")

class User(Base):
    __tablename__ = "users"

    # users_id(Integer, primary_key=True, index=True)
    uid = Column(String(50), primary_key=True, index=True)
    user_name = Column(String(30), nullable=False) 
    user_setting = relationship("UserSetting", back_populates="users")