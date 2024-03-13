//Q1.あなたのコースを選択してください
import React, { useState } from 'react';
// import './page.css';

const Course: React.FC = () => {

    // ボタンの状態を管理するための新しい状態
    const [isRegistered1, setIsRegistered1] = useState(false);
    const [isRegistered2, setIsRegistered2] = useState(false);
   //handleButtonClick関数でfetchAPIを使用してサーバーサイドにデータを送信
   const handleButtonClick = async (selectedCourse: string) => {

    try {
        //ユーザーが選択したコースをサーバーに送信
        const response = await fetch('http://localhost:8000/api/course_select_1', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selectedCourse }),
        });
        //サーバーからのレスポンスをJSON形式で取得
        const data = await response.json();
        console.log('Data saved:', data);
    } catch (error) {
        //エラーが発生した場合はコンソールに出力
        console.error('Error:', error);
    }
};

return (
    <div className="flex justify-center items-center text-center">
        <span className="text-inside">
            <h2 className='font-bold text-3xl text-center text-black'>Q1. あなたのコースを選択してください</h2>
            <button
                className={`p-3 rounded-full font-bold transition duration-300 text-black mr-2 ${isRegistered1 ? 'bg-pink-400' : 'bg-purple-400'}`}
                onClick={() => {
                    handleButtonClick('短期3か月');
                    setIsRegistered1(!isRegistered1);
                }}
            >
                {isRegistered1 ? '短期3か月' : '短期3か月'}
            </button>
            <button
                className={`p-3 rounded-full font-bold transition duration-300 text-black mr-2 ${isRegistered2 ? 'bg-pink-400' : 'bg-purple-400'}`}
                onClick={() => {
                    handleButtonClick('長期6か月');
                    setIsRegistered2(!isRegistered2);
                }}
            >
                {isRegistered2 ? '長期6か月' : '長期6か月'}
            </button>
        </span>
    </div >
);
};

export default Course;


// // ボタン変更前　動くコード
// import React from 'react';
// // import './page.css';

// const Course: React.FC = () => {

//     //handleButtonClick関数でfetchAPIを使用してサーバーサイドにデータを送信
//     const handleButtonClick = async (selectedCourse: string) => {

//         try {
//             //ユーザーが選択したコースをサーバーに送信
//             const response = await fetch('http://localhost:8000/api/course_select_1', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ selectedCourse }),
//             });
//             //サーバーからのレスポンスをJSON形式で取得
//             const data = await response.json();
//             console.log('Data saved:', data);
//         } catch (error) {
//             //エラーが発生した場合はコンソールに出力
//             console.error('Error:', error);
//         }
//     };

//     return (
//         <div className="flex justify-center items-center text-center">
//             <span className="text-inside">
//                 <h2 className='font-bold text-3xl text-center text-black'>Q1.　あなたのコースを選択してください</h2>
//                 {/* <button className="button" onClick={() => handleButtonClick('短期3か月')}>短期3か月</button> */}
//                 <button className={"bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"}
//                     onClick={() => handleButtonClick('短期3か月')}>短期3か月</button>
//                 {/* <button className='button' onClick={() => handleButtonClick('長期6か月')}>長期6か月</button> */}
//                 <button className={"bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"}
//                     onClick={() => handleButtonClick('長期6か月')}>長期6か月</button>
//             </span>
//         </div >
//     );
// };

// export default Course;
