import React, { useEffect } from 'react';
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



// Googleのサインインを処理し、ユーザー情報をサーバーに送信する
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
        } catch (error) {
            if (error instanceof FirebaseError && error.code === 'auth/popup-closed-by-user') {
                // ユーザーによってポップアップが閉じられた場合の処理
                console.log('ログインプロセスがユーザーによって中断されました。');
            } else {
                // その他のエラーの処理
                console.error('ログインエラー:', error);
            }
        }
        console.log("SignUpButtonコンポーネントのレンダリングが完了しました");
    };
    // 　　　useEffectは、コンポーネントがレンダリングを完了した後にサーバーからデータを取得する
 
    useEffect(() => {
        const fetchData = async () => {
            try {
                const user = auth.currentUser;
                if (user) {
                    // FASTAPIのエンドポイントにリクエストを送信する
                    const res = await fetch(`${process.env.NEXT_PUBLIC_API_ENDPOINT}/create_user`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            uid: user.uid,
                            user_name: user.displayName,
                        }),
                    });
                    if (res.ok) {
                        console.log('ユーザー情報をサーバーに送信しました。');
                        router.push('./user-setting');
                    } else {
                        // サーバーからの応答がエラーを引き起こした場合
                        
                            throw new Error(`${res.status} ${res.statusText}`);
                        
                    }
                }
            } catch (error) {
                console.error('Fetch Error:', error);
            }
        };
        fetchData();
        // useEffectのクリーンアップ関数を返す
        return () => {
            // クリーンアップの処理を記述
        };
    }, [router]); // routerを依存関係の配列に追加


    return (
        <button className="bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black" onClick={signInWithGoogle}>
            <p>Googleで新規登録</p>
        </button>
    );
}
export default SignUp;

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


