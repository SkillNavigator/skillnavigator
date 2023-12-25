import React, { useState } from 'react';

const LearningTarget: React.FC = () => {
    // 各曜日の学習時間を格納するstate
    const [studyTime, setStudyTime] = useState<number[]>([0, 0, 0, 0, 0, 0, 0]);

    // サーバーに学習時間データを送信する関数
    const sendStudyTime = async () => {
        try {
            // 学習時間データをサーバーに送信
            const response = await fetch('http://localhost:8000/api/study_time_4', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ studyTime }),
            });

            // サーバーからのレスポンスをJSON形式で取得
            const data = await response.json();
            console.log('Study time saved:', data);
        } catch (error) {
            // エラーが発生した場合はコンソールに出力
            console.error('Error:', error);
        }
    };

    return (
        <div className="square-container">
            <span className="text-inside">
                <h2>Q4.　1日の学習時間を入力してください</h2>
                <table className="table" border={1}>
                    <thead>
                        <tr>
                            <th scope="col">曜日</th>
                            <th scope="col">時間</th>
                        </tr>
                    </thead>
                    <tbody>
                        {['月', '火', '水', '木', '金', '土', '日'].map((day, index) => (
                            <tr key={index}>
                                <td>{day}</td>
                                <td>
                                    <input
                                        type="number"
                                        value={studyTime[index]}
                                        onChange={(e) => {
                                            const newStudyTime = [...studyTime];
                                            newStudyTime[index] = parseInt(e.target.value, 10) || 0;
                                            setStudyTime(newStudyTime);
                                        }}
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <button onClick={sendStudyTime}>学習時間を保存する</button>
            </span>
        </div>
    );
};

export default LearningTarget;
