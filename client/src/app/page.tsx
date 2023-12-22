'use client'

import React from 'react';
import Course from './Course/page';
import LearningTarget from './LearningTarget/page';
import LearningLog from './LearningLog/page';
import TargetLevel from './TargetLevel/page';
import Determination from './Determination/page';

const App: React.FC = () => {
    return (
        <div className="App">
            <h1>Setting for SkillNavigator</h1>
            <Course />
            <LearningLog />
            <TargetLevel />
            <LearningTarget />
            <Determination />
            <button>設定を完了する</button>
        </div>
    );
};

export default App;
