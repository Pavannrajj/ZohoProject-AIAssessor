export interface PendingAction {
  action: string;
  description: string;
  [key: string]: unknown;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  pending_action: PendingAction | null;
}
