"use client";

// Quote, Copy, Check removed as they are unused or sections removed
import { MessageSquare } from "lucide-react";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function TalkingPoints({ points }: { points: any[] }) {
  if (!points) return null;

  return (
    <div className="glass-panel p-6 rounded-2xl space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center text-indigo-600">
          <MessageSquare className="w-5 h-5" />
        </div>
        <h3 className="font-bold text-slate-800">Talking Points</h3>
      </div>

      <div className="space-y-4">
        {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
        {points.map((point: any, idx: number) => (
          <div key={idx} className="p-4 bg-slate-50/50 rounded-xl border border-slate-100 hover:border-indigo-100 transition-colors group">
            <h4 className="font-semibold text-slate-800 mb-1 group-hover:text-indigo-600 transition-colors">{point.topic}</h4>
            <p className="text-sm text-slate-600 leading-relaxed">{point.reasoning}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
