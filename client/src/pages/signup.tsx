import React, { useState, useEffect, useRef } from 'react';
import { auth, provider } from "./firebase";
import { FirebaseError } from 'firebase/app';
import firebase from 'firebase/compat/app';
import { signInWithPopup, signOut } from 'firebase/auth';
import { collection, addDoc, onSnapshot, getFirestore, doc, setDoc } from 'firebase/firestore';
import { useStripe } from '@stripe/react-stripe-js';


// const CheckoutButton = dynamic(() => import('./CheckoutButton'), { ssr: false });
const CheckoutButton = () => null;
// function SignUp() {
//   return (
//     <div>
//       <SignUpButton />
//     </div>
//   );
// }
// 新規登録ボタン
function SignUpButton() {
  const [user, setUser] = useState<firebase.User | null>(null);

  const signInWithGoogle = async (event: React.MouseEvent<HTMLButtonElement>) => {
    try {
      event.preventDefault();
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      const userData = {
        uid: user.uid,
        name: user.displayName,
      };

      const db = getFirestore();
      const userDocRef = doc(db, 'users', user.uid);

      await setDoc(userDocRef, userData, { merge: true });

      console.log('ユーザーデータをFirestoreに書き込みました:', userData);
    } catch (error) {
      if (error instanceof FirebaseError && error.code === 'auth/popup-closed-by-user') {
        console.log('ログインプロセスがユーザーによって中断されました。');
      } else {
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
      .catch((error) => {433
        console.log(error);
      });
  };

  const [isMounted, setIsMounted] = useState(true);
  const cleanupExecutedRef = useRef(false);
  // クライアントサイドのみでコードが実行されるのでハイドレーションエラーを軽減できる
  useEffect(() => {
    
    const checkout = async () => {
      try {
       
        const db = getFirestore();
        const customerRef = user?.uid ? doc(db, 'users', user.uid) : null;
        // customerRef が null の場合、処理をスキップ
        if (!customerRef) {
          console.error('ユーザードキュメントが存在しません。');
          return;
        }

        // サブコレクションの参照
          const checkoutColRef = collection(customerRef, 'checkout_sessions');
         
      
        // サブコレクションに新しいドキュメントを追加
        // 支払いページに関する記述
        const docRef = await addDoc(checkoutColRef, {
          automatic_tax: true,
          price: 'price_1OSRlDLW86m4ovpqP7zW0E4u',
          success_url: window.location.origin,
          cancel_url: window.location.origin,
        });
     
        // onSnapshotメソッド：Stripe Checkoutセッションのドキュメントの変更を監視し、変更があるとそれに応じて動作する
        onSnapshot(docRef, (snapshot) => {
          const { error, url } = snapshot.data() as { error?: { message: string }, url?: string };
          if (error) {
            alert(`エラーが発生しました: ${error.message}`);
          }
          if (url && !cleanupExecutedRef.current) {
             // クロスオリジンの問題を回避するため、直接 window.location.assign ではなくリンクに遷移させる
               window.location.href = url;
            // window.location.assign(url);
          }
        });
      } catch (error) {
        console.error('支払いエラー:', error);
      }
    };

    // クリーンアップ関数
    const cleanup = () => {
      // コンポーネントがアンマウントされたらisMountedをfalseに設定
      setIsMounted(false);
      cleanupExecutedRef.current = true;
    };

    checkout();
    return cleanup;
  }, [user?.uid]);

  return (
    <div>
      {/* COOPポリシーを変更。クロスオリジン　オープナーポリシーによってブロックされるのを防ぐ*/}
    <meta httpEquiv="Cross-Origin-Opener-Policy" content="unsafe-none"></meta>
      <button onClick={signInWithGoogle}>
        Googleで新規登録
        </button>
        <div>
      <CheckoutButton />
      </div>
      <button onClick={logout}>
        ログアウト
        </button>
    </div>
  );
}

export default SignUpButton;

