import React from 'react';
import LoginWithGoogle from './components/LoginWithGoogle';
import SignUp from './components/SignUp';

function Start() {
    return (
        <div>
            <h1>Welcome to Skill Navigator!!</h1>
            <h2>ログイン</h2>
            <LoginWithGoogle />
            
            <h2>アカウントを作成</h2>
            <SignUp />
        </div>
    );
}

export default Start;