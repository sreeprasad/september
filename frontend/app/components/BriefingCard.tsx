import React from 'react';
import Image from 'next/image';
import { Sparkles, Copy, Share, X, Globe, MapPin } from 'lucide-react';

interface BriefingData {
  themes?: any; // Complex union type simplified for now
  company_context?: any;
  mock_conversations?: any;
  person?: {
    name?: string;
    photo_url?: string;
    headline?: string;
    location?: string;
    company?: string;
    about?: string;
    summary?: string;
  };
  talking_points?: any[];
  sources?: { uri: string; title: string }[];
}

interface BriefingCardProps {
  data: BriefingData;
  onClose: () => void;
}

const BriefingCard: React.FC<BriefingCardProps> = ({ data, onClose }) => {
  // Helper to extract themes array from potentially complex object
  const themesList = React.useMemo(() => {
    if (!data.themes) return [];
    if (Array.isArray(data.themes)) return data.themes;
    // Handle object structure { primary: "...", secondary: [...] }
    return [
      data.themes.primary,
      ...(Array.isArray(data.themes.secondary) ? data.themes.secondary : [])
    ].filter(Boolean);
  }, [data.themes]);

  // Helper to extract company info
  const companyInfo = React.useMemo(() => {
      if (typeof data.company_context === 'string') return { name: '', description: data.company_context, facts: [] };
      return {
          name: data.company_context?.name || '',
          description: data.company_context?.description || '',
          facts: (data.company_context?.key_facts || []) as string[]
      };
  }, [data.company_context]);

  // Helper for conversations
  const conversationScenarios = React.useMemo(() => {
      if (Array.isArray(data.mock_conversations)) return data.mock_conversations;
      // If it's the structured object with likely_questions, etc.
      if (data.mock_conversations?.conversation_scenarios) {
          // Convert the scenarios object values to array
          return Object.values(data.mock_conversations.conversation_scenarios).map((s: any) => ({
              scenario: s.context?.replace('_', ' ') || "Scenario",
              script: s.sample_dialogue?.map((d: any) => ({ speaker: d.speaker, text: d.message })) || []
          }));
      }
      return [];
  }, [data.mock_conversations]);

  return (
    <div className="w-full max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="relative rounded-2xl bg-[#0B0C15]/60 backdrop-blur-xl border border-white/10 shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
        
        {/* Header Actions */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-slate-900/50">
          <div className="flex items-center gap-3">
             <div className="p-2 bg-indigo-500/10 rounded-lg">
                <Sparkles className="text-indigo-400 w-5 h-5" />
             </div>
             <div>
                <h2 className="text-sm font-semibold text-white">Generated Intelligence</h2>
                <p className="text-xs text-slate-400">AI-Synthesized Briefing</p>
             </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors" title="Copy">
               <Copy size={20} />
            </button>
            <button className="p-2 text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors" title="Export">
               <Share size={20} />
            </button>
            <div className="h-4 w-px bg-white/10 mx-1"></div>
            <button 
                onClick={onClose}
                className="p-2 text-slate-400 hover:text-white hover:bg-red-500/10 hover:text-red-400 rounded-lg transition-colors"
            >
                <X size={20} />
            </button>
          </div>
        </div>

        {/* Content Area */}
        <div className="p-8 md:p-10 overflow-y-auto custom-scrollbar bg-gradient-to-b from-transparent to-slate-950/30">
          
          {/* Profile Header */}
          <div className="flex items-start gap-6 mb-10 pb-10 border-b border-white/5">
            <div className="w-24 h-24 rounded-2xl bg-slate-800 border border-white/10 overflow-hidden shrink-0 relative">
               {data.person?.photo_url ? (
                  <Image 
                    src={data.person.photo_url} 
                    alt={data.person.name || "Profile"} 
                    fill
                    className="object-cover"
                    unoptimized
                  />
               ) : (
                  <div className="w-full h-full flex items-center justify-center text-3xl font-bold text-slate-600">
                    {data.person?.name?.charAt(0) || "?"}
                  </div>
               )}
            </div>
            <div>
               <h1 className="text-3xl font-bold text-white mb-2">{data.person?.name || "Unknown Profile"}</h1>
               <p className="text-lg text-indigo-400 mb-4">{data.person?.headline || "No headline available"}</p>
               <div className="flex flex-wrap gap-4 text-sm text-slate-400">
                  <div className="flex items-center gap-1.5">
                     <MapPin size={14} />
                     {data.person?.location || "Location unknown"}
                  </div>
                  {data.person?.company && (
                     <div className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-white/5 border border-white/5">
                        <Globe size={14} />
                        {data.person.company}
                     </div>
                  )}
               </div>
               <p className="mt-4 text-slate-300 leading-relaxed max-w-2xl text-sm">
                  {data.person?.about || data.person?.summary || "No summary available."}
               </p>
            </div>
          </div>

          {/* Structured Data View */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
             
             {/* Left Column: Talking Points & Icebreakers */}
             <div className="space-y-10">
                <section>
                   <div className="flex items-center gap-3 mb-6">
                      <span className="h-px flex-1 bg-gradient-to-r from-indigo-500/50 to-transparent"></span>
                      <h3 className="text-sm font-bold text-indigo-400 tracking-widest uppercase">Key Talking Points</h3>
                   </div>
                   <ul className="space-y-4">
                      {data.talking_points?.map((point: any, idx: number) => (
                         <li key={idx} className="flex gap-4 group">
                            <span className="text-indigo-500/50 font-mono text-sm mt-1">0{idx + 1}</span>
                            <div>
                               <p className="text-slate-200 font-medium group-hover:text-white transition-colors">
                                 {point.point || point.topic || point}
                               </p>
                               {point.why_selected && (
                                  <p className="text-sm text-slate-500 mt-1">{point.why_selected}</p>
                               )}
                               {point.reasoning && (
                                  <p className="text-sm text-slate-500 mt-1">{point.reasoning}</p>
                               )}
                            </div>
                         </li>
                      ))}
                   </ul>
                </section>

                <section>
                   <div className="flex items-center gap-3 mb-6">
                      <span className="h-px flex-1 bg-gradient-to-r from-purple-500/50 to-transparent"></span>
                      <h3 className="text-sm font-bold text-purple-400 tracking-widest uppercase">Psychological Profile</h3>
                   </div>
                   <div className="bg-white/5 rounded-xl p-6 border border-white/5">
                      <div className="flex flex-wrap gap-2 mb-4">
                         {themesList.map((theme: any, idx: number) => (
                            <span key={idx} className="px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-medium">
                               {theme.theme || theme}
                            </span>
                         ))}
                      </div>
                      <p className="text-sm text-slate-400 italic">
                         &quot;Based on their content, {data.person?.name} appears to value {typeof themesList[0] === 'string' ? themesList[0] : (themesList[0] as any)?.theme || "innovation"} and professional growth.&quot;
                      </p>
                   </div>
                </section>
             </div>

             {/* Right Column: Company & Strategy */}
             <div className="space-y-10">
                <section>
                   <div className="flex items-center gap-3 mb-6">
                      <span className="h-px flex-1 bg-gradient-to-r from-emerald-500/50 to-transparent"></span>
                      <h3 className="text-sm font-bold text-emerald-400 tracking-widest uppercase">Company Context</h3>
                   </div>
                   <div className="prose prose-invert prose-sm text-slate-300">
                      {companyInfo.name && <h4 className="text-white font-semibold mb-2">{companyInfo.name}</h4>}
                      <ul className="list-disc pl-4 space-y-1">
                          {companyInfo.facts.map((fact: string, idx: number) => (
                              <li key={idx}>{fact}</li>
                          ))}
                          {companyInfo.facts.length === 0 && <p>No specific company facts available.</p>}
                      </ul>
                   </div>
                </section>
                
                <section>
                   <div className="flex items-center gap-3 mb-6">
                      <span className="h-px flex-1 bg-gradient-to-r from-amber-500/50 to-transparent"></span>
                      <h3 className="text-sm font-bold text-amber-400 tracking-widest uppercase">Suggested approach</h3>
                   </div>
                   <div className="space-y-4">
                      {conversationScenarios.map((conv: any, idx: number) => (
                         <div key={idx} className="bg-[#030014]/50 p-4 rounded-lg border border-white/5">
                            <h4 className="text-white font-medium text-sm mb-2 capitalize">{conv.scenario || `Scenario ${idx + 1}`}</h4>
                            <div className="space-y-3 pl-4 border-l border-white/10">
                               {conv.script?.slice(0, 4).map((line: any, i: number) => (
                                  <p key={i} className="text-xs text-slate-400">
                                     <span className="text-slate-500 uppercase text-[10px] mr-2">{line.speaker}:</span>
                                     {line.text}
                                  </p>
                               ))}
                            </div>
                         </div>
                      ))}
                      {conversationScenarios.length === 0 && (
                          <p className="text-slate-500 text-sm">No scenarios generated.</p>
                      )}
                   </div>
                </section>
             </div>

          </div>

          {/* Sources Section */}
          {data.sources && data.sources.length > 0 && (
            <div className="mt-16 pt-8 border-t border-white/5">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6 flex items-center gap-2">
                <Globe size={14} />
                Verified Sources
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {data.sources.map((source: any, idx: number) => (
                  <a 
                    key={idx}
                    href={source.uri}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 transition-all group"
                  >
                    <div className="w-8 h-8 rounded bg-slate-800 flex items-center justify-center shrink-0">
                         <Globe size={14} className="text-slate-400" />
                    </div>
                    <div className="overflow-hidden">
                        <p className="text-sm text-slate-200 truncate font-medium group-hover:text-indigo-400 transition-colors">{source.title || "Source Link"}</p>
                        <p className="text-xs text-slate-500 truncate">{source.uri ? new URL(source.uri).hostname : "External Link"}</p>
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

export default BriefingCard;