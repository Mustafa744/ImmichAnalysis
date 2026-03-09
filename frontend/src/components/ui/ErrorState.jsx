import { AlertTriangle, RefreshCw } from "lucide-react";

export default function ErrorState({
  message = "Something went wrong",
  onRetry,
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-10 text-center">
      <AlertTriangle size={32} className="text-warning" />
      <p className="text-sm text-text-secondary">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-lg bg-accent/10 text-accent hover:bg-accent/20 transition-colors cursor-pointer"
        >
          <RefreshCw size={14} />
          Retry
        </button>
      )}
    </div>
  );
}
