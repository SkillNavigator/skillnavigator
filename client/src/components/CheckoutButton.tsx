
// CheckoutButton.tsx
import React from 'react';
import { useStripe } from '@stripe/react-stripe-js';
import { collection, addDoc, onSnapshot, getFirestore, doc } from 'firebase/firestore';
import firebase from 'firebase/compat/app'; // この行を修正
// CheckoutButton コンポーネントの props に User 型を指定
interface CheckoutButtonProps {
  user: firebase.User | null;
}
const CheckoutButton: React.FC <CheckoutButtonProps> = ({ user }) => {
  const stripe = useStripe();
 

  const handleCheckout = async () => {
    try {
      const db = getFirestore();

      // Get the user's Firestore document reference
      const userDocRef = doc(db, 'users', user?.uid as string);

      // Create a checkout session
      const checkoutColRef = collection(userDocRef, 'checkout_sessions');
      const docRef = await addDoc(checkoutColRef, {
        automatic_tax: true,
        price: 'price_1OUNoDLW86m4ovpqWkr3K4IR', // Use the appropriate price ID
        success_url: window.location.origin,
        cancel_url: window.location.origin,
      });

      // Wait for the checkout session and handle the result
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
    <button onClick={handleCheckout}>
      Checkout Now
    </button>
  );
};

export default CheckoutButton;


