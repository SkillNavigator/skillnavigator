import React from 'react';
// import './page.css';

const LearningLog: React.FC = () => {
    return (
        <div className="square-container">
            <span className="text-inside">
                <h2>Q2.　過去のプログラミング学習歴を選択してください</h2>
                <button>未経験</button>
                <button>少し知っている</button>
                <button>頻繁に使用している</button>
                <br></br>
            </span>
        </div>
    );
};

export default LearningLog;

