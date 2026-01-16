import { MapPin, Briefcase, Building2 } from "lucide-react";

export default function ProfileCard({ person, companyContext }: { person: any, companyContext: any }) {
  if (!person) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <div className="h-24 bg-gradient-to-r from-indigo-500 to-purple-500"></div>
      <div className="px-6 pb-6">
        <div className="relative -mt-12 mb-4">
          <div className="w-24 h-24 rounded-full border-4 border-white bg-slate-200 flex items-center justify-center text-2xl font-bold text-slate-400 overflow-hidden">
             {person.photo_url ? (
                <img src={person.photo_url} alt={person.name} className="w-full h-full object-cover" />
             ) : (
                person.name?.charAt(0) || "?"
             )}
          </div>
        </div>
        
        <div className="space-y-1">
          <h2 className="text-xl font-bold text-slate-900">{person.name}</h2>
          <p className="text-slate-600 font-medium">{person.role} at {person.company}</p>
          <p className="text-indigo-600 text-sm italic">{person.professional_identity}</p>
        </div>

        <div className="mt-6 space-y-3 pt-6 border-t border-slate-100">
          <div className="flex items-center gap-2 text-sm text-slate-600">
            <Briefcase className="w-4 h-4" />
            <span>{person.company}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-600">
            <Building2 className="w-4 h-4" />
            <span>{companyContext?.recent_developments?.[0] || "No recent news"}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
