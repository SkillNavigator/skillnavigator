// pages/ProductTest.tsx
// Reactのコンポーネントで、FirebaseのFirestoreを使用して商品データを取得する
// マウント時に商品データをFirestoreから取得し、それをコンソールに表示するためのテスト用のコンポーネント。テストボタンをクリックすることでも商品データを再取得できます。
import { FC } from 'react';
import { useEffect } from 'react';
import { getFirestore, collection, query, where, getDocs } from 'firebase/firestore';

const ProductTest: FC = () => {
  const test = async () => {
    // Firestoreから商品データを取得:
    const colRef = collection(getFirestore(), 'products');
    const q = query(colRef, where('active', '==', true));

    try {
      // 商品データの取得と表示:
      const querySnapshot = await getDocs(q);

      querySnapshot.forEach(async (doc) => {
        console.log(doc.id, '=>', doc.data());
        const priceColRef = collection(doc.ref, 'prices');
        const priceSnap = await getDocs(priceColRef);

        priceSnap.docs.forEach((priceDoc) => {
          console.log(priceDoc.id, '=>', priceDoc.data());
        });
      });
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };
  // useEffect フック:
  useEffect(() => {
    // Call the test function when the component mounts
    test();
  }, []);

  return (
    <div>
      <h1>Product Test</h1>
      <button onClick={test}>Test</button>
    </div>
  );
};

export default ProductTest;