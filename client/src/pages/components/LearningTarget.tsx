//Q4. 1日の学習時間を入力してください
import React, { useState } from 'react';

const LearningTarget: React.FC = () => {
    // 各曜日の学習時間を格納するstate
    const [studyTime, setStudyTime] = useState<number[]>([0, 0, 0, 0, 0, 0, 0]);

    // ボタンの状態を管理するための新しい状態
    const [isRegistered, setIsRegistered] = useState(false);

    // サーバーに学習時間データを送信する関数
    const sendStudyTime = async () => {
        try {
            // 学習時間データをサーバーに送信
            const response = await fetch('http://localhost:8000/api/study_time_4', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ studyTime }),
            });

            // サーバーからのレスポンスをJSON形式で取得
            const data = await response.json();
            console.log('Study time saved:', data);

        } catch (error) {
            // エラーが発生した場合はコンソールに出力
            console.error('Error:', error);
        }
    };
    //table border={1}

    return (
        <div className="flex justify-center items-center text-center">
            <span className="text-inside">
                <h2 className='font-bold text-3xl text-center text-black'>Q4. 1日の学習時間を入力してください</h2>
                <table className="min-w-full bg-white border border-gray-300 text-black">
                    <thead>
                        <tr>
                            <th className="px-4 py-2 border-b">曜日</th>
                            <th className='px-4 py-2 border-b'>時間</th>
                        </tr>
                    </thead>
                    <tbody>
                        {['月', '火', '水', '木', '金', '土', '日'].map((day, index) => (
                            <tr key={index}>
                                <td className="py-2 px-4 border-b">{day}</td>
                                <td className="py-2 px-4 border-b">
                                    <input
                                        type="number"
                                        value={studyTime[index]}
                                        onChange={(e) => {
                                            const newStudyTime = [...studyTime];
                                            newStudyTime[index] = parseInt(e.target.value, 10) || 0;
                                            setStudyTime(newStudyTime);
                                        }}
                                        className="w-16 p-1 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-100"
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <button
                    className={`p-3 rounded-full font-bold transition duration-300 text-black mr-2 ${isRegistered ? 'bg-pink-400' : 'bg-purple-400'}`}
                    onClick={async () => {
                        await sendStudyTime();
                        setIsRegistered(!isRegistered);
                    }}
                >
                    {isRegistered ? '学習時間を保存完了' : '学習時間を保存する'}
                </button>
            </span>
        </div >
    );
};

export default LearningTarget;

// // ボタン変更前　動くコード
// import React, { useState } from 'react';

// const LearningTarget: React.FC = () => {
//     // 各曜日の学習時間を格納するstate
//     const [studyTime, setStudyTime] = useState<number[]>([0, 0, 0, 0, 0, 0, 0]);

//     // サーバーに学習時間データを送信する関数
//     const sendStudyTime = async () => {
//         try {
//             // 学習時間データをサーバーに送信
//             const response = await fetch('http://localhost:8000/api/study_time_4', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ studyTime }),
//             });

//             // サーバーからのレスポンスをJSON形式で取得
//             const data = await response.json();
//             console.log('Study time saved:', data);
//         } catch (error) {
//             // エラーが発生した場合はコンソールに出力
//             console.error('Error:', error);
//         }
//     };
//     //table border={1}

//     return (
//         <div className="flex justify-center items-center text-center">
//             <span className="text-inside">
//                 <h2 className='font-bold text-3xl text-center text-black'>Q4. 1日の学習時間を入力してください</h2>
//                 <table className="min-w-full bg-white border border-gray-300 text-black">
//                     <thead>
//                         <tr>
//                             <th className="px-4 py-2 border-b">曜日</th>
//                             <th className='px-4 py-2 border-b'>時間</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         {['月', '火', '水', '木', '金', '土', '日'].map((day, index) => (
//                             <tr key={index}>
//                                 <td className="py-2 px-4 border-b">{day}</td>
//                                 <td className="py-2 px-4 border-b">
//                                     <input
//                                         type="number"
//                                         value={studyTime[index]}
//                                         onChange={(e) => {
//                                             const newStudyTime = [...studyTime];
//                                             newStudyTime[index] = parseInt(e.target.value, 10) || 0;
//                                             setStudyTime(newStudyTime);
//                                         }}
//                                         className="w-16 p-1 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-100"
//                                     />
//                                 </td>
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//                 <button className={"bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"} onClick={sendStudyTime}>学習時間を保存する</button>
//             </span>
//         </div >
//     );
// };

// export default LearningTarget;