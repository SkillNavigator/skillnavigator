import React, { useState } from 'react';
// import './page.css';

const Determination: React.FC = () => {
    // inputの値を格納するstate
    const [determinationText, setDeterminationText] = useState<string>('');

    // サーバーに文字列を送信する関数
    const sendDetermination = async () => {
        try {
            // ユーザーが入力した文字列をサーバーに送信
            const response = await fetch('http://localhost:8000/api/determination_5', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ determinationText }),
            });

            // サーバーからのレスポンスをJSON形式で取得
            const data = await response.json();
            console.log('Determination saved:', data);
        } catch (error) {
            // エラーが発生した場合はコンソールに出力
            console.error('Error:', error);
        }
    };

    return (
        <div className="square-container">
            <span className="text-inside">
                <h2>Q5.　意気込みを入力してください</h2>
                <input
                    type="text"
                    id="determinationInput"
                    name="determinationInput"
                    value={determinationText}
                    onChange={(e) => setDeterminationText(e.target.value)}
                />
                {/* 文字列をサーバーに送信するボタン */}
                <button onClick={sendDetermination}>意気込みを保存する</button>
            </span>
        </div>
    );
};


export default Determination;

