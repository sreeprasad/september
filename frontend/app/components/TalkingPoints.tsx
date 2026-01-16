import { MessageSquare } from "lucide-react";

export default function TalkingPoints({ points }: { points: any[] }) {
  if (!points || points.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <MessageSquare className="w-5 h-5 text-indigo-600" />
        <h3 className="text-lg font-semibold text-slate-900">Talking Points</h3>
      </div>
      
      <div className="space-y-3">
        {points.map((item, index) => (
          <div key={index} className="p-3 bg-slate-50 rounded-lg border border-slate-100 hover:border-indigo-200 transition-colors">
            <p className="font-medium text-slate-900">{item.point}</p>
            <p className="text-sm text-slate-500 mt-1">{item.context}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
