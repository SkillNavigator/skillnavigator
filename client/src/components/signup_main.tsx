// MainComponent.tsx
import React from 'react';
import SignUpButton from './SignUpButton';
// import any other necessary components

const MainComponent: React.FC = () => {
  return (
    <div className="flex flex-col h-screen justify-center items-center">
      {/* ... (any other content you want to include in the main component) */}
      <SignUpButton />
      {/* Include other components here if needed */}
    </div>
  );
};

export default MainComponent;
