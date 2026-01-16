import React from 'react';
import ReactMarkdown from 'react-markdown';
import { BriefingResponse } from '../types';

interface BriefingCardProps {
  data: BriefingResponse;
  onClose: () => void;
}

export const BriefingCard: React.FC<BriefingCardProps> = ({ data, onClose }) => {
  return (
    <div className="w-full max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="relative rounded-2xl bg-brief-surface/60 backdrop-blur-xl border border-brief-border shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
        
        {/* Header Actions */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-slate-900/50">
          <div className="flex items-center gap-3">
             <div className="p-2 bg-indigo-500/10 rounded-lg">
                <span className="material-symbols-outlined text-brief-primary">auto_awesome</span>
             </div>
             <div>
                <h2 className="text-sm font-semibold text-white">Generated Intelligence</h2>
                <p className="text-xs text-slate-400">AI-Synthesized Briefing</p>
             </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors" title="Copy">
               <span className="material-symbols-outlined text-[20px]">content_copy</span>
            </button>
            <button className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors" title="Export">
               <span className="material-symbols-outlined text-[20px]">ios_share</span>
            </button>
            <div className="h-4 w-px bg-white/10 mx-1"></div>
            <button 
                onClick={onClose}
                className="p-2 text-slate-400 hover:text-white hover:bg-red-500/10 hover:text-red-400 rounded-lg transition-colors"
            >
                <span className="material-symbols-outlined text-[20px]">close</span>
            </button>
          </div>
        </div>

        {/* Content Area */}
        <div className="p-8 md:p-10 overflow-y-auto custom-scrollbar bg-gradient-to-b from-transparent to-slate-950/30">
          <div className="prose prose-invert prose-slate max-w-none">
            <ReactMarkdown
              components={{
                h1: ({node, ...props}) => (
                  <div className="mb-8 pb-4 border-b border-white/10">
                    <h1 className="text-3xl font-bold text-white tracking-tight" {...props} />
                  </div>
                ),
                h2: ({node, ...props}) => (
                    <div className="flex items-center gap-3 mt-10 mb-4">
                        <span className="h-px flex-1 bg-gradient-to-r from-brief-primary/50 to-transparent"></span>
                        <h2 className="text-xl font-semibold text-indigo-300 tracking-wide uppercase text-sm" {...props} />
                    </div>
                ),
                h3: ({node, ...props}) => <h3 className="text-lg font-semibold text-white mt-6 mb-2" {...props} />,
                ul: ({node, ...props}) => <ul className="space-y-3 text-slate-300 my-4" {...props} />,
                li: ({node, ...props}) => (
                  <li className="flex gap-3 items-start" {...props}>
                    <span className="mt-2 w-1.5 h-1.5 rounded-full bg-brief-primary shrink-0 opacity-70"></span>
                    <span className="flex-1">{props.children}</span>
                  </li>
                ),
                strong: ({node, ...props}) => <strong className="text-white font-medium" {...props} />,
                p: ({node, ...props}) => <p className="text-slate-300 leading-7 mb-4 font-light" {...props} />
              }}
            >
              {data.markdown}
            </ReactMarkdown>
          </div>

          {/* Sources Section */}
          {data.sources && data.sources.length > 0 && (
            <div className="mt-12 p-6 rounded-xl bg-black/20 border border-white/5">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-[16px]">travel_explore</span>
                Verified Sources
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {data.sources.map((source, idx) => (
                  <a 
                    key={idx}
                    href={source.uri}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 transition-all group"
                  >
                    <div className="w-8 h-8 rounded bg-slate-800 flex items-center justify-center shrink-0">
                         <span className="material-symbols-outlined text-slate-400 text-[18px]">public</span>
                    </div>
                    <div className="overflow-hidden">
                        <p className="text-sm text-slate-200 truncate font-medium group-hover:text-brief-primary transition-colors">{source.title}</p>
                        <p className="text-xs text-slate-500 truncate">{new URL(source.uri).hostname}</p>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};