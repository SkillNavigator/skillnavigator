import React from 'react';
import { signInWithPopup } from 'firebase/auth';
import { auth, provider } from './../../firebase';
// import { useAuthState } from "react-firebase-hook";


function LoginWithGoogle() {
    return <div>
        <LogInButton />
    </div>


}

export default LoginWithGoogle;


function LogInButton() {
        const signInWithGoogle = () => {
            signInWithPopup(auth, provider)
    
    };
        return (
            <button className="bg-purple-400 hover:bg-pink-400 p-3 rounded-full font-bold transition duration-300 text-black" onClick={signInWithGoogle}>
            <p>Googleでログイン</p>
        </button>
        );
    };
