import React from 'react';
import Course from './components/Course';
import LearningTarget from './components/LearningTarget';
import LearningLog from './components/LearningLog';
import TargetLevel from './components/TargetLevel';
import Determination from './components/Determination';
import SettingComp from './components/SettingComp';
import GetPlan from './components/getPlan';

const App: React.FC = () => {
    return (
        <div className="App">
            <h1>Setting for SkillNavigator</h1>
            <Course />
            <LearningLog />
            <TargetLevel />
            <LearningTarget />
            <Determination />
            <SettingComp />
            <GetPlan />
        </div>
    );
};

export default App;