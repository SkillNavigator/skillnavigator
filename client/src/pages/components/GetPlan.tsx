import React, { useState, useEffect } from 'react';

const GetPlan  = () => {
  const [schedules, setSchedules] = useState([]);

  const handlePlanClick = async () => {
  try {
    // 1. ユーザー設定情報を取得
    const userSettingId = 1; // 仮　実際はユーザー認証システムからこのIDを取得し、それを用いてサーバーからユーザー設定を取得
    const userSettingResponse = await fetch(`http://localhost:8000/user-settings/${userSettingId}`);
    const userSettingData = await userSettingResponse.json();

    // 2. course_details のデータを取得
    const courseResponse = await fetch('http://localhost:8000/course-details');
    const courseData = await courseResponse.json();

    // 3. LLMに渡して立案を行う（実際のLLM立案処理はサーバー側で実装）
    const planResponse = await fetch('http://localhost:8000/llm-plan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        user_setting_id: userSettingId,
        // userSetting: userSettingData, 
        // courseDetails: courseData 
      }),
    });
    const planData = await planResponse.json();
    console.log("planData:",planData)

    // planDataが配列を含むオブジェクトであることを確認
    if (planData && Array.isArray(planData.plan)) {
      const mappedSchedules = planData.plan.map(item => ({
        courseLevel: item.course_level,
        date: item.date,
      }));
      console.log("Mapped Schedules:", mappedSchedules);
      setSchedules(mappedSchedules);
    } else {
      console.error('Received data is not in the expected format:', planData);
    }
  } catch (error) {
    console.error('Error creating plan:', error);
  }
};
//     // 取得したデータをマッピングしてスケジュールを設定
//     const mappedSchedules = planData.map(llm => {
//       // course_details から対応する教材を見つける
//       const courseDetail = courseData.find(detail => detail.course_details_id === llm.course_details_id);
//       return {
//         courseLevel: courseDetail ? courseDetail.course_level : '未定義の教材',
//         date: llm.date // この形式は仮定しています。実際のデータに合わせて調整してください。
//       };
//     });
//     // 4. 立案結果をステートにセットして表示
//     setSchedules(mappedSchedules);
//   } catch (error) {
//     console.error('Error creating plan:', error);
//   }
// };
  useEffect(() => {
    handlePlanClick(); // コンポーネントがマウントされたらデータを取得
  }, []); // 空の依存配列を渡して初回のみ実行
  return (
    <div>
      <span className="text-inside">
        <h2>スケジュール</h2>
        <table className="planning-table" border={14}>
          <thead>
            <tr>
              <th scope="col" className="planning-th">教材</th>
              <th scope="col" className="planning-th">実地日</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(schedules) && schedules.map((schedule, index) => (
              <tr key={index}>
                <td className="planning-td">{schedule.courseLevel}</td>
                <td className="planning-td">{schedule.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </span>
      <button className="replanning-button" onClick={handlePlanClick}>計画を立案する</button>
    </div>
  );
};

export default GetPlan ;
