// SignUp.tsx
import React from 'react';
import { loadStripe } from '@stripe/stripe-js';
import SignUpButton from '../components/SignUpButton';
import { Elements} from '@stripe/react-stripe-js';
// stripeの公開キーに変更'your-stripe-publishable-key'   ※関数の中に入れないといけないかも
const stripePromise = loadStripe('pk_test_51OPfgZLW86m4ovpqotrGZoZSodyT77T30LAxelD1DSyVBKnWP3hZolidYQOm3EkgtA2FKtEbUBGaeZJQ6g5P3WxD00ozYPoXl3');
const SignUp: React.FC = () => {
    return (
        <div>
            <Elements stripe={stripePromise}>
            <SignUpButton />
            </Elements>
        </div>
    );
};

export default SignUp;

