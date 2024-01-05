
from pydantic import BaseModel
from typing import List

class CourseDetail(BaseModel):
    course_details_id: int
    course_level: str # コースレベル
    duration: float # そのレベルを終えるのに必要な時間

    class Config:
        orm_mode = True


class UserSetting(BaseModel):
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
    course_detail: List[CourseDetail] # コースの詳細（複数のレベル）

    class Config:
        orm_mode = True

#llmの返答の形を固定(PlaniItem,StudyPlanRespone)

class PlanItem(BaseModel):
    course_level: str  # コースのレベル
    date: str  # 日付（YYYY-MM-DD形式）

class LLMAnswer(BaseModel):
    plan: List[PlanItem]