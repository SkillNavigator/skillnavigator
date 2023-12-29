import React from 'react';
import Schedules from './components/Schedules';

const App: React.FC = () => {
    return (
        <div className="planning">
            <h1 className="planning-title">SkillNavigator</h1>
            <Schedules />
        </div>
    );
};

export default App;