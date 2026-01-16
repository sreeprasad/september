import { Lightbulb, Info } from "lucide-react";

export default function WhyPanel({ reasoning }: { reasoning: any[] }) {
  // If no structured reasoning, show placeholder or handle empty
  if (!reasoning || reasoning.length === 0) {
      return (
         <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <div className="flex items-center gap-2 mb-4">
                <Lightbulb className="w-5 h-5 text-amber-500" />
                <h3 className="text-lg font-semibold text-slate-900">Why These Insights?</h3>
            </div>
            <p className="text-sm text-slate-500 italic">No specific reasoning chain available.</p>
         </div>
      )
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="w-5 h-5 text-amber-500" />
        <h3 className="text-lg font-semibold text-slate-900">Why These Insights?</h3>
      </div>
      
      <div className="space-y-4">
        {reasoning.map((item, index) => (
          <div key={index} className="relative pl-4 border-l-2 border-amber-200">
             {/* Handle both string format and object format if API varies */}
             {typeof item === 'string' ? (
                 <p className="text-sm text-slate-700">{item}</p>
             ) : (
                <>
                    <p className="font-medium text-slate-900 text-sm">{item.decision || "Decision"}</p>
                    <p className="text-sm text-slate-600 mt-1">Because: {item.reason}</p>
                    {item.evidence && (
                        <div className="flex items-center gap-1 mt-1 text-xs text-slate-400">
                            <Info className="w-3 h-3" />
                            <span>Evidence: {item.evidence}</span>
                        </div>
                    )}
                </>
             )}
          </div>
        ))}
      </div>
    </div>
  );
}
