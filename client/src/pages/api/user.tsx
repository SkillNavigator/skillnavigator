import { NextApiRequest, NextApiResponse } from 'next';  
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
      try {
        const user = req.body; // ユーザー情報を取得
        // FastAPIにリクエストを送信
        const response = await fetch('http://localhost:8000/create_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(user),
        });
  
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
  
        res.status(200).json({ message: 'User created successfully' });
      } catch (error:any) {
        res.status(500).json({ message: error.message });
      }
    } else {
      res.status(405).json({ message: 'Method Not Allowed' });
    }
  }
  