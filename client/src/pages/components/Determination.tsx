//Q5. 意気込みを入力してください
import React, { useState } from 'react';
// import './page.css';

const Determination: React.FC = () => {
    // inputの値を格納するstate
    const [determinationText, setDeterminationText] = useState<string>('');
    // ボタンの状態を管理するための新しい状態
    const [isRegistered, setIsRegistered] = useState(false);


    // サーバーに文字列を送信する関数
    const sendDetermination = async () => {

        try {
            // ユーザーが入力した文字列をサーバーに送信
            const response = await fetch('http://localhost:8000/api/determination_5', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ determinationText }),
            });

            // サーバーからのレスポンスをJSON形式で取得
            const data = await response.json();
            console.log('Determination saved:', data);
        } catch (error) {
            // エラーが発生した場合はコンソールに出力
            console.error('Error:', error);
        }
    };

    return (
        <div className="flex justify-center items-center text-center">
            <span className="text-inside">
                <h2 className='font-bold text-3xl text-black'>Q5. 意気込みを入力してください</h2>
                <input
                    className="p-2 border border-gray-600 rounded-md focus:outline-none focus:ring focus:border-blue-1000 w-1/2 text-black"
                    type="text"
                    id="determinationInput"
                    name="determinationInput"
                    value={determinationText}
                    onChange={(e) => setDeterminationText(e.target.value)}
                />
                <button
                    className={`p-3 rounded-full font-bold transition duration-300 text-black mr-2 ${isRegistered ? 'bg-pink-400' : 'bg-purple-400'}`}
                    onClick={async () => {
                        await sendDetermination();
                        setIsRegistered(!isRegistered);
                    }}
                >
                    {isRegistered ? '内容登録完了' : '学習内容登録'}
                </button>
            </span>
        </div>
    );
};


export default Determination;
// ボタン変更前　動くコード
// import React, { useState } from 'react';
// // import './page.css';

// const Determination: React.FC = () => {
//     // inputの値を格納するstate
//     const [determinationText, setDeterminationText] = useState<string>('');

//     // サーバーに文字列を送信する関数
//     const sendDetermination = async () => {
//         try {
//             // ユーザーが入力した文字列をサーバーに送信
//             const response = await fetch('http://localhost:8000/api/determination_5', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ determinationText }),
//             });

//             // サーバーからのレスポンスをJSON形式で取得
//             const data = await response.json();
//             console.log('Determination saved:', data);
//         } catch (error) {
//             // エラーが発生した場合はコンソールに出力
//             console.error('Error:', error);
//         }
//     };

//     return (
//         <div className="flex justify-center items-center text-center">
//             <span className="text-inside">
//                 <h2 className='font-bold text-3xl text-black'>Q5.　意気込みを入力してください</h2>
//                 <input
//                     className="p-2 border border-gray-600 rounded-md focus:outline-none focus:ring focus:border-blue-1000 w-1/2"
//                     type="text"
//                     id="determinationInput"
//                     name="determinationInput"
//                     value={determinationText}
//                     onChange={(e) => setDeterminationText(e.target.value)}
//                 />
//                 {/* 文字列をサーバーに送信するボタン */}
//                 <button className={"bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"} onClick={sendDetermination}>意気込みを保存する</button>
//             </span>
//         </div>
//     );
// };


// export default Determination;

