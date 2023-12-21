#  RESTful API 設計書  
### ホーム画面　
エンドポイント：　/
<br>
## ユーザー関連の機能:  
### 新規ユーザー登録:  
エンドポイント: /api/auth/register  
HTTPメソッド: POST  
リクエスト: {  
  "username": "sakura_tanaka",  
  "email": "sakura@example.com",  
  "password": "secure_password123"  
}  

レスポンス:{  
  message:"新規登録完了しました"  
}  
 <br>
## ログイン  
エンドポイント: /api/auth/login  
HTTPメソッド: POST  
リクエスト:  {  
  "email": "sakura@example.com",  
  "password": "secure_password123"  
}  
レスポンス: {  
    message:"ログインが完了しました"  
}  
<br>
## 設定の登録  
エンドポイント: /api/settings  
HTTPメソッド: POST  
認証: アクセストークン  
リクエスト:  
{  
  "short_or_long_term": "short", // or "long"  
  "learning_schedule": {  
    "course_type": "full_time", // or "night_shift"  
    "weekly_schedule": {  
      "Monday": "2 hours",  
      "Tuesday": "2 hours",  
      "Wednesday": "3 hours",  
      "Thursday": "2 hours",  
      "Friday": "1 hour",  
      "Saturday": "4 hours",  
      "Sunday": "0 hours"  
    },  
    "unavailable_days": ["2023-01-25", "2023-02-10", "2023-03-02"]  
    
  },  
  　"learning_history:experienced
   
  "study_plan": {  
    "must_or_advance": "must", // or "advance"  
    "check_in_schedule": {  
      "Monday": "10:00 AM",  
      "Wednesday": "5:00 PM",  
      "Saturday": "2:00 PM"  
    }  
  }  
  "comments":"3月にBC入学します"  
}  
レスポンス:   
{  
  message:"登録が完了しました"
}  
### 設定の更新  
エンドポイント: /api/settings  
HTTPメソッド: PUT  
認証: アクセストークン  
リクエスト:   
{  
    "unavailable_days": ["2023-03-04"]  
  }  
レスポンス：  
{  
    "unavailable_days": ["2023-01-25", "2023-02-10", "2023-03-02","2023-03-04"]  
  }  
<br>
## 計画立案関連の機能:  

### 計画の取得  
エンドポイント: /api/planning  
HTTPメソッド: GET  
認証: アクセストークン  

レスポンス:   
{  
  "plan_id": "abc123",  
  "current_schedule":  [  
    {  
      "modification_date": "2023-12-15",  
  　　"modification_day": "Monday",  
  　　"learning_item": "Level1",  
  　　"actual_learning_content": "Level2",  
  　　"actual_learning_time": "4 hours"  
    },  
    {  
      "date": "2023-12-16",  
      "day": "Tuesday",  
      "learning_item": "Level3",  
      "actual_learning_content": "Level3",  
      "actual_learning_time": "3 hours"  
    },  
  ]  
}  
<br>
## 計画の修正  

エンドポイント: /api/planning/{plan_id}  
HTTPメソッド: PUT  
認証: アクセストークン  
リクエスト:  
{  
  "modification_date": "2023-12-15",  
  "modification_day": "Monday",  
  "learning_item": "Level1",  
  "actual_learning_time": "4 hours"  
}  

レスポンス: 修正後の学習計画  
{  
  "modified_schedule": [  
    {  
      "modification_date": "2023-12-15",  
  　　"modification_day": "Monday",  
  　　"learning_item": "Level1",  
  　　"actual_learning_time": "4 hours"  
    },  
    {  
      "date": "2023-12-16",  
      "day": "Tuesday",  
      "learning_item": "Level3",  
      "actual_learning_time": "3 hours"  
    },  
    // ... 他の修正されたモジュール  
  ]  
}  
<br>  
## 学習時間記録の機能:  
### 学習記録取得  
エンドポイント: /api/learning-log  
HTTPメソッド: GET  
認証: アクセストークン  
レスポンス：  
{  
  "date": "2023-12-15",  
  "learning_log": [  
    {  
      "learning_item": "Lesson1",  
      "learning_time": "4 hours"  
    },  
  ]  
}  
### 学習時間の記録更新  
リクエスト:  
エンドポイント: /api/learning-log/update  
HTTPメソッド: POST  
認証: アクセストークン  
リクエスト：  
{  
  "date": "2023-12-15",  
  "learning_log": [  
    {  
      "learning_item": "Lesson1",  
      "learning_time": "5 hours"  
    },  
  ]  
}  
レスポンス：  
{  
  "date": "2023-12-15",  
  "learning_log": [  
    {  
      "learning_item": "Lesson1",  
      "learning_time": "5 hours"  
    },  
    {  
      "learning_item": "Lesson2",  
      "learning_time": "6 hours"  
    },  
    // ... 他の学習ログ  
  ]  
}  
<br>
## 学習実績機能  
### 学習実績取得  
エンドポイント: /api/learning-achievements  
HTTPメソッド: GET  
認証: アクセストークン  
レスポンス  

{  
  "learning_records": [  
    {  
      "date": "2023-12-15",  
      "learning_time": "4 hours",  
      "difference_from_previous_day": "1 hour less"  
    },  
    {  
      "date": "2023-12-16",  
      "learning_time": "3 hours",  
      "difference_from_previous_day": "1 hour more"  
    },  
    // ... 他の学習実績  
  ],  
  "weekly_total": "20 hours"  
}  