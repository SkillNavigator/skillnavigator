// // CheckoutButton.tsx
// import React, { useState, useEffect } from 'react';
// import { Elements } from '@stripe/react-stripe-js';
// import CheckoutForm from './CheckoutForm';
// import { useStripe } from '@stripe/react-stripe-js';

// const CheckoutButton: React.FC = () => {
//   const stripe = useStripe();
//   const [loading, setLoading] = useState(false);
//   useEffect(() => {
//     // stripeオブジェクトが利用可能かどうかを確認する
//     if (stripe) {
//       // ここで追加のセットアップやチェックを行うことができます
//     }
//   }, [stripe]);
//   const handleClick = async () => {
//     try {
//       setLoading(true);

//       // Stripeの支払い処理などを行う
//       const { error } = await stripe.redirectToCheckout({
//         items: [{ sku: 'your-sku-id', quantity: 1 }], // 商品のSKU IDなどを指定
//         successUrl: window.location.origin,
//         cancelUrl: window.location.origin,
//       });

//       if (error) {
//         console.error('支払いエラー:', error);
//         alert(`エラーが発生しました: ${error.message}`);
//       }
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div>
//       <Elements stripe={stripe}>
//         <CheckoutForm /> {/* Stripe Elementsを使用するフォームのコンポーネント */}
//       </Elements>

//       <button onClick={handleClick} disabled={loading}>
//         {loading ? '処理中...' : '支払い'}
//       </button>
//     </div>
//   );
// };

// export default CheckoutButton;

// // // CheckoutButton.tsx
// // import React, { useState, useEffect } from 'react';
// // import { useStripe } from '@stripe/react-stripe-js';
// // import CheckoutForm from './CheckoutForm'; // この部分にStripe Elementsを使用するフォームのコンポーネントをインポート

// // const CheckoutButton: React.FC = () => {
// //   const stripe = useStripe();
// //   const [loading, setLoading] = useState(false);

// //   const handleClick = async () => {
// //     try {
// //       setLoading(true);

// //       // Stripeの支払い処理などを行う
// //       const { error } = await stripe.redirectToCheckout({
// //         items: [{ sku: 'your-sku-id', quantity: 1 }], // 商品のSKU IDなどを指定
// //         successUrl: window.location.origin,
// //         cancelUrl: window.location.origin,
// //       });

// //       if (error) {
// //         console.error('支払いエラー:', error);
// //         alert(`エラーが発生しました: ${error.message}`);
// //       }
// //     } finally {
// //       setLoading(false);
// //     }
// //   };

// //   return (
// //     <Elements stripe={stripe}>
// //     <button onClick={handleClick} disabled={loading}>
// //       {loading ? '処理中...' : '支払い'}
// //     </button>
// //     </Elements>
// //   );
// // };

// // export default CheckoutButton;
