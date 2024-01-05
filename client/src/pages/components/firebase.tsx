import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBlXiF-FbZxVuxXu_9YeQIawAKERWO04vk",
  authDomain: "skill-navigator-8feca.firebaseapp.com",
  projectId: "skill-navigator-8feca",
  storageBucket: "skill-navigator-8feca.appspot.com",
  messagingSenderId: "801448993987",
  appId: "1:801448993987:web:29b6a563bf7908f2ed6e76"
};

//NOTE:初期化設定
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();
//NOTE:GoogleAuthProviderポップアップでログインページが出てくる

export { auth, provider };