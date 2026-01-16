"use client";

import { useState } from "react";
import { Sparkles, History, ArrowRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

// Components
import ProfileCard from "./components/ProfileCard";
import ThemeChart from "./components/ThemeChart";
import TalkingPoints from "./components/TalkingPoints";
import WhyPanel from "./components/WhyPanel";
import MockConversations from "./components/MockConversations";
import AgentProgress from "./components/AgentProgress";
import AnimatedBackground from "./components/AnimatedBackground";

export default function Home() {
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [meetingContext, setMeetingContext] = useState("first meeting, potential partnership");
  const [twitterUrl, setTwitterUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [briefingData, setBriefingData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch("http://localhost:8000/api/briefing/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          linkedin_url: linkedinUrl,
          twitter_url: twitterUrl,
          meeting_context: meetingContext,
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || "Failed to generate briefing");
      }
      
      setBriefingData(data);
    } catch (error: any) {
      console.error("Error generating briefing:", error);
      setError(error.message || "Failed to generate briefing. Please check the backend connection.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen font-sans text-slate-900 selection:bg-indigo-100 selection:text-indigo-900">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 glass-panel border-b-0 rounded-none bg-white/80">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <motion.div 
              className="bg-gradient-to-tr from-indigo-600 to-violet-600 p-1.5 rounded-lg shadow-lg shadow-indigo-500/30"
              animate={{ 
                scale: [1, 1.05, 1],
                boxShadow: [
                  "0 10px 15px -3px rgba(99, 102, 241, 0.3)",
                  "0 10px 20px -3px rgba(99, 102, 241, 0.5)",
                  "0 10px 15px -3px rgba(99, 102, 241, 0.3)"
                ]
              }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            >
              <Sparkles className="w-5 h-5 text-white" />
            </motion.div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600">
              BriefMe
            </span>
          </div>
          <div className="flex items-center gap-4 text-sm font-medium text-slate-600">
            <button className="hover:text-slate-900 transition-colors px-3 py-1.5 hover:bg-slate-100/50 rounded-lg">History</button>
            <button className="hover:text-slate-900 transition-colors px-3 py-1.5 hover:bg-slate-100/50 rounded-lg">Templates</button>
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-100 to-violet-100 border border-white shadow-sm flex items-center justify-center text-indigo-700 font-bold text-xs">
              JD
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-10 relative">
        <AnimatePresence mode="wait">
          {!briefingData ? (
            <motion.div 
              key="hero"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-3xl mx-auto space-y-10 mt-12"
            >
              <div className="text-center space-y-6">
                <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.1] tracking-tight">
                  Master every meeting with <br/>
                  <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600">AI-powered intel</span>.
                </h1>
                <p className="text-xl text-slate-500 max-w-xl mx-auto leading-relaxed font-light">
                  Instant deep-dive research and roleplay simulations for any LinkedIn profile.
                </p>
              </div>

              <motion.div 
                className="glass-panel p-8 rounded-3xl space-y-8 relative overflow-hidden group border border-white/40 shadow-2xl shadow-indigo-100/50"
                initial={{ scale: 0.98, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.1, ease: "easeOut" }}
              >
                <AnimatedBackground />
                
                {isLoading ? (
                  <div className="py-8 relative z-10">
                    <AgentProgress />
                  </div>
                ) : (
                  <>
                    <div className="space-y-6 relative z-10">
                      <div className="space-y-2">
                        <label className="text-xs font-bold uppercase tracking-wider text-slate-400 ml-1">Target Profile</label>
                        <div className="relative group/input">
                          <input
                            type="text"
                            placeholder="https://linkedin.com/in/username"
                            className="w-full pl-4 pr-4 py-4 bg-white/80 backdrop-blur-sm border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 outline-none transition-all shadow-sm text-lg placeholder:text-slate-300 group-hover/input:border-indigo-200"
                            value={linkedinUrl}
                            onChange={(e) => setLinkedinUrl(e.target.value)}
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                          <label className="text-xs font-bold uppercase tracking-wider text-slate-400 ml-1">Twitter (Optional)</label>
                          <input
                            type="text"
                            placeholder="@username"
                            className="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 outline-none transition-all shadow-sm placeholder:text-slate-300 hover:border-indigo-200"
                            value={twitterUrl}
                            onChange={(e) => setTwitterUrl(e.target.value)}
                          />
                        </div>
                        <div className="space-y-2">
                          <label className="text-xs font-bold uppercase tracking-wider text-slate-400 ml-1">Meeting Context</label>
                          <div className="relative">
                            <select 
                              className="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-100 focus:border-indigo-500 outline-none transition-all appearance-none shadow-sm cursor-pointer hover:border-indigo-200"
                              value={meetingContext}
                              onChange={(e) => setMeetingContext(e.target.value)}
                            >
                              <option value="first meeting, potential partnership">🤝 Partnership Meeting</option>
                              <option value="sales pitch">💼 Sales Pitch</option>
                              <option value="mentorship request">🎓 Mentorship Request</option>
                              <option value="job interview">📝 Job Interview</option>
                            </select>
                            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
                              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              </svg>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {error && (
                      <div className="p-4 bg-red-50 text-red-700 rounded-xl text-sm flex items-center gap-2 border border-red-100 animate-in fade-in slide-in-from-top-2 relative z-10">
                        <div className="w-1.5 h-1.5 rounded-full bg-red-600"></div>
                        {error}
                      </div>
                    )}

                    <button
                      onClick={handleGenerate}
                      disabled={isLoading || !linkedinUrl}
                      className="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-4 rounded-xl transition-all shadow-xl shadow-slate-900/20 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed group relative overflow-hidden z-10"
                    >
                      <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500 opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-[length:200%_auto] animate-gradient"></div>
                      <span className="relative flex items-center gap-2">
                        Generate Briefing <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                      </span>
                    </button>
                  </>
                )}
              </motion.div>
            </motion.div>
          ) : (
            <motion.div
              key="dashboard"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="space-y-8"
            >
              <div className="flex items-center justify-between glass-panel p-4 rounded-2xl sticky top-20 z-40 bg-white/90">
                <div className="flex items-center gap-4">
                    <div className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                      Ready
                    </div>
                    <div>
                        <h2 className="text-lg font-bold text-slate-900">Meeting Briefing</h2>
                        <p className="text-sm text-slate-500 flex items-center gap-1">
                          Generated for <span className="font-medium text-slate-700">{meetingContext}</span>
                        </p>
                    </div>
                </div>
                <button 
                    onClick={() => setBriefingData(null)}
                    className="text-sm font-medium text-slate-600 hover:text-indigo-600 flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-slate-50 transition-colors border border-transparent hover:border-slate-200"
                >
                    <History className="w-4 h-4" />
                    New Search
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                {/* Left Column: Profile & Context (Sticky) */}
                <div className="lg:col-span-4 space-y-6 lg:sticky lg:top-44">
                  <ProfileCard person={briefingData.person} companyContext={briefingData.company_context} />
                  <ThemeChart themes={briefingData.themes} />
                </div>

                {/* Middle Column: Talking Points & Reasoning */}
                <div className="lg:col-span-4 space-y-6">
                  <TalkingPoints points={briefingData.talking_points || []} />
                  <WhyPanel reasoning={briefingData.decision_metadata?.decision_rationale || []} />
                </div>

                {/* Right Column: Mock Conversations */}
                <div className="lg:col-span-4 space-y-6">
                  <MockConversations conversations={briefingData.mock_conversations} />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
