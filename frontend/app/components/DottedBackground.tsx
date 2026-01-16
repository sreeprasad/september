import React from 'react';

export const DottedBackground = () => {
  return (
    <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden bg-[#030014]">
      {/* Refined Radial Gradient Background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(99,102,241,0.15),transparent_50%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(168,85,247,0.1),transparent_40%)]" />
      
      {/* Subtle Noise Texture overlay for texture */}
      <div className="absolute inset-0 opacity-[0.03] bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />
      
      {/* Floating Glow Orbs - More diffuse */}
      <div className="absolute top-[-10%] left-[20%] w-[600px] h-[600px] bg-indigo-600/10 rounded-full blur-[120px] animate-pulse duration-[8000ms]"></div>
      <div className="absolute bottom-[-10%] right-[10%] w-[700px] h-[700px] bg-purple-600/5 rounded-full blur-[140px]"></div>
    </div>
  );
};

export default DottedBackground;
