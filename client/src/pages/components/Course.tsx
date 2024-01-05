import React from 'react';
// import './page.css';

const Course: React.FC = () => {

    //handleButtonClick関数でfetchAPIを使用してサーバーサイドにデータを送信
    const handleButtonClick = async (selectedCourse: string) => {

        try {
            //ユーザーが選択したコースをサーバーに送信
            const response = await fetch('http://localhost:8000/api/course_select_1', {
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
        <div className="square-container" >
            <span className="text-inside">
                <h2>Q1. あなたのコースを選択してください</h2>
                <button className="button" onClick={() => handleButtonClick('短期3か月')}>短期3か月</button>
                <button className='button' onClick={() => handleButtonClick('長期6か月')}>長期6か月</button>
            </span>
        </div >
    );
};

export default Course;