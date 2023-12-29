import React, { useState } from 'react';

const initialSchedules = [
    { title: "level0 イントロダクション・基礎学習について", date: ["2023-12-24"] },
    { title: "level1-1 環境構築", date: ["2023-12-24"] },
    { title: "level1-2 データ型・演算子・変数", date: ["2023-12-24"] },
    { title: "level2-1 関数", date: ["2023-12-25","2023-12-26","2023-12-27","2023-12-28","2023-12-29","2023-12-30"]},
    { title: "level2-2 より良いコードを書くには？", date: ["2023-12-30"] },
    { title: "level2-3 比較", date: ["2023-12-30"]},
    { title: "level3-1 条件分岐①", date: ["2023-12-31","2024-01-01","2024-01-02"] },
    { title: "level3-2 条件分岐②・演算子・変数", date: ["2024-01-03","2024-01-04","2024-01-05"]},
    { title: "level3-3 スコープ", date: ["2024-01-06"]},
    { title: "level4-1 配列", date: ["2024-01-06","2024-01-07","2024-01-08"]},
    { title: "level4-2 オブジェクト", date: ["2024-01-09","2024-01-10","2024-01-11","2024-01-12"]},
    { title: "level4-3 forループ", date: ["2024-01-13","2024-01-14","2024-01-15","2024-01-16","2024-01-17"]},
    { title: "level5-1 HTML・CSSの基礎知識", date: ["2024-01-17"]},
    { title: "level5-2 HTML・CSS演習（My IRページ）", date: ["2024-01-18","2024-01-19","2024-01-20","2024-01-21","2024-01-22","2024-01-23","2024-01-24","2024-01-25"]}
];


const Schedules: React.FC = () => {
    const [schedules, setSchedules] = useState(initialSchedules);
    const handleDateChange = (index: number, newDate: string) => {
        setSchedules((prevSchedules) => {
            const updatedSchedules = [...prevSchedules];
            updatedSchedules[index].date = newDate;
            return updatedSchedules;
        });
    };

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
                                <td className="planning-td">{schedule.title}</td>
                                <td className="planning-td">
                                    <input
                                        type="date"
                                        value={schedule.date || ''}
                                        onChange={(e) => {
                                            const newDate = e.target.value;
                                            handleDateChange(index, newDate); // ハンドラーを呼び出す
                                        }}
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </span>
            <button className="replanning-button">現在のスケジュールを修正する</button>
        </div>
    );
};

export default Schedules;

// import React, { useState, useEffect } from 'react';

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

// // const Planning: React.FC = () => {
// //     const [schedules, setSchedules] = useState([]);
  
// //     useEffect(() => {
// //       // APIからデータをフェッチする関数
// //       const fetchSchedules = async () => {
// //         const response = await fetch('http://localhost:8000/initialSchedules');
// //         const data = await response.json();
// //         setSchedules(data);
// //       };
  
// //       fetchSchedules();
// //     }, []); // 空の依存配列で、コンポーネントがマウントされた時に一度だけ実行
  

// const Planning: React.FC = () => {
//     const [schedules, setSchedules] = useState(initialSchedules);

//     //  日程を更新する関数
//     const updateDate = (scheduleIndex, dateIndex, newDate) => {
//         // スケジュールのディープコピーを作成
//         const newSchedules = schedules.map((schedule, idx) => {
//             if (idx === scheduleIndex) {
//                 // 日程の配列を更新
//                 const newDates = [...schedule.date];
//                 newDates[dateIndex] = newDate;
//                 return { ...schedule, dates: newDates };
//             }
//             return schedule;
//         });

//         // 更新したスケジュールで状態を更新
//         setSchedules(newSchedules);
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
//                         {schedules.map((schedule, scheduleIndex) => (
//                             <tr key={scheduleIndex}>
//                                 <td className="planning-td">{schedule.title}</td>
//                                 <td className="planning-td">
//                                     {schedule.date.map((date, dateIndex) => (
//                                         <input
//                                             key={dateIndex}
//                                             type="date"
//                                             value={date || ''}
//                                             onChange={(e) => updateDate(scheduleIndex, dateIndex, e.target.value)}
//                                         />
//                                     ))}
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
