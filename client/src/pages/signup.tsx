import React from 'react';
import { auth, provider } from "./firebase";
import { FirebaseError } from 'firebase/app';
import { signInWithPopup } from 'firebase/auth';

function SignUp() {
    return (
        <div>
            <SignUpButton />
        </div>
    );

}

export default SignUp;


function SignUpButton() {
        const signInWithGoogle = async () => {
            try {
                const result = await signInWithPopup(auth, provider);
                // 認証成功時にユーザー情報を取得
                const user = result.user;
                console.log('認証されたユーザー:', user);
    
                await fetch('/api/user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        uid: user.uid,
                        name: user.displayName,
                    }),
                });

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
            <button onClick={signInWithGoogle}>
                <p>Googleで新規登録</p>
            </button>
            );
        };