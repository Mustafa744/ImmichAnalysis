import { ImageIcon, Globe, Calendar, TrendingUp } from "lucide-react";
import Card from "../ui/Card";

const statConfig = [
  {
    key: "total_photos",
    label: "Total Photos",
    icon: ImageIcon,
    format: (v) => v?.toLocaleString() ?? "—",
  },
  {
    key: "countries",
    label: "Countries",
    icon: Globe,
    format: (v) => v ?? "—",
  },
  {
    key: "date_range",
    label: "Date Range",
    icon: Calendar,
    format: (v) => (v ? `${v.from} → ${v.to}` : "—"),
  },
  {
    key: "most_active_country",
    label: "Most Active Country",
    icon: TrendingUp,
    format: (v) => v ?? "—",
  },
];

export default function StatsCards({ data }) {
  if (!data) return null;

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 stagger-children">
      {statConfig.map(({ key, label, icon: Icon, format }) => (
        <div key={key} className="glass-card glass-card-hover p-5">
          <div className="flex items-center gap-2 mb-3">
            <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-accent/10">
              <Icon size={16} className="text-accent" />
            </div>
          </div>
          <p className="text-2xl font-bold text-text-primary mb-1">
            {format(data[key])}
          </p>
          <p className="text-xs text-text-muted uppercase tracking-wider">
            {label}
          </p>
        </div>
      ))}
    </div>
  );
}
