import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from 'firebase/firestore';
import firebase from 'firebase/compat/app'; 

const firebaseConfig = {
  apiKey:"AIzaSyBlXiF-FbZxVuxXu_9YeQIawAKERWO04vk",
  authDomain:"skill-navigator-8feca.firebaseapp.com",
  projectId:"skill-navigator-8feca",
// 　サーバーが起動できたら.env.localファイルの環境変数で動かすこと！
  // apiKey:process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  // authDomain:process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  // projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,

  storageBucket: "skill-navigator-8feca.appspot.com",
  messagingSenderId: "801448993987",
  appId: "1:801448993987:web:29b6a563bf7908f2ed6e76"
};

//NOTE:初期化設定
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
//NOTE:GoogleAuthProviderポップアップでログインページが出てくる
const firestore = getFirestore(app);

// NOTE: 'firebase/auth' モジュールから FirebaseError をエクスポート
export { auth, provider, firestore, firebase as default };

