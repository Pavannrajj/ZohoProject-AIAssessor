import type { ChatResponse } from './types';

const BASE_URL = 'http://localhost:8000';

export async function sendMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }

  return res.json();
}

export function getLoginUrl(): string {
  return `${BASE_URL}/auth/login`;
}
