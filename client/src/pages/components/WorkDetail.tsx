import React, { useEffect, useState } from 'react';
// 学習履歴や作業内容などを入力・表示するためのUIを構築するためのもの
const WorkDetail: React.FC = () => {
    // useStateフックを使用して、コンポーネント内で状態を管理するための
    //学習日の一覧を管理するための状態
    const [dates, setDates] = useState<string[]>([]);
    //各学習日に対する学習内容と学習時間を管理するための状態
    const [learningData, setLearningData] = useState<{ [date: string]: { contentA: string; contentB: string; hours: number } }>({});

    // ボタンの状態を管理するための新しい状態
    const [isRegistered, setIsRegistered] = useState(false);

    // メッセージ表示用の状態を追加
    const [message, setMessage] = useState<string>("");

    //選択できる学習コンテンツのオプションが含まれている
    const learningContentOptions = [
        'level0-1 イントロダクション・基礎学習について',
        'level1-1 環境構築',
        'level1-2 データ型・演算子・変数',
        'level2-1 関数',
        'level2-2 より良いコードを書くには？',
        'level2-3 比較',
        'level3-1 条件分岐①',
        'level3-2 条件分岐②・演算子・変数',
        'level3-3 スコープ',
        'level4-1 配列',
        'level4-2 オブジェクト',
        'level4-3 forループ',
        'level5-1 HTML・CSSの基礎知識',
        'level5-2 HTML・CSS演習（My IRページ）',
    ];

    //コンポーネントが初めてマウントされたときに実行される処理を定義している
    //今日から3か月後までの日付を生成し、datesステートに設定している
    useEffect(() => {
        const startDate = new Date();
        const endDate = new Date();
        endDate.setMonth(endDate.getMonth() + 3);

        const generatedDates: string[] = [];

        while (startDate <= endDate) {
            generatedDates.push(
                `${startDate.getFullYear()}/${startDate.getMonth() + 1}/${startDate.getDate()}`
            );
            startDate.setDate(startDate.getDate() + 1);
        }

        setDates(generatedDates);
    }, []);

    //学習データの変更があった際に呼び出され、その変更をlearningDataステートに反映する
    const handleLearningDataChange = (date: string, contentA: string, contentB: string, hours: number) => {
        setLearningData((prevData) => ({
            ...prevData,
            [date]: { contentA, contentB, hours },
        }));
    };
    
    // 学習内容登録ボタンのクリックイベントハンドラ
    const handleRegisterClick = () => {
        // 学習内容の登録処理をここに実装
        setIsRegistered(!isRegistered); // ボタンの状態をトグルする
    };

    return (
        <div className="square-container">
            <span className="text-inside">
                <h2 className='font-bold text-blue-500 mt-8 mb-5 text-2xl'>実際の作業内容</h2>
                <table border={1}>
                    <thead>
                        <tr className='text-black'>
                            <th>学習日</th>
                            <th>実際の学習内容</th>
                            <th>実際の学習内容</th>
                            <th>学習時間[h]</th>
                        </tr>
                    </thead>
                    <tbody className='text-black'>
                        {dates.map((date, index) => (
                            <tr key={index}>
                                <td>{date}</td>
                                <td>
                                    <select
                                        value={learningData[date]?.contentA || ''}
                                        onChange={(e) => {
                                            const contentA = e.target.value;
                                            handleLearningDataChange(date, contentA, learningData[date]?.contentB || '', learningData[date]?.hours || 0);
                                        }}
                                    >
                                        <option value="">選択してください</option>
                                        {learningContentOptions.map((option) => (
                                            <option key={option} value={option}>
                                                {option}
                                            </option>
                                        ))}
                                    </select>
                                </td>
                                <td>
                                    <select
                                        value={learningData[date]?.contentB || ''}
                                        onChange={(e) => {
                                            const contentB = e.target.value;
                                            handleLearningDataChange(date, learningData[date]?.contentA || '', contentB, learningData[date]?.hours || 0);
                                        }}
                                    >
                                        <option value="">選択してください</option>
                                        {learningContentOptions.map((option) => (
                                            <option key={option} value={option}>
                                                {option}
                                            </option>
                                        ))}
                                    </select>
                                </td>
                                <td>
                                    <input
                                        type="number"
                                        value={learningData[date]?.hours || 0}
                                        onChange={(e) => {
                                            const hours = parseFloat(e.target.value);
                                            handleLearningDataChange(date, learningData[date]?.contentA || '', learningData[date]?.contentB || '', hours);
                                        }}
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <button 
                    style={{ float: 'right' }} 
                    className="bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black">学習内容修正</button>

                <button 
                    style={{ float: 'right' }} 
                        className={`p-3 rounded-full font-bold transition duration-300 text-black mr-2 ${isRegistered ? 'bg-pink-400' : 'bg-purple-400'}`}
                        onClick={handleRegisterClick}
                >
                    {isRegistered ? '登録完了!' : '学習内容登録'}
                </button>
            </span>
        </div>
    );
};

export default WorkDetail;



// import React, { useEffect, useState } from 'react';
// // 学習履歴や作業内容などを入力・表示するためのUIを構築するためのもの
// const WorkDetail: React.FC = () => {
//     // useStateフックを使用して、コンポーネント内で状態を管理するための
//     //学習日の一覧を管理するための状態
//     const [dates, setDates] = useState<string[]>([]);
//     //各学習日に対する学習内容と学習時間を管理するための状態
//     const [learningData, setLearningData] = useState<{ [date: string]: { contentA: string; contentB: string; hours: number } }>({});

//     //選択できる学習コンテンツのオプションが含まれている
//     const learningContentOptions = [
//         'level0-1 イントロダクション・基礎学習について',
//         'level1-1 環境構築',
//         'level1-2 データ型・演算子・変数',
//         'level2-1 関数',
//         'level2-2 より良いコードを書くには？',
//         'level2-3 比較',
//         'level3-1 条件分岐①',
//         'level3-2 条件分岐②・演算子・変数',
//         'level3-3 スコープ',
//         'level4-1 配列',
//         'level4-2 オブジェクト',
//         'level4-3 forループ',
//         'level5-1 HTML・CSSの基礎知識',
//         'level5-2 HTML・CSS演習（My IRページ）',
//     ];

//     //コンポーネントが初めてマウントされたときに実行される処理を定義している
//     //今日から3か月後までの日付を生成し、datesステートに設定している
//     useEffect(() => {
//         const startDate = new Date();
//         const endDate = new Date();
//         endDate.setMonth(endDate.getMonth() + 3);

//         const generatedDates: string[] = [];

//         while (startDate <= endDate) {
//             generatedDates.push(
//                 `${startDate.getFullYear()}/${startDate.getMonth() + 1}/${startDate.getDate()}`
//             );
//             startDate.setDate(startDate.getDate() + 1);
//         }

//         setDates(generatedDates);
//     }, []);

//     //学習データの変更があった際に呼び出され、その変更をlearningDataステートに反映する
//     const handleLearningDataChange = (date: string, contentA: string, contentB: string, hours: number) => {
//         setLearningData((prevData) => ({
//             ...prevData,
//             [date]: { contentA, contentB, hours },
//         }));
//     };

//     return (
//         <div className="square-container">
//             <span className="text-inside">
//                 <h2 className='font-bold text-blue-500 mt-8 mb-5 text-2xl'>実際の作業内容</h2>
//                 <table border="1">
//                     <thead>
//                         <tr className='text-black'>
//                             <th>学習日</th>
//                             <th>実際の学習内容</th>
//                             <th>実際の学習内容</th>
//                             <th>学習時間[h]</th>
//                         </tr>
//                     </thead>
//                     <tbody className='text-black'>
//                         {dates.map((date, index) => (
//                             <tr key={index}>
//                                 <td>{date}</td>
//                                 <td>
//                                     <select
//                                         value={learningData[date]?.contentA || ''}
//                                         onChange={(e) => {
//                                             const contentA = e.target.value;
//                                             handleLearningDataChange(date, contentA, learningData[date]?.contentB || '', learningData[date]?.hours || 0);
//                                         }}
//                                     >
//                                         <option value="">選択してください</option>
//                                         {learningContentOptions.map((option) => (
//                                             <option key={option} value={option}>
//                                                 {option}
//                                             </option>
//                                         ))}
//                                     </select>
//                                 </td>
//                                 <td>
//                                     <select
//                                         value={learningData[date]?.contentB || ''}
//                                         onChange={(e) => {
//                                             const contentB = e.target.value;
//                                             handleLearningDataChange(date, learningData[date]?.contentA || '', contentB, learningData[date]?.hours || 0);
//                                         }}
//                                     >
//                                         <option value="">選択してください</option>
//                                         {learningContentOptions.map((option) => (
//                                             <option key={option} value={option}>
//                                                 {option}
//                                             </option>
//                                         ))}
//                                     </select>
//                                 </td>
//                                 <td>
//                                     <input
//                                         type="number"
//                                         value={learningData[date]?.hours || 0}
//                                         onChange={(e) => {
//                                             const hours = parseFloat(e.target.value);
//                                             handleLearningDataChange(date, learningData[date]?.contentA || '', learningData[date]?.contentB || '', hours);
//                                         }}
//                                     />
//                                 </td>
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//                 <button style={{ float: 'right' }} className="bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black">学習内容修正</button>
//                 <button style={{ float: 'right' }} className="bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black mr-2">学習内容登録</button>
//             </span>
//         </div>
//     );
// };

// export default WorkDetail;

