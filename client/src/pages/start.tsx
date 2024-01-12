import React from 'react';
import LoginWithGoogle from './components/LoginWithGoogle';
import SignUp from './components/SignUp';

function Start() {
    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200">
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
// import LoginWithGoogle from './components/LoginWithGoogle';
// import SignUp from './components/SignUp';

// function Start() {
//     return (
//         <div>
//             <h1>Welcome to Skill Navigator!!</h1>
//             <h2>ログイン</h2>
//             <LoginWithGoogle />
            
//             <h2>アカウントを作成</h2>
//             <SignUp />
//         </div>
//     );
// }

// export default Start;