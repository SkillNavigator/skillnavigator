import React, { useState, useEffect } from 'react';

const Schedules = () => {
  const [schedules, setSchedules] = useState([]);

  const fetchLLMPlans = async () => {
    try {
      // course_details のデータを取得
      const courseResponse = await fetch('http://localhost:8000/course-details');
      const courseData = await courseResponse.json();
      
      // llm_answers のデータを取得
      // const userSettingId = useContext(UserContext).id; // これは例。実際のコンテキストやステート管理方法に応じて調整必須
      const userSettingId = "1"; // 実際のユーザー設定IDに置き換えてください
      const llmResponse = await fetch(`http://localhost:8000/user-settings/${userSettingId}/llm-answers`);;
      const llmData = await llmResponse.json();

      // 取得したデータをマッピングしてスケジュールを設定
      const mappedSchedules = llmData.map(llm => {
        // course_details から対応する教材を見つける
        const courseDetail = courseData.find(detail => detail.course_details_id === llm.course_details_id);
        return {
          courseLevel: courseDetail ? courseDetail.course_level : '未定義の教材',
          date: llm.date // この形式は仮定しています。実際のデータに合わせて調整してください。
        };
      });
      setSchedules(mappedSchedules);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };
  useEffect(() => {
    fetchLLMPlans(); // コンポーネントがマウントされたらデータを取得
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
            {schedules.map((schedule, index) => (
              <tr key={index}>
                <td className="planning-td">{schedule.courseLevel}</td>
                <td className="planning-td">{schedule.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </span>
      <button className="replanning-button" onClick={fetchLLMPlans}>計画を立案する</button>
    </div>
  );
};

export default Schedules;

// べた書きコード


// import React, { useState } from 'react';

// const initialSchedules = [
//     { title: "level0 イントロダクション・基礎学習について", date: ["2023-12-24"] },
//     { title: "level1-1 環境構築", date: ["2023-12-24"] },
//     { title: "level1-2 データ型・演算子・変数", date: ["2023-12-24"] },
//     { title: "level2-1 関数", date: ["2023-12-25","2023-12-26","2023-12-27","2023-12-28","2023-12-29","2023-12-30"]},
//     { title: "level2-2 より良いコードを書くには？", date: ["2023-12-30"] },
//     { title: "level2-3 比較", date: ["2023-12-30"]},
//     { title: "level3-1 条件分岐①", date: ["2023-12-31","2024-01-01","2024-01-02"] },
//     { title: "level3-2 条件分岐②・演算子・変数", date: ["2024-01-03","2024-01-04","2024-01-05"]},
//     { title: "level3-3 スコープ", date: ["2024-01-06"]},
//     { title: "level4-1 配列", date: ["2024-01-06","2024-01-07","2024-01-08"]},
//     { title: "level4-2 オブジェクト", date: ["2024-01-09","2024-01-10","2024-01-11","2024-01-12"]},
//     { title: "level4-3 forループ", date: ["2024-01-13","2024-01-14","2024-01-15","2024-01-16","2024-01-17"]},
//     { title: "level5-1 HTML・CSSの基礎知識", date: ["2024-01-17"]},
//     { title: "level5-2 HTML・CSS演習（My IRページ）", date: ["2024-01-18","2024-01-19","2024-01-20","2024-01-21","2024-01-22","2024-01-23","2024-01-24","2024-01-25"]}
// ];


// const Schedules: React.FC = () => {
//     const [schedules, setSchedules] = useState(initialSchedules);
//     const handleDateChange = (index: number, newDate: string) => {
//         setSchedules((prevSchedules) => {
//             const updatedSchedules = [...prevSchedules];
//             updatedSchedules[index].date = newDate;
//             return updatedSchedules;
//         });
//     };

//     return (
//         <div>
//             <span className="text-inside">
//                 <h2>スケジュール</h2>
//                 <table className="planning-table" border={14}>
//                     <thead>
//                         <tr>
//                             <th scope="col" className="planning-th">教材</th>
//                             <th scope="col" className="planning-th">実地日</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         {schedules.map((schedule, index) => (
//                             <tr key={index}>
//                                 <td className="planning-td">{schedule.title}</td>
//                                 <td className="planning-td">
//                                     <input
//                                         type="date"
//                                         value={schedule.date || ''}
//                                         onChange={(e) => {
//                                             const newDate = e.target.value;
//                                             handleDateChange(index, newDate); // ハンドラーを呼び出す
//                                         }}
//                                     />
//                                 </td>
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//             </span>
//             <button className="replanning-button">現在のスケジュールを修正する</button>
//         </div>
//     );
// };

// export default Schedules;