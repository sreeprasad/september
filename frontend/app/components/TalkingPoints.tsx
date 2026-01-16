"use client";

import { MessageSquare, Quote, Copy, Check } from "lucide-react";
import { useState } from "react";

export default function TalkingPoints({ points }: { points: any[] }) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  if (!points || points.length === 0) return null;

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="glass-panel p-6 rounded-2xl h-full flex flex-col relative overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
        <MessageSquare className="w-24 h-24 text-indigo-500" />
      </div>

      <div className="flex items-center gap-3 mb-6 relative z-10">
        <div className="p-2.5 bg-indigo-50 rounded-xl text-indigo-600 border border-indigo-100 shadow-sm">
            <MessageSquare className="w-5 h-5" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-slate-900">Talking Points</h3>
          <p className="text-xs text-slate-500 font-medium">Strategic conversation starters</p>
        </div>
      </div>
      
      <div className="space-y-4 relative z-10">
        {points.map((item, index) => (
          <div 
            key={index} 
            className="group p-5 bg-white rounded-xl border border-slate-200 hover:border-indigo-300 hover:shadow-md hover:shadow-indigo-500/5 transition-all duration-300 relative"
          >
            <div className="flex gap-4">
                <div className="mt-1">
                  <Quote className="w-5 h-5 text-indigo-300 group-hover:text-indigo-500 transition-colors" />
                </div>
                <div className="flex-1">
                    <p className="font-semibold text-slate-900 leading-snug mb-2 text-[15px]">{item.point}</p>
                    <p className="text-sm text-slate-500 leading-relaxed bg-slate-50 p-2 rounded-lg border border-slate-100">
                      <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mr-1">Context:</span>
                      {item.context}
                    </p>
                </div>
            </div>
            
            <button 
              onClick={() => handleCopy(item.point, index)}
              className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 opacity-0 group-hover:opacity-100 transition-all"
              title="Copy to clipboard"
            >
              {copiedIndex === index ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
