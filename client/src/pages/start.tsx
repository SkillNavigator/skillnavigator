import React from 'react';

import LoginWithGoogle from './LoginWithGoogle';
import SignUp from './signup';

function Start() {
    return (
       
      <div>
        <h1>Skill Navigator</h1>
        <h2>ログイン</h2>
        <LoginWithGoogle />

        <h2>新規登録</h2>
        <SignUp />
      </div>
    
       
    );

}

export default Start;