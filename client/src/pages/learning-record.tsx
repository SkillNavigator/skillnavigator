import React from 'react';
import ReferenceSchedule from './components/ReferenceSchedule';
import WorkDetail from './components/WorkDetail';
import HamburgerMenu from './components/HamburgerMenu';


const LearningRecord: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center bg-gradient-to-r from-indigo-200 via-purple-200 to-pink-200">
      <h1 className="font-bold text-4xl text-blue-500 mt-8">学習記録</h1>
        <HamburgerMenu />
        <ReferenceSchedule />
        <WorkDetail />
    </div>
  );
};

export default LearningRecord;

// import React from 'react';
// import ReferenceSchedule from './components/ReferenceSchedule';
// import WorkDetail from './components/WorkDetail';
// import HamburgerMenu from './components/HamburgerMenu';


// const LearningRecord: React.FC = () => {
//   return (
//     <div className="flex flex-col items-center justify-center bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300">
//       <h1>Learning Record for SkillNavigator</h1>
//       <HamburgerMenu />
//       <ReferenceSchedule />
//       <WorkDetail />
//     </div>
//   );
// };

// export default LearningRecord;