import React, { useState } from 'react';

interface CompletionStatus {
    [key: number]: boolean;
}

const data = [
    { title: "level0-1 イントロダクション・基礎学習について", estimatedTime: 1 },
    { title: "level1-1 環境構築", estimatedTime: 0.5 },
    { title: "level1-2 データ型・演算子・変数", estimatedTime: 2.5 },
    { title: "level2-1 関数", estimatedTime: 5 },
    { title: "level2-2 より良いコードを書くには？", estimatedTime: 2 },
    { title: "level2-3 比較", estimatedTime: 2 },
    { title: "level3-1 条件分岐①", estimatedTime: 4 },
    { title: "level3-2 条件分岐②・演算子・変数", estimatedTime: 4 },
    { title: "level3-3 スコープ", estimatedTime: 2 },
    { title: "level4-1 配列", estimatedTime: 6 },
    { title: "level4-2 オブジェクト", estimatedTime: 6 },
    { title: "level4-3 forループ", estimatedTime: 10 },
    { title: "level5-1 HTML・CSSの基礎知識", estimatedTime: 1 },
    { title: "level5-2 HTML・CSS演習（My IRページ）", estimatedTime: 14 }
];

const ReferenceSchedule: React.FC = () => {
    const [completionStatus, setCompletionStatus] = useState<CompletionStatus>({});

    const handleCompletionClick = async (rowIndex: number) => {
        setCompletionStatus((prevStatus) => ({
            ...prevStatus,
            [rowIndex]: !prevStatus[rowIndex],
        }));
    }


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

    //コンソール上に完了・未完了を表示する
    const handlePrintCompletionStatus = async () => {
        console.log("各行の完了状態:");
        data.forEach((row, index) => {
            console.log(`${row.title}: ${completionStatus[index] ? "完了" : "未完了"}`);
        });

        try {
            //サーバーにデータを送信
            const response = await fetch('http://localhost:8000/api/saveCompletionStatus', {
                method: 'POST',
                //リクエストのヘッダーでJSON形式のデータを指定
                headers: {
                    'Content-Type': 'application/json',
                },
                // completionStatusオブジェクトをJSON文字列に変換してリクエストボディに設定
                body: JSON.stringify(completionStatus),
            });
            // サーバーからのレスポンスをJSON形式で取得
            const data = await response.json();
            //取得したデータをコンソールに出力
            console.log('完了か否か:', data);
            console.log(completionStatus)
        } catch (error) {
            // エラーが発生した場合はコンソールに出力
            console.error('Error:', error);
        }
    }

    return (
        <div className="square-container">
            <span className="text-inside">
                <h2 className='font-bold mt-8 mb-5 text-2xl text-blue-500'>参考スケジュール</h2>
                <table className="min-w-full bg-white border border-gray-300">
                    <thead>
                        <tr className='text-black'>
                            <th className="px-4 py-2 border-b">教材・チェックイン</th>
                            <th className="px-4 py-2 border-b">想定所要時間（時間）</th>
                            <th className="px-4 py-2 border-b">完了したらボタンを押してください</th>
                        </tr>
                    </thead>
                    <tbody className='text-black'>
                        {data.map((row, index) => (
                            <tr key={index}>
                                <td className="px-4 py-2 border-b">{row.title}</td>
                                <td className="px-4 py-2 border-b text-center">{row.estimatedTime}</td>
                                <td className="px-4 py-2 border-b text-center">
                                    <button 
                                        className={`p-3 rounded-full font-bold transition duration-300 text-black p-1 ${completionStatus[index] ? 'bg-pink-400' : 'bg-purple-400 hover:bg-pink-400'}`}
                                        onClick={() => handleCompletionClick(index)}
                                    >
                                        {completionStatus[index] ? '完了' : '未完了'}
                                    </button>
                                </td>
                            </tr>
                        ))}
                     </tbody>
                 </table>
            </span>
         </div>
    );
};

export default ReferenceSchedule;


// import React, { useState } from 'react';

// interface CompletionStatus {
//     [key: number]: boolean;
// }

// const data = [
//     { title: "level0-1 イントロダクション・基礎学習について", estimatedTime: 1 },
//     { title: "level1-1 環境構築", estimatedTime: 0.5 },
//     { title: "level1-2 データ型・演算子・変数", estimatedTime: 2.5 },
//     { title: "level2-1 関数", estimatedTime: 5 },
//     { title: "level2-2 より良いコードを書くには？", estimatedTime: 2 },
//     { title: "level2-3 比較", estimatedTime: 2 },
//     { title: "level3-1 条件分岐①", estimatedTime: 4 },
//     { title: "level3-2 条件分岐②・演算子・変数", estimatedTime: 4 },
//     { title: "level3-3 スコープ", estimatedTime: 2 },
//     { title: "level4-1 配列", estimatedTime: 6 },
//     { title: "level4-2 オブジェクト", estimatedTime: 6 },
//     { title: "level4-3 forループ", estimatedTime: 10 },
//     { title: "level5-1 HTML・CSSの基礎知識", estimatedTime: 1 },
//     { title: "level5-2 HTML・CSS演習（My IRページ）", estimatedTime: 14 }
// ];

// const ReferenceSchedule: React.FC = () => {
//     const [completionStatus, setCompletionStatus] = useState<CompletionStatus>({});

//     const handleCompletionClick = async (rowIndex: number) => {
//         setCompletionStatus((prevStatus) => ({
//             ...prevStatus,
//             [rowIndex]: !prevStatus[rowIndex],
//         }));
//     }


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

//     //コンソール上に完了・未完了を表示する
//     const handlePrintCompletionStatus = async () => {
//         console.log("各行の完了状態:");
//         data.forEach((row, index) => {
//             console.log(`${row.title}: ${completionStatus[index] ? "完了" : "未完了"}`);
//         });

//         try {
//             //サーバーにデータを送信
//             const response = await fetch('http://localhost:8000/api/saveCompletionStatus', {
//                 method: 'POST',
//                 //リクエストのヘッダーでJSON形式のデータを指定
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 // completionStatusオブジェクトをJSON文字列に変換してリクエストボディに設定
//                 body: JSON.stringify(completionStatus),
//             });
//             // サーバーからのレスポンスをJSON形式で取得
//             const data = await response.json();
//             //取得したデータをコンソールに出力
//             console.log('完了か否か:', data);
//             console.log(completionStatus)
//         } catch (error) {
//             // エラーが発生した場合はコンソールに出力
//             console.error('Error:', error);
//         }
//     }

//     return (
//         <div className="square-container">
//             <span className="text-inside">
//                 <h2>参考スケジュール</h2>
//                 <table border='1'>
//                     <thead>
//                         <tr>
//                             <th>教材・チェックイン</th>
//                             <th>想定所要時間（時間）</th>
//                             <th>完了したらボタンを押してください</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         {data.map((row, index) => (
//                             <tr key={index}>
//                                 <td>{row.title}</td>
//                                 <td>{row.estimatedTime}</td>
//                                 <td>
//                                     <button onClick={() => handleCompletionClick(index)}>
//                                         完了
//                                     </button>{" "}
//                                     {completionStatus[index] && "完了"}
//                                 </td>
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//                 <button onClick={handlePrintCompletionStatus}>
//                     コンソールに完了状態を表示
//                 </button>
//             </span>
//         </div>
//     );
// };

// export default ReferenceSchedule;