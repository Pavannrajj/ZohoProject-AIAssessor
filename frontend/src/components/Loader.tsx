import { MessageSquare } from 'lucide-react';

export default function Loader() {
  return (
    <div className="flex gap-3 flex-row">
      <div className="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center bg-slate-200">
        <MessageSquare className="w-4 h-4 text-slate-600" />
      </div>
      <div className="bg-white border border-slate-200 shadow-sm rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-1">
        {[0, 1, 2].map(i => (
          <span
            key={i}
            className="w-2 h-2 rounded-full bg-slate-400 animate-bounce"
            style={{ animationDelay: `${i * 150}ms` }}
          />
        ))}
      </div>
    </div>
  );
}
