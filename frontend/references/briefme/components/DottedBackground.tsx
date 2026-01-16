import React from 'react';

export const DottedBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 z-0 bg-[#030014] overflow-hidden pointer-events-none">
      {/* Abstract Grid that fades out at the bottom */}
      <div 
        className="absolute inset-0 z-0 opacity-[0.15]"
        style={{
          backgroundImage: `linear-gradient(to right, #4f46e5 1px, transparent 1px),
                           linear-gradient(to bottom, #4f46e5 1px, transparent 1px)`,
          backgroundSize: '4rem 4rem',
          maskImage: 'linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 80%)'
        }}
      />

      {/* Ambient Moving Blobs for "Alive" feel */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-[1]">
          <div className="absolute top-[-10%] left-[20%] w-[500px] h-[500px] bg-purple-900/40 rounded-full mix-blend-screen filter blur-[100px] animate-blob"></div>
          <div className="absolute top-[-10%] right-[10%] w-[400px] h-[400px] bg-indigo-900/40 rounded-full mix-blend-screen filter blur-[100px] animate-blob" style={{ animationDelay: '2s' }}></div>
          <div className="absolute bottom-[-10%] left-[30%] w-[600px] h-[600px] bg-blue-900/20 rounded-full mix-blend-screen filter blur-[120px] animate-blob" style={{ animationDelay: '4s' }}></div>
      </div>
      
      {/* Noise Texture for Matte Finish */}
      <div className="absolute inset-0 opacity-[0.04] z-[2]" 
           style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }} 
      />
      
      {/* Vignette to focus center */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,#030014_100%)] z-[3] opacity-80" />
    </div>
  );
};