import React from 'react';
// import './page.css';

const TargetLevel: React.FC = () => {
    return (
        <div className="square-container">
            <span className="text-inside">
                <h2>Q3.　目標レベルを設定してください</h2>
                <button>Must課題までをマスター</button>
                <button>Advance課題までをマスター</button>
            </span>
        </div>
    );
};

export default TargetLevel;