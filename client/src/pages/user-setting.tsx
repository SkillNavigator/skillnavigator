// ボタン装飾のため保存できない時に使用するコード　ページ遷移がいつでもできます。
// import React from 'react';
// import Link from 'next/link';
// import { useRouter } from 'next/router';  // useRouterをインポート
// import Course from './components/Course';
// import LearningTarget from './components/LearningTarget';
// import LearningLog from './components/LearningLog';
// import TargetLevel from './components/TargetLevel';
// import Determination from './components/Determination';
// import HamburgerMenu from './components/HamburgerMenu';

// const UserSetting: React.FC = () => {
//     const router = useRouter();  // useRouterフックの使用
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
//             // // サーバーとの通信が成功したら、/get-planページに遷移する
//             // if (response.ok) {
//             //     router.push('/get-plan');
//             // }
//         } catch (error) {
//             console.error('Error:', error);
//         }
//         router.push('/get-plan');
//     };

//     return (
//         <div className="flex flex-col items-center justify-center bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200">
//             <br></br>
//             <h1 className='font-bold text-5xl tracking-tight text-blue-500 bg-clip-text ttext-transparent text-center'>設定</h1>
//             <HamburgerMenu />
//             <br></br>
//             <Course />
//             <br></br>
//             <LearningLog />
//             <br></br>
//             <TargetLevel />
//             <br></br>
//             <LearningTarget />
//             <br></br>
//             <Determination />
//             <br></br>
//             <div className="square-container">
//                 <span className="text-inside">
//                     {/* リンク不要のため削除 */}
//                     <button className={"bg-pink-600 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"} onClick={handleSettingComplete}>設定を完了する</button>
//                 </span>
//             </div>
//         </div>
//     );
// };

// export default UserSetting;


// ページ遷移は保存ができたら実行される
import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';  // useRouterをインポート
import Course from './components/Course';
import LearningTarget from './components/LearningTarget';
import LearningLog from './components/LearningLog';
import TargetLevel from './components/TargetLevel';
import Determination from './components/Determination';
import HamburgerMenu from './components/HamburgerMenu';

const UserSetting: React.FC = () => {
    const router = useRouter();  // useRouterフックの使用
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
            // サーバーとの通信が成功したら、/get-planページに遷移する
            if (response.ok) {
                router.push('/get-plan');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200">
            <br></br>
            <h1 className='font-bold text-5xl tracking-tight text-blue-500 bg-clip-text ttext-transparent text-center'>設定</h1>
            <HamburgerMenu />
            <br></br>
            <Course />
            <br></br>
            <LearningLog />
            <br></br>
            <TargetLevel />
            <br></br>
            <LearningTarget />
            <br></br>
            <Determination />
            <br></br>
            <div className="square-container">
                <span className="text-inside">
                    {/* リンク不要のため削除 */}
                    <button className={"bg-pink-600 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black"} onClick={handleSettingComplete}>設定を完了する</button>
                </span>
            </div>
        </div>
    );
};

export default UserSetting;

