"use client";

import { useState } from "react";
import { Search, Loader2 } from "lucide-react";

// Components will be imported here
import ProfileCard from "./components/ProfileCard";
import ThemeChart from "./components/ThemeChart";
import TalkingPoints from "./components/TalkingPoints";
import WhyPanel from "./components/WhyPanel";
import MockConversations from "./components/MockConversations";

export default function Home() {
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [meetingContext, setMeetingContext] = useState("first meeting, potential partnership");
  const [twitterUrl, setTwitterUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [briefingData, setBriefingData] = useState<any>(null);

  const handleGenerate = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/briefing/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          linkedin_url: linkedinUrl,
          twitter_url: twitterUrl,
          meeting_context: meetingContext,
        }),
      });
      const data = await response.json();
      setBriefingData(data);
    } catch (error) {
      console.error("Error generating briefing:", error);
      alert("Failed to generate briefing. Please check the backend connection.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-slate-900 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-slate-900">Brief Me</h1>
          <p className="text-slate-500">Intelligent Meeting Preparation Dashboard</p>
        </div>

        {/* Input Section */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">LinkedIn URL</label>
              <input
                type="text"
                placeholder="https://linkedin.com/in/..."
                className="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                value={linkedinUrl}
                onChange={(e) => setLinkedinUrl(e.target.value)}
              />
            </div>
             <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Twitter URL (Optional)</label>
              <input
                type="text"
                placeholder="https://twitter.com/..."
                className="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                value={twitterUrl}
                onChange={(e) => setTwitterUrl(e.target.value)}
              />
            </div>
          </div>
          
           <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Meeting Context</label>
              <select 
                className="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                value={meetingContext}
                onChange={(e) => setMeetingContext(e.target.value)}
              >
                <option value="first meeting, potential partnership">First Meeting - Partnership</option>
                <option value="sales pitch">Sales Pitch</option>
                <option value="mentorship request">Mentorship Request</option>
                <option value="job interview">Job Interview</option>
              </select>
            </div>

          <button
            onClick={handleGenerate}
            disabled={isLoading || !linkedinUrl}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Generating Insights...
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                Generate Briefing
              </>
            )}
          </button>
        </div>

        {/* Results Section */}
        {briefingData && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Column: Profile & Context */}
            <div className="lg:col-span-4 space-y-6">
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
        )}
      </div>
    </div>
  );
}
