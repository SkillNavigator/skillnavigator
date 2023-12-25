'use client'

import React from 'react';
import Course from './Course/page';
import LearningTarget from './LearningTarget/page';
import LearningLog from './LearningLog/page';
import TargetLevel from './TargetLevel/page';
import Determination from './Determination/page';
import SettingComp from './SettingComp/page';

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
        </div>
    );
};

export default App;
