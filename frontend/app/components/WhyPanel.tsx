import { Lightbulb, Info, CheckCircle2, TrendingUp } from "lucide-react";

export default function WhyPanel({ reasoning }: { reasoning: any[] }) {
  if (!reasoning || reasoning.length === 0) {
      return (
         <div className="glass-panel p-6 rounded-2xl">
            <div className="flex items-center gap-3 mb-4">
                <div className="p-2.5 bg-amber-50 rounded-xl text-amber-600 border border-amber-100">
                    <Lightbulb className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold text-slate-900">Why These Insights?</h3>
            </div>
            <p className="text-sm text-slate-500 italic bg-slate-50 p-4 rounded-xl text-center">
              No specific reasoning chain available for this profile.
            </p>
         </div>
      )
  }

  return (
    <div className="glass-panel p-6 rounded-2xl relative overflow-hidden">
      {/* Decorative background element */}
      <div className="absolute -top-10 -right-10 w-40 h-40 bg-amber-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div className="flex items-center justify-between mb-8 relative z-10">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-amber-50 rounded-xl text-amber-600 border border-amber-100 shadow-sm">
              <Lightbulb className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Why These Insights?</h3>
            <p className="text-xs text-slate-500 font-medium">AI Decision Logic</p>
          </div>
        </div>
        <div className="flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-bold border border-green-100">
          <TrendingUp className="w-3 h-3" />
          High Confidence
        </div>
      </div>
      
      <div className="relative space-y-0 pl-3 relative z-10">
        {/* Timeline Line */}
        <div className="absolute top-3 bottom-10 left-[19px] w-[2px] bg-gradient-to-b from-slate-200 via-slate-200 to-transparent"></div>

        {reasoning.map((item, index) => (
          <div key={index} className="relative pl-12 pb-8 group last:pb-0">
             {/* Timeline Dot */}
             <div className="absolute left-[10px] top-0 w-5 h-5 rounded-full border-4 border-white bg-slate-200 ring-1 ring-slate-100 group-hover:bg-amber-500 group-hover:ring-amber-200 transition-all duration-500 z-10 shadow-sm"></div>
             
             {typeof item === 'string' ? (
                 <p className="text-sm text-slate-700 bg-white p-3 rounded-lg border border-slate-100 shadow-sm">{item}</p>
             ) : (
                <div className="bg-white rounded-xl p-5 border border-slate-200 hover:border-amber-300 hover:shadow-lg hover:shadow-amber-500/5 transition-all duration-300 relative group-hover:-translate-y-1">
                    <div className="absolute top-5 right-5 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                      <CheckCircle2 className="w-5 h-5 text-green-500" />
                    </div>

                    <div className="mb-2">
                      <p className="font-bold text-slate-900 text-[15px]">{item.decision || "Decision Point"}</p>
                    </div>
                    
                    <p className="text-sm text-slate-600 leading-relaxed mb-3">{item.reason}</p>
                    
                    {item.evidence && (
                        <div className="flex items-start gap-2 pt-3 border-t border-slate-100">
                            <Info className="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" />
                            <span className="text-xs text-slate-500 font-medium bg-slate-50 px-2 py-1 rounded border border-slate-100">
                              Evidence: {item.evidence}
                            </span>
                        </div>
                    )}
                </div>
             )}
          </div>
        ))}
      </div>
    </div>
  );
}
