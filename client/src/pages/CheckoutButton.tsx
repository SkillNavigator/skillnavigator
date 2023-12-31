// CheckoutButton.tsx
import React, { useState, useEffect } from 'react';
import { useStripe } from '@stripe/react-stripe-js';

const CheckoutButton: React.FC = () => {
  const stripe = useStripe();
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    try {
      setLoading(true);

      // Stripeの支払い処理などを行う
      const { error } = await stripe.redirectToCheckout({
        items: [{ sku: 'your-sku-id', quantity: 1 }], // 商品のSKU IDなどを指定
        successUrl: window.location.origin,
        cancelUrl: window.location.origin,
      });

      if (error) {
        console.error('支払いエラー:', error);
        alert(`エラーが発生しました: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleClick} disabled={loading}>
      {loading ? '処理中...' : '支払い'}
    </button>
  );
};

export default CheckoutButton;
