import { ImageIcon, Globe, Calendar, TrendingUp } from "lucide-react";
import Card from "../ui/Card";

const statConfig = [
  {
    key: "total_photos",
    label: "Total Memories",
    icon: ImageIcon,
    format: (v) => v?.toLocaleString() ?? "—",
  },
  {
    key: "date_range",
    label: "Time Span",
    icon: Calendar,
    isDateRange: true,
  },
  {
    key: "top_shooting_hour",
    label: "Peak Activity",
    icon: TrendingUp,
    format: (v) => (v !== null ? `${v}:00` : "—"),
  },
  {
    key: "top_location",
    label: "Top Location",
    icon: Globe,
    format: (v) => v ?? "—",
  },
];

export default function StatsCards({ data }) {
  if (!data) return null;

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 stagger-children">
      {statConfig.map(({ key, label, icon: Icon, format, isDateRange }) => (
        <div
          key={key}
          className="glass-card glass-card-hover p-7 flex flex-col m-1 shadow-sm h-full"
        >
          <div className="flex items-center gap-4">
            <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-accent/10 border border-accent/20 shrink-0">
              <Icon size={18} className="text-accent" />
            </div>

            <div className="flex-1 min-w-0">
              {isDateRange ? (
                <div className="flex items-center gap-2.5">
                  <div className="flex flex-col">
                    <span className="text-xl font-bold text-text-primary leading-none">
                      {data[key]?.from ? data[key].from.split("-")[0] : "—"}
                    </span>
                    <span className="text-[9px] text-text-muted font-medium uppercase tracking-tighter mt-1">
                      {data[key]?.from
                        ? new Date(data[key].from).toLocaleDateString("en-US", {
                            month: "short",
                            day: "numeric",
                          })
                        : ""}
                    </span>
                  </div>

                  <div className="text-text-muted/20 font-light text-xl">/</div>

                  <div className="flex flex-col">
                    <span className="text-xl font-bold text-text-primary leading-none">
                      {data[key]?.to ? data[key].to.split("-")[0] : "—"}
                    </span>
                    <span className="text-[9px] text-text-muted font-medium uppercase tracking-tighter mt-1">
                      {data[key]?.to
                        ? new Date(data[key].to).toLocaleDateString("en-US", {
                            month: "short",
                            day: "numeric",
                          })
                        : ""}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="text-xl font-bold text-text-primary tracking-tight truncate leading-none">
                  {format(data[key])}
                </p>
              )}
            </div>
          </div>

          <p className="text-[10px] text-text-muted uppercase tracking-[0.2em] font-bold mt-6 ml-[56px]">
            {label}
          </p>
        </div>
      ))}
    </div>
  );
}
