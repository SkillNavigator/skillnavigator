import React, { useState }from 'react';
import { auth, provider} from "./firebase";
import { FirebaseError} from 'firebase/app';
import { signInWithPopup, signOut} from 'firebase/auth';
import { collection,addDoc,onSnapshot,getFirestore, doc, setDoc } from 'firebase/firestore'; 


function SignUp() {
    return (
        <div>
            <SignUpButton />
        </div>
    );

}

function SignUpButton() {
    // ユーザーの状態を更新
        const [user, setUser] = useState<firebase.User | null>(null);
        const signInWithGoogle = async (event: React.MouseEvent<HTMLButtonElement>) => {
            try {
                event.preventDefault(); // デフォルトの挙動をキャンセルしてリンク先に遷移
                const result = await signInWithPopup(auth, provider);
                // 認証成功時にユーザー情報を取得
                const user = result.user;
                console.log('認証されたユーザー:', user);
    
                 // Firestoreに書き込むデータ
                const userData = {
                
                        uid: user.uid,
                        name: user.displayName,
                };
                 // Firestoreの参照を取得
                 const db = getFirestore();
                 // "users"というコレクションの中で、ユーザーのUIDをドキュメントIDとして指定
                 const userDocRef = doc(db, 'users', user.uid);

                  // ドキュメントが存在する場合は更新、存在しない場合は新規追加{ merge: true }
                  await setDoc(userDocRef, userData, { merge: true });

                 console.log('ユーザーデータをFirestoreに書き込みました:', userData);
             
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
        const logout = () => {
            signOut(auth)
              .then(() => {
                setUser(null);
                console.log('ログアウト成功.');
              })
              .catch((error) => {
                console.log(error);
              });
          };
                 const checkout = async () => {
                    try {
                      // 決済の機能のコードをそのまま統合
                      const db = getFirestore();
                     
                      const customerRef = doc(collection(db, 'customers'), user?.uid);
                      const checkoutColRef = collection(customerRef, 'checkout_sessions');
                      const docRef = await addDoc(checkoutColRef, {
                        automatic_tax: true,
                        price: 'price_1MqpEYKdOqi8OlZoZT8MEXVP',
                        success_url: window.location.origin,
                        cancel_url: window.location.origin,
                      });
                      onSnapshot(docRef, (snapshot) => {
                        const { error, url } = snapshot.data() as { error?: { message: string }, url?: string };
                        if (error) {
                          alert(`エラーが発生しました: ${error.message}`);
                        }
                        if (url) {
                          window.location.assign(url);
                        }
                      });
                     } catch (error) {
                    console.error('支払いエラー:', error);
                  }
                };
           
        return (
            <button onClick={signInWithGoogle}>
                <p>Googleで新規登録</p>
             <button onClick={checkout}>支払い</button>
             <button onClick={logout}>ログアウト</button>
            </button>
            );
        };
        export default SignUpButton;