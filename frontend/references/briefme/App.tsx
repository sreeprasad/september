import React, { useState } from 'react';
import { Header } from './components/Header';
import { DottedBackground } from './components/DottedBackground';
import { InputForm } from './components/InputForm';
import { BriefingCard } from './components/BriefingCard';
import { generateBriefing } from './services/geminiService';
import { BriefingResponse } from './types';

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [briefing, setBriefing] = useState<BriefingResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (data: { profileUrl: string; twitterHandle: string; context: string }) => {
    setIsLoading(true);
    setError(null);
    setBriefing(null);

    try {
      const result = await generateBriefing(data);
      setBriefing(result);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCloseBriefing = () => {
    setBriefing(null);
  };

  return (
    <div className="relative min-h-screen font-sans antialiased selection:bg-brief-primary/30 selection:text-white">
      <DottedBackground />
      <Header />

      <main className="relative z-10 container mx-auto px-4 pt-36 pb-20 flex flex-col items-center min-h-screen">
        
        {/* Hero Section */}
        {!briefing && (
          <div className="text-center mb-12 max-w-3xl animate-in fade-in zoom-in-95 duration-700">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-slate-300 mb-6 hover:bg-white/10 transition-colors cursor-default">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              Powered by Gemini 3.0 Model
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white mb-8 leading-[1.1]">
              Preparation is your <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400">
                unfair advantage.
              </span>
            </h1>
            
            <p className="text-slate-400 text-xl font-light leading-relaxed max-w-2xl mx-auto mb-10">
              Generate elite-level dossier briefings on anyone in seconds. <br className="hidden md:block"/>
              Walk into every meeting knowing exactly what to say.
            </p>
          </div>
        )}

        {/* Main Interface */}
        <div className="w-full flex flex-col items-center transition-all duration-500">
          {!briefing ? (
            <InputForm onSubmit={handleGenerate} isLoading={isLoading} />
          ) : (
             <BriefingCard data={briefing} onClose={handleCloseBriefing} />
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-8 px-6 py-4 bg-red-500/10 border border-red-500/20 text-red-200 rounded-xl flex items-center gap-3 backdrop-blur-sm animate-in fade-in slide-in-from-bottom-2">
              <span className="material-symbols-outlined text-red-400">error_outline</span>
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
};

export default App;