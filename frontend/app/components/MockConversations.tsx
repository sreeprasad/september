"use client";

// HelpCircle, PlayCircle, Send, User, Bot, Sparkles removed as they are currently unused or their sections are removed
import { MessageCircle, User, Bot } from "lucide-react";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function MockConversations({ conversations }: { conversations: any }) {
  if (!conversations) return null;

  return (
    <div className="glass-panel p-6 rounded-2xl h-full flex flex-col relative overflow-hidden">
      <div className="flex items-center justify-between mb-6 relative z-10">
        <div className="flex items-center gap-3">
            <div className="p-2.5 bg-violet-50 rounded-xl text-violet-600 border border-violet-100 shadow-sm">
                <MessageCircle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900">Conversation Prep</h3>
              <p className="text-xs text-slate-500 font-medium">Roleplay & Strategy</p>
            </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar relative z-10">
        <div className="space-y-4">
          {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
          {conversations.map((conv: any, idx: number) => (
            <div key={idx} className="bg-white rounded-xl p-5 border border-slate-200 hover:border-violet-200 hover:shadow-md hover:shadow-violet-500/5 transition-all duration-300 group">
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-violet-50 flex items-center justify-center text-violet-600 border border-violet-100">
                        <span className="font-bold text-sm font-mono">{idx + 1}</span>
                    </div>
                </div>
                <div className="space-y-3 flex-1">
                  <h4 className="font-semibold text-slate-900 leading-snug text-lg uppercase tracking-wide text-xs text-violet-600">{conv.scenario}</h4>
                  
                  <div className="space-y-3 bg-slate-50/50 rounded-xl p-4 border border-slate-100">
                     {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
                     {conv.script?.map((line: any, i: number) => {
                         const isUser = line.speaker === "Me" || line.speaker === "You";
                         return (
                            <div key={i} className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
                                <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-indigo-600 text-white' : 'bg-white border border-slate-200 text-slate-500'}`}>
                                    {isUser ? <User size={12} /> : <Bot size={12} />}
                                </div>
                                <div className={`text-sm py-2 px-3 rounded-lg ${isUser ? 'bg-indigo-50 text-indigo-900' : 'bg-white border border-slate-100 text-slate-600'}`}>
                                    {line.text}
                                </div>
                            </div>
                         );
                     })}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
