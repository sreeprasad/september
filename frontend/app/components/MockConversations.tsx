"use client";

import { useState } from "react";
import { MessageCircle, HelpCircle, PlayCircle } from "lucide-react";

export default function MockConversations({ conversations }: { conversations: any }) {
  const [activeTab, setActiveTab] = useState<"questions" | "pitch">("questions");

  if (!conversations) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 h-full">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-slate-900">Conversation Prep</h3>
        <div className="flex bg-slate-100 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab("questions")}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all ${
              activeTab === "questions"
                ? "bg-white text-indigo-600 shadow-sm"
                : "text-slate-500 hover:text-slate-700"
            }`}
          >
            Questions
          </button>
          <button
            onClick={() => setActiveTab("pitch")}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-all ${
              activeTab === "pitch"
                ? "bg-white text-indigo-600 shadow-sm"
                : "text-slate-500 hover:text-slate-700"
            }`}
          >
            Simulation
          </button>
        </div>
      </div>

      {activeTab === "questions" && (
        <div className="space-y-4">
          {conversations.likely_questions?.map((q: any, index: number) => (
            <div key={index} className="bg-slate-50 rounded-lg p-4">
              <div className="flex gap-3">
                <HelpCircle className="w-5 h-5 text-indigo-500 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-slate-900 mb-2">{q.question}</p>
                  
                  {/* Handle response strategy structure */}
                  {q.response_framework ? (
                      <div className="text-sm space-y-2">
                          <p className="text-slate-600"><span className="font-semibold text-indigo-600">Strategy:</span> {q.response_framework}</p>
                          {q.emphasize && <p className="text-slate-500 text-xs">Emphasize: {Array.isArray(q.emphasize) ? q.emphasize.join(", ") : q.emphasize}</p>}
                      </div>
                  ) : (
                      <p className="text-sm text-slate-600">{q.response_strategy || "No strategy available."}</p>
                  )}
                </div>
              </div>
            </div>
          ))}
          {!conversations.likely_questions?.length && (
              <p className="text-slate-500 text-sm text-center py-4">No likely questions generated.</p>
          )}
        </div>
      )}

      {activeTab === "pitch" && (
        <div className="space-y-4">
          <div className="bg-slate-50 rounded-lg p-4 h-[400px] overflow-y-auto space-y-4">
             {conversations.pitch_simulation?.map((msg: any, index: number) => {
                 // Determine speaker role mapping
                 const isUser = msg.speaker === 'you' || msg.role === 'you';
                 
                 return (
                    <div key={index} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] rounded-2xl px-4 py-2.5 ${
                        isUser 
                        ? 'bg-indigo-600 text-white rounded-br-none' 
                        : 'bg-white border border-slate-200 text-slate-800 rounded-bl-none shadow-sm'
                    }`}>
                        <p className="text-xs opacity-70 mb-1">{isUser ? 'You' : 'Them'}</p>
                        <p className="text-sm">{msg.message || msg.content}</p>
                        {msg.context && (
                             <p className={`text-xs mt-1.5 italic ${isUser ? 'text-indigo-200' : 'text-slate-400'}`}>
                                 ({msg.context})
                             </p>
                        )}
                    </div>
                    </div>
                 );
             })}
             {!conversations.pitch_simulation?.length && (
                 <div className="flex flex-col items-center justify-center h-full text-slate-400">
                     <PlayCircle className="w-12 h-12 mb-2 opacity-20" />
                     <p>No pitch simulation generated.</p>
                 </div>
             )}
          </div>
        </div>
      )}
    </div>
  );
}
