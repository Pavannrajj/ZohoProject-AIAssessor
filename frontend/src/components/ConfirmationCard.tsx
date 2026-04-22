import { AlertTriangle, Check, X } from 'lucide-react';
import type { PendingAction } from '../types';

interface Props {
  action: PendingAction;
  onConfirm: () => void;
  onCancel: () => void;
  disabled: boolean;
}

export default function ConfirmationCard({ action, onConfirm, onCancel, disabled }: Props) {
  return (
    <div className="flex justify-start">
      <div className="max-w-[72%] bg-amber-50 border border-amber-200 rounded-2xl rounded-tl-sm px-5 py-4 shadow-sm">
        <div className="flex items-start gap-3 mb-4">
          <div className="w-8 h-8 rounded-full bg-amber-100 flex items-center justify-center flex-shrink-0 mt-0.5">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-800 mb-1">Confirm Action</p>
            <p className="text-sm text-slate-600 leading-relaxed">
              {action.description ?? JSON.stringify(action, null, 2)}
            </p>
          </div>
        </div>

        {/* Action details */}
        {action.action && (
          <div className="mb-4 bg-white border border-amber-100 rounded-lg px-3 py-2">
            <span className="text-xs text-slate-500 font-medium uppercase tracking-wide">Action</span>
            <p className="text-sm text-slate-700 mt-0.5 font-mono">{action.action}</p>
          </div>
        )}

        <div className="flex gap-2">
          <button
            onClick={onConfirm}
            disabled={disabled}
            className="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 text-white disabled:text-slate-400 text-sm font-medium rounded-lg transition-colors"
          >
            <Check className="w-3.5 h-3.5" />
            Confirm
          </button>
          <button
            onClick={onCancel}
            disabled={disabled}
            className="flex items-center gap-1.5 px-4 py-2 bg-white hover:bg-slate-50 disabled:bg-slate-50 border border-slate-200 text-slate-700 disabled:text-slate-400 text-sm font-medium rounded-lg transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
