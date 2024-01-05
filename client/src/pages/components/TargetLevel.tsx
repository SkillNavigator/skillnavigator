import React from 'react';
// import './page.css';

const TargetLevel: React.FC = () => {
    //handleButtonClick関数でfetchAPIを使用してサーバーサイドにデータを送信
    const handleButtonClick = async (selectedCourse: string) => {
        try {
            //ユーザーが選択したコースをサーバーに送信
            const response = await fetch('http://localhost:8000/api/target_level_3', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ selectedCourse }),
            });
            //サーバーからのレスポンスをJSON形式で取得
            const data = await response.json();
            console.log('Data saved:', data);
        } catch (error) {
            //エラーが発生した場合はコンソールに出力
            console.error('Error:', error);
        }
    };

    return (
        <div className="square-container">
            <span className="text-inside">
                <h2>Q3. 目標レベルを設定してください</h2>
                <button className="button" onClick={() => handleButtonClick('Must課題までをマスター')}>Must課題までをマスター</button>
                <button className="button" onClick={() => handleButtonClick('Advanced課題までをマスター')}>Advance課題までをマスター</button>
            </span>
        </div>
    );
};

export default TargetLevel;