import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="fixed top-6 left-0 right-0 z-50 flex justify-center px-4 animate-fade-in">
      <div className="w-full max-w-3xl bg-[#0B0C15]/60 backdrop-blur-2xl border border-white/10 rounded-full shadow-2xl shadow-black/50 p-1.5 pl-4 pr-2 flex items-center justify-between transition-all hover:bg-[#0B0C15]/70 hover:border-white/15">
        
        {/* Logo Section */}
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20 text-white border border-white/10 overflow-hidden group">
            <div className="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <span className="material-symbols-outlined text-[20px] relative z-10">hub</span>
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-bold tracking-wider text-white leading-none font-sans">
              BRIEFME
            </span>
            <span className="text-[9px] font-medium text-indigo-400/80 tracking-widest uppercase mt-0.5">
              Intelligence
            </span>
          </div>
        </div>

        {/* Center Navigation - Pill Design */}
        <nav className="hidden md:flex items-center gap-1 bg-white/5 rounded-full p-1 border border-white/5 ml-4">
          <button className="px-4 py-1.5 text-[11px] font-semibold text-white bg-indigo-500/20 border border-indigo-500/20 rounded-full shadow-[0_0_10px_rgba(99,102,241,0.15)] transition-all hover:bg-indigo-500/30 hover:shadow-[0_0_15px_rgba(99,102,241,0.25)]">
            New Brief
          </button>
          <button className="px-4 py-1.5 text-[11px] font-medium text-slate-400 hover:text-white transition-colors rounded-full hover:bg-white/5">
            History
          </button>
          <button className="px-4 py-1.5 text-[11px] font-medium text-slate-400 hover:text-white transition-colors rounded-full hover:bg-white/5">
            Templates
          </button>
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-1">
           <button className="w-9 h-9 flex items-center justify-center rounded-full text-slate-400 hover:text-white hover:bg-white/5 transition-all relative">
              <span className="material-symbols-outlined text-[20px]">notifications</span>
              <span className="absolute top-2.5 right-2.5 w-1.5 h-1.5 bg-red-500 rounded-full border border-[#0B0C15]"></span>
           </button>
           
           <div className="h-4 w-px bg-white/10 mx-1 hidden sm:block"></div>
           
           <button className="flex items-center gap-2 pl-1 pr-1 rounded-full hover:bg-white/5 transition-all group">
             <div className="w-9 h-9 rounded-full bg-gradient-to-b from-slate-700 to-slate-800 border border-white/10 flex items-center justify-center text-[10px] font-bold text-white shadow-inner group-hover:border-indigo-500/50 transition-all">
               JD
             </div>
           </button>
        </div>

      </div>
    </header>
  );
};
