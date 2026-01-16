import { Briefcase, Building2, ExternalLink } from "lucide-react";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export default function ProfileCard({ person, companyContext }: { person: any, companyContext: any }) {
  if (!person) return null;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow duration-300">
      <div className="h-32 bg-gradient-to-br from-indigo-600 via-purple-600 to-violet-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-white/10 backdrop-blur-[2px]"></div>
        <div className="absolute top-0 right-0 p-4 opacity-50">
            <svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="60" cy="60" r="50" stroke="white" strokeWidth="2" strokeOpacity="0.2"/>
                <circle cx="90" cy="30" r="20" stroke="white" strokeWidth="2" strokeOpacity="0.2"/>
            </svg>
        </div>
      </div>
      
      <div className="px-6 pb-6 relative">
        <div className="flex justify-between items-end -mt-12 mb-4">
            <div className="w-24 h-24 rounded-2xl border-4 border-white bg-slate-100 shadow-md flex items-center justify-center text-2xl font-bold text-slate-400 overflow-hidden relative z-10">
                {person.photo_url ? (
                    /* eslint-disable-next-line @next/next/no-img-element */
                    <img src={person.photo_url} alt={person.name} className="w-full h-full object-cover" />
                ) : (
                    <span className="select-none bg-indigo-50 w-full h-full flex items-center justify-center text-indigo-300">
                        {person.name?.charAt(0) || "?"}
                    </span>
                )}
            </div>
            <a href="#" className="mb-1 p-2 bg-slate-50 rounded-full hover:bg-slate-100 text-slate-400 hover:text-indigo-600 transition-colors border border-slate-200">
                <ExternalLink className="w-4 h-4" />
            </a>
        </div>
        
        <div className="space-y-1">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">{person.name}</h2>
          <div className="flex flex-wrap gap-2 text-sm font-medium text-slate-600 mt-1">
             <span className="flex items-center gap-1.5">
                <Briefcase className="w-4 h-4 text-slate-400" />
                {person.role}
             </span>
             <span className="text-slate-300">•</span>
             <span className="flex items-center gap-1.5 text-indigo-600">
                <Building2 className="w-4 h-4" />
                {person.company}
             </span>
          </div>
          
          <div className="mt-4 p-3 bg-indigo-50/50 border border-indigo-100 rounded-lg">
             <p className="text-indigo-900 text-sm italic font-medium">&quot;{person.professional_identity}&quot;</p>
          </div>
        </div>

        <div className="mt-6 space-y-3 pt-6 border-t border-slate-100">
          <div className="flex items-start gap-3">
             <div className="p-1.5 bg-green-100 rounded text-green-700 mt-0.5">
                <Building2 className="w-3.5 h-3.5" />
             </div>
             <div>
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-0.5">Recent Company News</p>
                <p className="text-sm text-slate-700 leading-snug">{companyContext?.recent_developments?.[0] || "No recent news available."}</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
