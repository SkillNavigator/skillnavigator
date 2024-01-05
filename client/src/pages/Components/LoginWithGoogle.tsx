import React from 'react';
import { signInWithPopup } from 'firebase/auth';
import { auth, provider } from './firebase';
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
             <button onClick={signInWithGoogle}>
                <p>Googleでログイン</p>
            </button>
            );
        };