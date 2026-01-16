"use client";

import React, { useState, useRef } from "react";
import DottedBackground from "../components/DottedBackground";
import Header from "../components/Header";
import { Upload, FileText, AlertTriangle, CheckCircle, Search, Loader2 } from "lucide-react";

interface Violation {
  severity: "HIGH" | "MEDIUM" | "LOW";
  rule_code: string;
  explanation: string;
  quote: string;
  suggestion: string;
}

interface AnalyzeResult {
  total_violations: number;
  risk_level: "HIGH" | "MEDIUM" | "LOW" | "NONE";
  summary: string;
  violations: Violation[];
  transcript?: string;
}

export default function AnalyzePage() {
  const [activeTab, setActiveTab] = useState<"upload" | "text">("upload");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [transcript, setTranscript] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/analyze-audio", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Analysis failed");
      }

      const data = await response.json();
      setResult(data);
      // If the backend returns the transcript as part of the response, set it.
      // The current backend implementation of /analyze-audio returns AnalyzeResponse which doesn't strictly have transcript field in the Pydantic model,
      // but let's check if we can get it.
      // Actually, looking at backend code:
      // analyze_audio calls transcribe_audio (returns transcript) then analyze_compliance.
      // It returns AnalyzeResponse. We might need to modify backend to return transcript too if we want to show it.
      // For now, assuming the backend might be updated or we rely on what we have.
      // Wait, let's check backend again.
      // The /analyze-audio endpoint returns `analyze_result` which is `AnalyzeResponse`.
      // It DOES NOT return the transcript text itself in the response model.
      // However, /analyze-audio-base64 DOES return `{**compliance_result, "transcript": transcript}`.
      // Let's assume for now we might not get transcript text back from /analyze-audio unless we update backend.
      // BUT, let's try to handle it if it does comes back or if we use the text input flow.
      
      // If we want to show transcript, we should probably update backend /analyze-audio to return it.
      // But I cannot modify backend in this step easily without going back.
      // Let's proceed with what we have. If transcript is missing in UI, we can note it.
      
    } catch (error: unknown) {
      console.error("Error analyzing audio:", error);
      const errorMessage = error instanceof Error ? error.message : "Please try again.";
      alert(`Failed to analyze audio: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTextAnalyze = async () => {
    if (!transcript.trim()) return;

    setIsLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Analysis failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (error: unknown) {
      console.error("Error analyzing text:", error);
      const errorMessage = error instanceof Error ? error.message : "Please try again.";
      alert(`Failed to analyze text: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen font-sans antialiased selection:bg-indigo-500/30 selection:text-white overflow-x-hidden">
      <DottedBackground />
      <Header />

      <main className="relative z-10 container mx-auto px-4 pt-36 pb-20 flex flex-col items-center min-h-screen">
        
        {/* Header */}
        <div className="text-center mb-10 max-w-2xl animate-in fade-in zoom-in-95 duration-700">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-slate-300 mb-6 hover:bg-white/10 transition-colors cursor-default">
            <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
            Compliance Engine
          </div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-white mb-6">
            Call Analyzer
          </h1>
          <p className="text-slate-400 text-lg font-light leading-relaxed">
            Upload call recordings or paste transcripts to detect compliance risks automatically.
          </p>
        </div>

        {/* Input Section */}
        <div className="w-full max-w-4xl glass-panel rounded-2xl p-6 mb-10 animate-in slide-in-from-bottom-4 duration-700 delay-100">
          <div className="flex gap-4 mb-6 border-b border-white/10 pb-4">
            <button
              onClick={() => setActiveTab("upload")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "upload"
                  ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/20"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <Upload className="w-4 h-4" />
              Upload Audio
            </button>
            <button
              onClick={() => setActiveTab("text")}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "text"
                  ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/20"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <FileText className="w-4 h-4" />
              Paste Transcript
            </button>
          </div>

          {activeTab === "upload" ? (
            <div 
              className="border-2 border-dashed border-white/10 rounded-xl p-10 text-center hover:border-indigo-500/50 hover:bg-white/5 transition-all cursor-pointer group"
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept="audio/*"
                onChange={handleFileUpload}
              />
              <div className="w-16 h-16 bg-indigo-500/10 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                <Upload className="w-8 h-8 text-indigo-400" />
              </div>
              <p className="text-white font-medium mb-1">Click to upload or drag and drop</p>
              <p className="text-slate-500 text-sm">MP3, WAV, M4A (Max 10MB)</p>
            </div>
          ) : (
            <div className="space-y-4">
              <textarea
                value={transcript}
                onChange={(e) => setTranscript(e.target.value)}
                placeholder="Paste call transcript here..."
                className="w-full h-48 bg-[#0B0C15]/50 border border-white/10 rounded-xl p-4 text-white placeholder:text-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/50 resize-none text-sm leading-relaxed"
              />
              <div className="flex justify-end">
                <button
                  onClick={handleTextAnalyze}
                  disabled={isLoading || !transcript.trim()}
                  className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2 rounded-lg font-medium text-sm transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4" />
                      Analyze Text
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="w-full max-w-4xl space-y-6 animate-in slide-in-from-bottom-8 duration-700">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-panel p-6 rounded-2xl flex items-center justify-between border-l-4 border-l-indigo-500">
                <div>
                  <p className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-1">Total Violations</p>
                  <p className="text-3xl font-bold text-white">{result.total_violations}</p>
                </div>
                <div className={`p-3 rounded-xl ${result.total_violations > 0 ? "bg-red-500/10 text-red-400" : "bg-green-500/10 text-green-400"}`}>
                  <AlertTriangle className="w-6 h-6" />
                </div>
              </div>
              
              <div className={`glass-panel p-6 rounded-2xl flex items-center justify-between border-l-4 ${
                result.risk_level === "HIGH" ? "border-l-red-500" : 
                result.risk_level === "MEDIUM" ? "border-l-yellow-500" : "border-l-green-500"
              }`}>
                <div>
                  <p className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-1">Risk Level</p>
                  <p className={`text-3xl font-bold ${
                    result.risk_level === "HIGH" ? "text-red-400" : 
                    result.risk_level === "MEDIUM" ? "text-yellow-400" : "text-green-400"
                  }`}>{result.risk_level}</p>
                </div>
                <div className="p-3 rounded-xl bg-white/5 text-slate-300">
                  <CheckCircle className="w-6 h-6" />
                </div>
              </div>
            </div>

            {/* Summary */}
            <div className="glass-panel p-6 rounded-2xl">
                <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                    <span className="w-1.5 h-4 bg-indigo-500 rounded-full"></span>
                    Executive Summary
                </h3>
                <p className="text-slate-300 leading-relaxed text-sm">
                    {result.summary}
                </p>
            </div>

            {/* Violations Table */}
            {result.violations && result.violations.length > 0 ? (
                <div className="glass-panel rounded-2xl overflow-hidden">
                    <div className="p-6 border-b border-white/5">
                        <h3 className="text-white font-semibold flex items-center gap-2">
                            <span className="w-1.5 h-4 bg-red-500 rounded-full"></span>
                            Compliance Violations
                        </h3>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-white/5 text-slate-400 uppercase text-xs font-semibold tracking-wider">
                                <tr>
                                    <th className="px-6 py-4">Severity</th>
                                    <th className="px-6 py-4">Rule Code</th>
                                    <th className="px-6 py-4">Explanation</th>
                                    <th className="px-6 py-4">Suggestion</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {result.violations.map((violation, idx) => (
                                    <tr key={idx} className="hover:bg-white/5 transition-colors">
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded text-xs font-bold border ${
                                                violation.severity === "HIGH" ? "bg-red-500/10 text-red-400 border-red-500/20" :
                                                violation.severity === "MEDIUM" ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20" :
                                                "bg-blue-500/10 text-blue-400 border-blue-500/20"
                                            }`}>
                                                {violation.severity}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-white font-mono text-xs">{violation.rule_code}</td>
                                        <td className="px-6 py-4 text-slate-300 max-w-xs">
                                            <p className="mb-2">{violation.explanation}</p>
                                            <div className="bg-white/5 p-2 rounded border border-white/5 text-xs italic text-slate-400">
                                                &quot;{violation.quote}&quot;
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-emerald-400">{violation.suggestion}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            ) : (
                <div className="glass-panel p-10 rounded-2xl flex flex-col items-center justify-center text-center">
                    <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center mb-4 text-green-500 border border-green-500/20">
                        <CheckCircle className="w-8 h-8" />
                    </div>
                    <h3 className="text-white font-bold text-lg mb-2">No Violations Detected</h3>
                    <p className="text-slate-400 max-w-md">The call appears to be fully compliant with all checked regulations.</p>
                </div>
            )}

            {/* Transcript (if available in result, or if we used text input) */}
            {(result.transcript || transcript) && (
                <div className="glass-panel p-6 rounded-2xl">
                    <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
                        <span className="w-1.5 h-4 bg-slate-500 rounded-full"></span>
                        Transcript
                    </h3>
                    <div className="bg-[#0B0C15]/50 rounded-xl p-6 border border-white/5 max-h-96 overflow-y-auto custom-scrollbar">
                        <p className="text-slate-300 whitespace-pre-wrap leading-relaxed text-sm">
                            {result.transcript || transcript}
                        </p>
                    </div>
                </div>
            )}

          </div>
        )}

      </main>
    </div>
  );
}
