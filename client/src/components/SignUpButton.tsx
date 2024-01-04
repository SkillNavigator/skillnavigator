// SignUpButton.tsx
import React ,{ useState }from 'react';
import { Elements, useStripe } from '@stripe/react-stripe-js';

import { signInWithPopup, signOut } from 'firebase/auth';
import { collection, addDoc, onSnapshot, getFirestore, doc, setDoc } from 'firebase/firestore';
import { auth, provider } from '../pages/firebase';
import firebase from 'firebase/compat/app';
import styles from '@/styles/tailwind.module.css';
import { FirebaseError } from '@firebase/util';
import CheckoutButton from './CheckoutButton'; 



const SignUpButton: React.FC = () => {
  
  const [user, setUser] = useState<firebase.User | null>(null);
  const signInWithGoogle = async (event: React.MouseEvent<HTMLButtonElement>) => {
    try {
      event.preventDefault(); // デフォルトの挙動をキャンセルしてリンク先に遷移
      //Google認証ポップアップが表示
        const result = await signInWithPopup(auth, provider);
        // 認証成功時にユーザー情報を取得
        const user = result.user;
        console.log('認証されたユーザー:', user);
        // // ログイン成功後、ユーザー情報を設定
        // setUser(result.user);
        //posgreに登録
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
    } catch (error:unknown) {
        if (error instanceof FirebaseError &&error.code === 'auth/popup-closed-by-user') {
            // ユーザーによってポップアップが閉じられた場合の処理
        console.log('ログインプロセスがユーザーによって中断されました。');
            } else {
            // その他のエラーの処理
            console.error('ログインエラー:', error);
            }
}
};

const stripe = useStripe();
// 成功したサインインの後にアクションを処理するためのプレースホルダー
const handleSignInSuccess = async (user: firebase.User) => {


  // stripeを使う前に使える状態かどうかを調べる
  if (stripe) {
    const elements = stripe.elements();
    // Use stripe and elements as needed
  }
}

const checkout = async () => {
  try {
    const db = getFirestore();

    // ユーザーの Firestore ドキュメントを参照
    const userDocRef = doc(db, 'users', user?.uid as string);

   
    const checkoutColRef = collection(userDocRef, 'checkout_sessions');
 // チェックアウトセッションの作成　firestoreに記録
    const docRef = await addDoc(checkoutColRef, {
      automatic_tax: true,
      price: 'price_1OUNoDLW86m4ovpqWkr3K4IR',
      success_url: window.location.origin,
      cancel_url: window.location.origin,
    });

    // チェックアウトセッションの待機
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

  

  return (
    
    
      <div className="flex flex-col h-screen justify-center items-center">
        <div className="text-center">
          <button className={styles.button} onClick={signInWithGoogle}>
            Googleで新規登録
          </button>
           {/* CheckoutButtonにuser情報をpropsとして渡す */}
          <CheckoutButton user={user} />
          <button className={styles.button} onClick={logout}>
            ログアウト
          </button>
        </div>
      </div>

    
  );
};

export default SignUpButton;

