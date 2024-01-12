import React from 'react';
import LoginWithGoogle from './components/LoginWithGoogle';
import SignUp from './components/SignUp';
import HamburgerMenu from './components/HamburgerMenu'; 

function Start() {
    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200">
            <HamburgerMenu />
         {/* <div className="custom-background"> */}
            <h1 className="font-bold text-8xl text-blue-500">Welcome to SkillNavigator!!</h1>
                <div className="font-bold flex justify-center gap-5 mt-24 text-2xl flex-wrap">
                    <LoginWithGoogle />
                    <SignUp />
                </div>
        </div>
    );
}

export default Start;



// import React from 'react';
// import Link from 'next/link';
// import { useRouter } from 'next/router';  // useRouterをインポート
// import Course from './components/Course';
// import LearningTarget from './components/LearningTarget';
// import LearningLog from './components/LearningLog';
// import TargetLevel from './components/TargetLevel';
// import Determination from './components/Determination';

// const App: React.FC = () => {
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
//             // サーバーとの通信が成功したら、/get-planページに遷移する
//             if (response.ok) {
//                 router.push('/get-plan');
//             }
//         } catch (error) {
//             console.error('Error:', error);
//         }
//     };

//     return (
//         <div className="App">
//             <h1>Setting for SkillNavigator</h1>
//             <Course />
//             <LearningLog />
//             <TargetLevel />
//             <LearningTarget />
//             <Determination />
//             <div className="square-container">
//                 <span className="text-inside">
//                     {/* リンク不要のため削除 */}
//                     <button onClick={handleSettingComplete}>設定を完了する</button>
//                 </span>
//             </div>
//         </div>
//     );
// };

// export default App;




