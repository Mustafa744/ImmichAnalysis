import { Calendar } from "lucide-react";

export default function DateRangePicker({ dateFrom, dateTo, onChange }) {
  return (
    <div className="flex items-center gap-2">
      <Calendar size={14} className="text-text-muted" />
      <input
        type="date"
        value={dateFrom}
        onChange={(e) => onChange(e.target.value, dateTo)}
        className="bg-bg-card border border-border rounded-lg px-3 py-1.5 text-xs text-text-primary focus:outline-none focus:border-accent/50 transition-colors"
      />
      <span className="text-text-muted text-xs">—</span>
      <input
        type="date"
        value={dateTo}
        onChange={(e) => onChange(dateFrom, e.target.value)}
        className="bg-bg-card border border-border rounded-lg px-3 py-1.5 text-xs text-text-primary focus:outline-none focus:border-accent/50 transition-colors"
      />
    </div>
  );
}
