import { MessageSquare, Zap, Shield, ArrowRight } from 'lucide-react';
import { getLoginUrl } from '../api';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="px-8 py-5 flex items-center gap-3 border-b border-slate-200 bg-white">
        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
          <MessageSquare className="w-4 h-4 text-white" />
        </div>
        <span className="font-semibold text-slate-800 text-lg tracking-tight">ZohoChat</span>
      </header>

      {/* Hero */}
      <main className="flex-1 flex items-center justify-center px-6 py-16">
        <div className="max-w-md w-full">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-10 text-center">
            <div className="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <MessageSquare className="w-8 h-8 text-blue-600" />
            </div>

            <h1 className="text-2xl font-bold text-slate-900 mb-2">
              Zoho Projects Assistant
            </h1>
            <p className="text-slate-500 text-sm leading-relaxed mb-8">
              Manage your projects, tasks, and workflows using natural language. Powered by AI.
            </p>

            <button
              onClick={() => { window.location.href = getLoginUrl(); }}
              className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-xl transition-colors duration-150 text-sm"
            >
              Sign in with Zoho
              <ArrowRight className="w-4 h-4" />
            </button>

            <div className="mt-8 pt-8 border-t border-slate-100 grid grid-cols-3 gap-4">
              {[
                { icon: Zap, label: 'Instant actions', desc: 'Create & update tasks' },
                { icon: Shield, label: 'Confirm changes', desc: 'Review before apply' },
                { icon: MessageSquare, label: 'Natural chat', desc: 'Plain English queries' },
              ].map(({ icon: Icon, label, desc }) => (
                <div key={label} className="flex flex-col items-center gap-1">
                  <div className="w-8 h-8 bg-slate-100 rounded-lg flex items-center justify-center">
                    <Icon className="w-4 h-4 text-slate-600" />
                  </div>
                  <span className="text-xs font-medium text-slate-700">{label}</span>
                  <span className="text-xs text-slate-400 text-center leading-tight">{desc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <footer className="text-center py-4 text-xs text-slate-400">
        Powered by Gemini + LangGraph
      </footer>
    </div>
  );
}
