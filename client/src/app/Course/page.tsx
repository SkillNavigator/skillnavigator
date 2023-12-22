import React from 'react';
// import './page.css';

const Course: React.FC = () => {
    return (
        <div className="square-container">
            <span className="text-inside">
                <h2>Q1.　あなたのコースを選択してください</h2>
                <button className="button">短期3か月</button>
                <button className='button'>長期3か月</button>
            </span>
        </div>
    );
};

export default Course;

