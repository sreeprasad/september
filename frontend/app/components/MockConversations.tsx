"use client";

import { useState } from "react";
import { MessageCircle, HelpCircle, PlayCircle, Send, User, Bot, Sparkles } from "lucide-react";

export default function MockConversations({ conversations }: { conversations: any }) {
  const [activeTab, setActiveTab] = useState<"questions" | "pitch">("questions");

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
        <div className="flex bg-slate-100/80 p-1 rounded-xl backdrop-blur-sm border border-slate-200">
          <button
            onClick={() => setActiveTab("questions")}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${
              activeTab === "questions"
                ? "bg-white text-indigo-600 shadow-sm ring-1 ring-black/5"
                : "text-slate-500 hover:text-slate-700 hover:bg-slate-200/50"
            }`}
          >
            Questions
          </button>
          <button
            onClick={() => setActiveTab("pitch")}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-all ${
              activeTab === "pitch"
                ? "bg-white text-indigo-600 shadow-sm ring-1 ring-black/5"
                : "text-slate-500 hover:text-slate-700 hover:bg-slate-200/50"
            }`}
          >
            Simulation
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar relative z-10">
      {activeTab === "questions" && (
        <div className="space-y-4">
          {conversations.likely_questions?.map((q: any, index: number) => (
            <div key={index} className="bg-white rounded-xl p-5 border border-slate-200 hover:border-violet-200 hover:shadow-md hover:shadow-violet-500/5 transition-all duration-300 group">
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                    <div className="w-10 h-10 rounded-full bg-violet-50 flex items-center justify-center text-violet-600 border border-violet-100">
                        <span className="font-bold text-sm font-mono">Q{index + 1}</span>
                    </div>
                </div>
                <div className="space-y-3 flex-1">
                  <p className="font-semibold text-slate-900 leading-snug text-lg">{q.question}</p>
                  
                  {/* Handle response strategy structure */}
                  <div className="bg-slate-50/50 rounded-xl p-4 border border-slate-100">
                    {q.response_framework ? (
                        <div className="space-y-3">
                            <div className="flex items-start gap-2">
                              <Sparkles className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                              <p className="text-sm text-slate-600"><span className="font-semibold text-slate-900">Strategy:</span> {q.response_framework}</p>
                            </div>
                            
                            {q.emphasize && (
                                <div className="flex flex-wrap gap-2 pt-1">
                                    {(Array.isArray(q.emphasize) ? q.emphasize : [q.emphasize]).map((tag: string, i: number) => (
                                        <span key={i} className="text-[10px] uppercase tracking-wider font-bold bg-green-50 text-green-700 px-2.5 py-1 rounded-md border border-green-100">
                                            + {tag}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </div>
                    ) : (
                        <p className="text-sm text-slate-600">{q.response_strategy || "No strategy available."}</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
          {!conversations.likely_questions?.length && (
              <div className="flex flex-col items-center justify-center py-12 text-slate-400">
                  <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                    <HelpCircle className="w-8 h-8 opacity-20" />
                  </div>
                  <p>No likely questions generated yet.</p>
              </div>
          )}
        </div>
      )}

      {activeTab === "pitch" && (
        <div className="space-y-4 h-[550px] flex flex-col">
          <div className="bg-slate-50/50 rounded-2xl border border-slate-200/60 flex-1 p-6 overflow-y-auto space-y-6 custom-scrollbar">
             {!conversations.pitch_simulation?.length ? (
                 <div className="flex flex-col items-center justify-center h-full text-slate-400">
                     <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mb-4">
                        <PlayCircle className="w-8 h-8 opacity-20" />
                     </div>
                     <p>No pitch simulation generated.</p>
                 </div>
             ) : (
                 conversations.pitch_simulation.map((msg: any, index: number) => {
                     const isUser = msg.speaker === 'you' || msg.role === 'you';
                     return (
                        <div key={index} className={`flex gap-4 ${isUser ? 'flex-row-reverse' : 'flex-row'} group`}>
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm border border-white ${isUser ? 'bg-indigo-600 text-white' : 'bg-white text-slate-600'}`}>
                                {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                            </div>
                            <div className={`max-w-[80%] space-y-1.5`}>
                                <div className={`p-4 rounded-2xl text-[15px] leading-relaxed shadow-sm transition-all duration-300 ${
                                    isUser 
                                    ? 'bg-indigo-600 text-white rounded-tr-sm shadow-indigo-200' 
                                    : 'bg-white border border-slate-200 text-slate-700 rounded-tl-sm hover:shadow-md'
                                }`}>
                                    {msg.message || msg.content}
                                </div>
                                {msg.context && (
                                    <p className={`text-xs font-medium flex items-center gap-1.5 ${isUser ? 'justify-end text-slate-400' : 'text-slate-400'}`}>
                                        <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                                        {msg.context}
                                    </p>
                                )}
                            </div>
                        </div>
                     );
                 })
             )}
          </div>
          
          {/* Fake Input Area */}
          <div className="relative pt-2">
              <input 
                disabled 
                type="text" 
                placeholder="Type a message to practice..." 
                className="w-full pl-5 pr-14 py-4 bg-white border border-slate-200 rounded-2xl text-sm focus:outline-none focus:border-indigo-300 disabled:bg-white disabled:text-slate-400 shadow-sm"
              />
              <button disabled className="absolute right-3 top-1/2 mt-1 -translate-y-1/2 p-2 bg-indigo-600 text-white rounded-xl opacity-90 hover:opacity-100 transition-opacity shadow-lg shadow-indigo-500/30">
                  <Send className="w-4 h-4" />
              </button>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}
