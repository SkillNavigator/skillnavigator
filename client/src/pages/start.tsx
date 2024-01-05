import React from 'react';
import LoginWithGoogle from './Components/LoginWithGoogle';
import SignUp from './Components/SignUp';

function Start() {
    return (
        <div>
            <h1>Welcome to Skill Navigator!!</h1>
            <h2>ログイン</h2>
            <LoginWithGoogle />
            
            <h2>アカウントを作成</h2>
            <SignUp />
        </div>
    );
}

export default Start;


































// ---------
//以下tailwind css付きのコード。エラーのためコメントアウト中
// import React from 'react';
// import LoginWithGoogle from './Components/LoginWithGoogle';
// import SignUp from './Components/SignUp';

// function Start() {
//     return (
//         <div class="font-bold m-20 text-center text-black dark:text-white">
//             <h1 class="text-4xl">Welcome to Skill Navigator!!</h1>

//             <div class="flex justify-center gap-5 mt-44 text-2xl flex-wrap">
//                 <div class="mr-40">
//                     <h2>ログイン</h2>
//                         <button class="bg-white hover:bg-gray-200 text-black font-bold py-2 px-4 rounded-full">
//                             <LoginWithGoogle />
//                         </button>
//                 </div>

//                 <div>
//                     <h2>アカウントを作成</h2>
//                         <button class="bg-white hover:bg-gray-200 text-black font-bold py-2 px-4 rounded-full">
//                             <SignUp />
//                         </button>
//                 </div>
//             </div>
//         </div>
//     );

// }

// export default Start;