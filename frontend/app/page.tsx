"use client";

import React, { useState } from "react";
import DottedBackground from "./components/DottedBackground";
import Header from "./components/Header";
import InputForm from "./components/InputForm";
import BriefingCard from "./components/BriefingCard";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [briefingData, setBriefingData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (data: { profileUrl: string; twitterHandle: string; context: string }) => {
    setIsLoading(true);
    setError(null);
    setBriefingData(null);
    
    try {
      const response = await fetch("http://localhost:8000/api/briefing/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          linkedin_url: data.profileUrl,
          twitter_url: data.twitterHandle,
          meeting_context: data.context,
        }),
      });
      
      const responseData = await response.json();
      
      if (!response.ok) {
        // #region agent log
        fetch('http://127.0.0.1:7247/ingest/80f3ef17-6c9f-413b-8834-23a71a0136f6',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'frontend/app/page.tsx:34',message:'Generate request failed',data:{status: response.status},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'H_API_CONNECT'})}).catch(()=>{});
        // #endregion
        throw new Error(responseData.detail || "Failed to generate briefing");
      }
      
      // #region agent log
      fetch('http://127.0.0.1:7247/ingest/80f3ef17-6c9f-413b-8834-23a71a0136f6',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'frontend/app/page.tsx:37',message:'Generate request success',data:{},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'H_API_CONNECT'})}).catch(()=>{});
      // #endregion

      setBriefingData(responseData);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      console.error("Error generating briefing:", error);
      setError(error.message || "Failed to generate briefing. Please check the backend connection.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloseBriefing = () => {
    setBriefingData(null);
  };

  return (
    <div className="relative min-h-screen font-sans antialiased selection:bg-indigo-500/30 selection:text-white overflow-x-hidden">
      <DottedBackground />
      <Header />

      <main className="relative z-10 container mx-auto px-4 pt-36 pb-20 flex flex-col items-center min-h-screen">
        
        {/* Hero Section */}
        {!briefingData && (
          <div className="text-center mb-12 max-w-4xl animate-in fade-in zoom-in-95 duration-700">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-[11px] font-medium text-slate-400 mb-8 hover:bg-white/10 transition-colors cursor-default tracking-wide uppercase">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse" aria-hidden="true"></span>
              Powered by Yutori • TinyFish • Cline • Tonic • Retool • Freepik
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white mb-8 leading-[1.1]">
              Preparation is your <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400">
                unfair advantage.
              </span>
            </h1>
            
            <p className="text-slate-400 text-xl font-light leading-relaxed max-w-2xl mx-auto mb-10">
              Generate elite-level dossier briefings on anyone in seconds. <br className="hidden md:block" aria-hidden="true"/>
              Walk into every meeting knowing exactly what to say.
            </p>
          </div>
        )}

        {/* Main Interface */}
        <div className="w-full flex flex-col items-center transition-all duration-500">
          {!briefingData ? (
            <InputForm onSubmit={handleGenerate} isLoading={isLoading} />
          ) : (
             <BriefingCard data={briefingData} onClose={handleCloseBriefing} />
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-8 px-6 py-4 bg-red-500/10 border border-red-500/20 text-red-200 rounded-xl flex items-center gap-3 backdrop-blur-sm animate-in fade-in slide-in-from-bottom-2">
              <span className="text-red-400 font-bold">!</span>
              <span className="font-medium">{error}</span>
              </div>
          )}
        </div>

      </main>

      {/* Footer / Copyright */}
      <footer className="fixed bottom-6 w-full text-center z-20 pointer-events-none">
        <p className="text-slate-600 text-xs font-medium tracking-wide">
          BRIEFME INTELLIGENCE SUITE &copy; {new Date().getFullYear()}
        </p>
      </footer>
    </div>
  );
}
