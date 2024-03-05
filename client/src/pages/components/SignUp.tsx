import React from 'react';
import { auth, provider } from "./../../firebase";
import { FirebaseError } from 'firebase/app';
import { signInWithPopup } from 'firebase/auth';
import { useRouter } from 'next/router'; 
function SignUp() {
    return (
        <div>
            <SignUpButton />
        </div>
    );

}

export default SignUp;


function SignUpButton() {
    const router = useRouter();
        const signInWithGoogle = async () => {
            try {
                const result = await signInWithPopup(auth, provider);
                // 認証成功時にユーザー情報を取得
                const user = result.user;
                console.log('認証されたユーザー:', user);
                console.log('データの中身:', JSON.stringify({
                    uid: user.uid,
                    user_name: user.displayName,
                }),);
                 // ページ遷移
                 router.push('./user-setting');
                await fetch('http://localhost:8000/create_user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        uid: user.uid,
                        user_name: user.displayName,
                    }),
                });
                  // サーバーへの送信成功後にページ遷移
                  router.push('./user-setting');
            } catch (error) {
                if (error instanceof FirebaseError && error.code === 'auth/popup-closed-by-user') {
                    // ユーザーによってポップアップが閉じられた場合の処理
                    console.log('ログインプロセスがユーザーによって中断されました。');
                } else {
                    // その他のエラーの処理
                    console.error('ログインエラー:', error);
            }
        }
    };
        return (
            <button className="bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black" onClick={signInWithGoogle}>
                <p>Googleで新規登録</p>
            </button>
            );
        };

// import React from 'react';
// import { auth, provider } from "./firebase";
// import { FirebaseError } from 'firebase/app';
// import { signInWithPopup } from 'firebase/auth';
// import { useRouter } from 'next/router';

// function SignUp() {
//     return (
//         <div>
//             <SignUpButton />
//         </div>
//     );

// }

// export default SignUp;


// function SignUpButton() {

//     const router = useRouter();
//     const signInWithGoogle = async () => {
//         try {
//             const result = await signInWithPopup(auth, provider);
//             // 認証成功時にユーザー情報を取得
//             const user = result.user;
//             console.log('認証されたユーザー:', user);
//             console.log('データの中身:', JSON.stringify({
//                 uid: user.uid,
//                 user_name: user.displayName,
//             }),);

//             //本番環境とローカル環境でURLが異なる
//             await fetch('http://localhost:8000/create_user', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({
//                     uid: user.uid,
//                     user_name: user.displayName,
//                 }),
//             });

//             router.push('./user-setting');

//         } catch (error) {
//             if (error instanceof FirebaseError && error.code === 'auth/popup-closed-by-user') {
//                 // ユーザーによってポップアップが閉じられた場合の処理
//                 console.log('ログインプロセスがユーザーによって中断されました。');
//             } else {
//                 // その他のエラーの処理
//                 console.error('ログインエラー:', error);
//             }
//         }
//     };
//     return (
//         <button className="bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black" onClick={signInWithGoogle}>
//             <p>Googleで新規登録</p>
//         </button>
//     );
// };


