from sqlalchemy.orm import Session
from .models import CourseDetail, UserSetting, LLMAnswer
from sqlalchemy.orm import joinedload


#コースのデフォルト情報を取得
def get_course_details(db: Session):
    return db.query(CourseDetail).all()

#コース内容の変更がある場合のために記入
def create_course_detail(db: Session, course_detail_data):
    course_detail = CourseDetail(**course_detail_data)
    db.add(course_detail)
    db.commit()
    db.refresh(course_detail)
    return course_detail

#ユーザー設定を取得
def get_user_setting(db: Session, user_setting_id: int):
    return db.query(UserSetting).filter(UserSetting.user_setting_id == user_setting_id).first()

#LLMが立案した計画をデータベースに保存
def create_llm_answer(db: Session, llm_answer_data):
    llm_answer = LLMAnswer(**llm_answer_data)
    db.add(llm_answer)
    db.commit()
    db.refresh(llm_answer)
    return llm_answer

# def get_llm_answers_by_user_setting(db: Session, user_setting_id: int):
#     return db.query(LLMAnswer).filter(LLMAnswer.user_setting_id == user_setting_id).all()

def get_llm_answers_by_user_setting(db: Session, user_setting_id: int):
    return db.query(LLMAnswer).options(joinedload(LLMAnswer.course_details)).filter(LLMAnswer.user_setting_id == user_setting_id).all()