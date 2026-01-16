import React, { useState } from 'react';
import { MeetingContext } from '../types';

interface InputFormProps {
  onSubmit: (data: { profileUrl: string; twitterHandle: string; context: string }) => void;
  isLoading: boolean;
}

export const InputForm: React.FC<InputFormProps> = ({ onSubmit, isLoading }) => {
  const [profileUrl, setProfileUrl] = useState('');
  const [twitterHandle, setTwitterHandle] = useState('');
  const [context, setContext] = useState<string>(MeetingContext.PARTNERSHIP);
  const [focusedField, setFocusedField] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (profileUrl) {
      onSubmit({ profileUrl, twitterHandle, context });
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="relative group">
        {/* Decorative Gradient Border Glow */}
        <div className="absolute -inset-[1px] bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500 rounded-2xl opacity-30 blur-sm group-hover:opacity-50 transition duration-1000"></div>
        
        <div className="relative bg-[#0B0C15]/80 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Target Profile Input */}
            <div className="space-y-2">
              <label className="text-[10px] font-bold text-indigo-300/80 uppercase tracking-widest ml-1">
                LinkedIn URL / Website
              </label>
              <div 
                className={`
                  relative flex items-center transition-all duration-300 rounded-xl border bg-[#030014]/50
                  ${focusedField === 'profile' ? 'border-indigo-500 ring-1 ring-indigo-500/20' : 'border-white/5 hover:border-white/10'}
                `}
              >
                <div className="pl-4 text-slate-500">
                  <span className="material-symbols-outlined text-[20px]">link</span>
                </div>
                <input
                  type="text"
                  value={profileUrl}
                  onChange={(e) => setProfileUrl(e.target.value)}
                  onFocus={() => setFocusedField('profile')}
                  onBlur={() => setFocusedField(null)}
                  placeholder="https://linkedin.com/in/..."
                  className="w-full bg-transparent text-white placeholder-slate-600 px-4 py-4 rounded-xl focus:outline-none font-medium text-sm"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Twitter Input */}
              <div className="space-y-2">
                <label className="text-[10px] font-bold text-indigo-300/80 uppercase tracking-widest ml-1">
                  Twitter Handle
                </label>
                <div 
                  className={`
                    relative flex items-center transition-all duration-300 rounded-xl border bg-[#030014]/50
                    ${focusedField === 'twitter' ? 'border-indigo-500 ring-1 ring-indigo-500/20' : 'border-white/5 hover:border-white/10'}
                  `}
                >
                  <div className="pl-4 text-slate-500">
                    <span className="material-symbols-outlined text-[18px]">alternate_email</span>
                  </div>
                  <input
                    type="text"
                    value={twitterHandle}
                    onChange={(e) => setTwitterHandle(e.target.value)}
                    onFocus={() => setFocusedField('twitter')}
                    onBlur={() => setFocusedField(null)}
                    placeholder="@username"
                    className="w-full bg-transparent text-white placeholder-slate-600 px-4 py-3.5 rounded-xl focus:outline-none font-medium text-sm"
                  />
                </div>
              </div>

              {/* Meeting Context Dropdown */}
              <div className="space-y-2">
                <label className="text-[10px] font-bold text-indigo-300/80 uppercase tracking-widest ml-1">
                  Context
                </label>
                <div className="relative">
                  <select
                    value={context}
                    onChange={(e) => setContext(e.target.value)}
                    className="w-full bg-[#030014]/50 text-white border border-white/5 hover:border-white/10 px-4 py-3.5 rounded-xl focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/20 transition-all appearance-none cursor-pointer font-medium text-sm pr-10"
                  >
                    {Object.values(MeetingContext).map((val) => (
                      <option key={val} value={val} className="bg-[#0B0C15] text-white py-2">{val}</option>
                    ))}
                  </select>
                  <div className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none">
                    <span className="material-symbols-outlined text-[18px]">unfold_more</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading || !profileUrl}
              className={`
                w-full mt-2 flex items-center justify-center gap-3 py-4 rounded-xl text-white font-semibold text-sm tracking-wide transition-all duration-300 relative overflow-hidden shadow-lg
                ${isLoading 
                  ? 'bg-slate-800 cursor-wait opacity-70' 
                  : 'bg-indigo-600 hover:bg-indigo-500 hover:shadow-indigo-500/25 active:scale-[0.98]'
                }
              `}
            >
              {isLoading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  <span>INITIALIZING SCAN...</span>
                </>
              ) : (
                <>
                  <span>GENERATE BRIEFING</span>
                  <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                </>
              )}
            </button>

          </form>
        </div>
      </div>
    </div>
  );
};