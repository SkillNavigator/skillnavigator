import React from 'react';
// import './page.css';

const LearningTarget: React.FC = () => {
    return (
        <div className="square-container">
            <span className="text-inside">
                <h2>Q4.　1日の学習時間を入力してください</h2>
                <table className="table" border={1}>
                    <thead>
                        <tr>
                            <th scope="col">曜日</th>
                            <th scope="col">月</th>
                            <th scope="col">火</th>
                            <th scope="col">水</th>
                            <th scope="col">木</th>
                            <th scope="col">金</th>
                            <th scope="col">土</th>
                            <th scope="col">日</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>時間</td>
                            <td><input type="number"></input></td>
                            <td><input type="number"></input></td>
                            <td><input type="number"></input></td>
                            <td><input type="number"></input></td>
                            <td><input type="number"></input></td>
                            <td><input type="number"></input></td>
                            <td><input type="number"></input></td>
                        </tr>
                    </tbody>
                </table>
            </span>
        </div>
    );
};

export default LearningTarget;

