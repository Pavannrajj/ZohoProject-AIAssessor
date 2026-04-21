import { useState } from 'react';
import LoginPage from './components/LoginPage';
import ChatPage from './components/ChatPage';

type AppView = 'login' | 'chat';

function detectView(): AppView {
  const params = new URLSearchParams(window.location.search);
  if (params.get('auth') === 'success') {
    sessionStorage.setItem('zoho_authed', '1');
    window.history.replaceState({}, '', window.location.pathname);
    return 'chat';
  }
  return sessionStorage.getItem('zoho_authed') === '1' ? 'chat' : 'login';
}

export default function App() {
  const [view] = useState<AppView>(detectView);

  if (view === 'login') {
    return <LoginPage />;
  }

  return <ChatPage />;
}
