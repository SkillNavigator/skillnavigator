import React from 'react';
// import './page.css';

const LearningLog: React.FC = () => {

    //handleButtonClick関数でfetchAPIを使用してサーバーサイドにデータを送信
    const handleButtonClick = async (selectedCourse: string) => {
        try {
            //ユーザーが選択したコースをサーバーに送信
            const response = await fetch('http://localhost:8000/api/learning_history_2', {
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
                <h2>Q2. 過去のプログラミング学習歴を選択してください</h2>
                <button className="button" onClick={() => handleButtonClick('未経験')}>未経験</button>
                <button className="button" onClick={() => handleButtonClick('少し知っている')}>少し知っている</button>
                <button className="button" onClick={() => handleButtonClick('頻繫に使用している')}>頻繁に使用している</button>
                <br></br>
            </span>
        </div>
    );
};

export default LearningLog;