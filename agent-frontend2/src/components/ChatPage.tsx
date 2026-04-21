import { useEffect, useRef, useState } from 'react';
import { MessageSquare, LogOut } from 'lucide-react';
import { sendMessage } from '../api';
import type { ChatMessage, PendingAction } from '../types';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import ConfirmationCard from './ConfirmationCard';
import Loader from './Loader';

let msgCounter = 0;
function newId() {
  return `msg-${++msgCounter}`;
}

function makeMessage(role: ChatMessage['role'], content: string): ChatMessage {
  return { id: newId(), role, content, timestamp: new Date() };
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    makeMessage('bot', 'Hi! I am your Zoho Projects assistant. Ask me anything about your projects, tasks, or team.'),
  ]);
  const [loading, setLoading] = useState(false);
  const [pendingAction, setPendingAction] = useState<PendingAction | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading, pendingAction]);

  async function handleSend(text: string) {
    setMessages(prev => [...prev, makeMessage('user', text)]);
    setLoading(true);
    setPendingAction(null);

    try {
      const data = await sendMessage(text);
      setMessages(prev => [
  ...prev,
  makeMessage('bot', data.response)
]);
      if (data.pending_action) {
        setPendingAction(data.pending_action);
      }
    } catch {
      setMessages(prev => [...prev, makeMessage('bot', 'Sorry, something went wrong. Please try again.')]);
    } finally {
      setLoading(false);
    }
  }

  async function handleConfirm() {
    setPendingAction(null);
    await handleSend('confirm');
  }

  async function handleCancel() {
    setPendingAction(null);
    await handleSend('cancel');
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-10 bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <MessageSquare className="w-4 h-4 text-white" />
          </div>
          <div>
            <span className="font-semibold text-slate-800 text-sm block leading-tight">ZohoChat</span>
            <span className="text-xs text-slate-400">Zoho Projects Assistant</span>
          </div>
        </div>
        <button
          onClick={() => { window.location.href = 'http://localhost:8000/auth/logout'; }}
          className="flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-700 transition-colors px-3 py-1.5 rounded-lg hover:bg-slate-100"
        >
          <LogOut className="w-3.5 h-3.5" />
          Sign out
        </button>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-4 py-6 max-w-3xl mx-auto w-full">
        <div className="flex flex-col gap-4">
          {messages.map(msg => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {/* Pending action confirmation */}
          {pendingAction && !loading && (
            <ConfirmationCard
              action={pendingAction}
              onConfirm={handleConfirm}
              onCancel={handleCancel}
              disabled={loading}
            />
          )}

          {/* Loading indicator */}
          {loading && <Loader />}

          <div ref={bottomRef} />
        </div>
      </main>

      {/* Input */}
      <footer className="sticky bottom-0 bg-slate-50 border-t border-slate-200 px-4 py-4">
        <div className="max-w-3xl mx-auto">
          <ChatInput onSend={handleSend} disabled={loading || pendingAction !== null} />
          <p className="text-xs text-slate-400 text-center mt-2">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </footer>
    </div>
  );
}
