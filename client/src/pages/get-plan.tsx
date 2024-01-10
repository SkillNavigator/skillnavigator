//現在の正規コード
import React, { useState, useEffect } from 'react';

const GetPlan  = () => {
  const [schedules, setSchedules] = useState([]);


  const handlePlanClick = async () => {
  try {
    // 1. ユーザー設定情報を取得
    const userSettingId = 19;
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
        // courseLevel: item.course_level,
        // startDate: item.start_date,
        // endDate: item.end_date
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

  // useEffect(() => {
  //   handlePlanClick(); // コンポーネントがマウントされたらデータを取得
  // }, []); // 空の依存配列を渡して初回のみ実行
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
                {/* <td className="planning-td">{`${schedule.startDate} - ${schedule.endDate}`}</td> */}
                <td className="planning-td">{schedule.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </span>
      <button className="replanning-button" onClick={handlePlanClick}>計画を立案する</button>
      <button className="replanning-button" >計画の再立案</button>
    </div>
  );
};

export default GetPlan ;

//  リスタートボタンを作成しようとしています
// import React, { useState, useEffect } from 'react';

// const GetPlan  = () => {
//   const [schedules, setSchedules] = useState([]);
//   const [reschedules, setreSchedules] = useState([]);

//   const handlePlanClick = async () => {
//   try {
//     // 1. ユーザー設定情報を取得
//     const userSettingId = 19;
//     const userSettingResponse = await fetch(`http://localhost:8000/user-settings/${userSettingId}`);
//     const userSettingData = await userSettingResponse.json();

//     // 2. course_details のデータを取得
//     const courseResponse = await fetch('http://localhost:8000/course-details');
//     const courseData = await courseResponse.json();

//     // 3. LLMに渡して立案を行う（実際のLLM立案処理はサーバー側で実装）
//     const planResponse = await fetch('http://localhost:8000/llm-plan', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ 
//         user_setting_id: userSettingId,
//       }),
//     });
//     const planData = await planResponse.json();
//     console.log("planData:",planData)

//     // planDataが配列を含むオブジェクトであることを確認
//     if (planData && Array.isArray(planData.plan)) {
//       const mappedSchedules = planData.plan.map(item => ({
      
//         courseLevel: item.course_level,
//         date: item.date,
//       }));
//       console.log("Mapped Schedules:", mappedSchedules);
//       setSchedules(mappedSchedules);
//     } else {
//       console.error('Received data is not in the expected format:', planData);
//     }
//   } catch (error) {
//     console.error('Error creating plan:', error);
//   }
//   const rePlanningClick = async () => {
//     try {
//       // 省略: ユーザー設定情報とcourse_detailsの取得
//       // 再計画のためのリクエスト
//       const replanResponse = await fetch('http://localhost:8000/replan-llm-plan', {
//         // 省略: リクエストの設定
//       });
//       const replanData = await replanResponse.json();
//       console.log("Replan Data:", replanData);

//       // planDataが配列を含むオブジェクトであることを確認
//       if (replanData && Array.isArray(replanData.plan)) {
//         const mappedReSchedules = replanData.plan.map(item => ({
//           courseLevel: item.course_level,
//           date: item.date,
//         }));
//         console.log("Mapped ReSchedules:", mappedReSchedules);
//         setReSchedules(mappedReSchedules);
//       } else {
//         console.error('Received data is not in the expected format:', replanData);
//       }
//     } catch (error) {
//       console.error('Error in replanning:', error);
//     }
//   };

//   return (
//     <div>
//       <span className="text-inside">
//         <h2>スケジュール</h2>
//         <table className="planning-table" border={14}>
//           <thead>
//             <tr>
//               <th scope="col" className="planning-th">教材</th>
//               <th scope="col" className="planning-th">実地日</th>
//             </tr>
//           </thead>
//           <tbody>
//             {Array.isArray(schedules) && schedules.map((schedule, index) => (
//               <tr key={index}>
//                 <td className="planning-td">{schedule.courseLevel}</td>
//                 {/* <td className="planning-td">{`${schedule.startDate} - ${schedule.endDate}`}</td> */}
//                 <td className="planning-td">{schedule.date}</td>
//               </tr>
//             ))}
//             {/* 再スケジュールの表示 */}
//             {Array.isArray(reschedules) && reschedules.map((reschedule, index) => (
//               <tr key={`re-${index}`}>
//                 <td className="planning-td">{reschedule.courseLevel}</td>
//                 <td className="planning-td">{reschedule.date}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </span>
//       <button className="replanning-button" onClick={handlePlanClick}>計画を立案する</button>
//       <button className="replanning-button" onClick={rePlanningClick}>計画の再立案</button>
//     </div>
//   );
// };

// export default GetPlan ;


// LLM立案内容の日付がlevel0: [yyyy/MM/dd] - [yyyy/MM/dd]形になるために作ったコード schemasとmain.py変更必須
// import React, { useState, useEffect } from 'react';

// const GetPlan  = () => {
//   const [schedules, setSchedules] = useState([]);


//   const handlePlanClick = async () => {
//   try {
//     // 1. ユーザー設定情報を取得
//     const userSettingId = 15;
//     const userSettingResponse = await fetch(`http://localhost:8000/user-settings/${userSettingId}`);
//     const userSettingData = await userSettingResponse.json();

//     // 2. course_details のデータを取得
//     const courseResponse = await fetch('http://localhost:8000/course-details');
//     const courseData = await courseResponse.json();

//     // 3. LLMに渡して立案を行う（実際のLLM立案処理はサーバー側で実装）
//     const planResponse = await fetch('http://localhost:8000/llm-plan', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ 
//         user_setting_id: userSettingId,
//         // userSetting: userSettingData, 
//         // courseDetails: courseData 
//       }),
//     });
//     const planData = await planResponse.json();
//     console.log("planData:",planData)

//     // planDataが配列を含むオブジェクトであることを確認
//     if (planData && Array.isArray(planData.plan)) {
//       const mappedSchedules = planData.plan.map(item => ({
//         courseLevel: item.course_level,
//         startDate: item.start_date,
//         endDate: item.end_date
//         // courseLevel: item.course_level,
//         // date: item.date,
//       }));
//       console.log("Mapped Schedules:", mappedSchedules);
//       setSchedules(mappedSchedules);
//     } else {
//       console.error('Received data is not in the expected format:', planData);
//     }
//   } catch (error) {
//     console.error('Error creating plan:', error);
//   }
// };

//   // useEffect(() => {
//   //   handlePlanClick(); // コンポーネントがマウントされたらデータを取得
//   // }, []); // 空の依存配列を渡して初回のみ実行
//   return (
//     <div>
//       <span className="text-inside">
//         <h2>スケジュール</h2>
//         <table className="planning-table" border={14}>
//           <thead>
//             <tr>
//               <th scope="col" className="planning-th">教材</th>
//               <th scope="col" className="planning-th">実地日</th>
//             </tr>
//           </thead>
//           <tbody>
//             {Array.isArray(schedules) && schedules.map((schedule, index) => (
//               <tr key={index}>
//                 <td className="planning-td">{schedule.courseLevel}</td>
//                 <td className="planning-td">{`${schedule.startDate} - ${schedule.endDate}`}</td>
//                 {/* <td className="planning-td">{schedule.date}</td> */}
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </span>
//       <button className="replanning-button" onClick={handlePlanClick}>計画を立案する</button>
//     </div>
//   );
// };

// export default GetPlan ;
