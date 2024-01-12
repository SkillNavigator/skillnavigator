import React from 'react';
// import './page.css';

const SettingComp: React.FC = () => {
    const handleSettingComplete = async () => {
        try {
            // サーバーに送信するデータを定義（例: 空のオブジェクト）
            const requestData = {};

            // サーバーとの通信（POSTリクエスト）
            const response = await fetch('http://localhost:8000/api/setting_complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            // サーバーからのレスポンスを取得
            const data = await response.json();

            // サーバーの応答をコンソールに出力
            console.log('Setting completed:', data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="flex justify-center items-center">
            <span className="text-inside">
                {/* ボタンがクリックされたときに handleSettingComplete 関数を呼び出す */}
                <button className={"bg-pink-600 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"} onClick={handleSettingComplete}>設定を完了する</button>
            </span>
        </div>
    );
};

export default SettingComp;


// import React from 'react';
// // import './page.css';

// const SettingComp: React.FC = () => {
//     const handleSettingComplete = async () => {
//         try {
//             // サーバーに送信するデータを定義（例: 空のオブジェクト）
//             const requestData = {};

//             // サーバーとの通信（POSTリクエスト）
//             const response = await fetch('http://localhost:8000/api/setting_complete', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify(requestData),
//             });

//             // サーバーからのレスポンスを取得
//             const data = await response.json();

//             // サーバーの応答をコンソールに出力
//             console.log('Setting completed:', data);
//         } catch (error) {
//             console.error('Error:', error);
//         }
//     };

//     return (
//         <div className="flex justify-center items-center">
//             <span className="text-inside">
//                 {/* ボタンがクリックされたときに handleSettingComplete 関数を呼び出す */}
//                 <button className={"bg-pink-600 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"} onClick={handleSettingComplete}>設定を完了する</button>
//             </span>
//         </div>
//     );
// };

// export default SettingComp;

