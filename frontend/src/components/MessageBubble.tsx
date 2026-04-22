import { MessageSquare, User } from 'lucide-react';
import type { ChatMessage } from '../types';

interface Props {
  message: ChatMessage;
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center ${
        isUser ? 'bg-blue-600' : 'bg-slate-200'
      }`}>
        {isUser
          ? <User className="w-4 h-4 text-white" />
          : <MessageSquare className="w-4 h-4 text-slate-600" />
        }
      </div>

      {/* Bubble */}
      <div className={`max-w-[72%] flex flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
          isUser
            ? 'bg-blue-600 text-white rounded-tr-sm'
            : 'bg-white text-slate-800 border border-slate-200 shadow-sm rounded-tl-sm'
        }`}>
          {message.content}
        </div>
        <span className="text-xs text-slate-400 px-1">{formatTime(message.timestamp)}</span>
      </div>
    </div>
  );
}
