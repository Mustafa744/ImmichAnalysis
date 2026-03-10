import { Sun, Droplets, Flame, Cloud } from "lucide-react";
import Card from "../ui/Card";

const metrics = [
  {
    key: "brightness",
    label: "Brightness",
    icon: Sun,
    color: "#fcc419",
    maxVal: 255,
  },
  {
    key: "colorfulness",
    label: "Colorfulness",
    icon: Droplets,
    color: "#cc5de8",
    maxVal: 150,
  },
  { key: "warmth", label: "Warmth", icon: Flame, color: "#ff922b", maxVal: 2 },
  {
    key: "sky_score",
    label: "Sky Score",
    icon: Cloud,
    color: "#339af0",
    maxVal: 1,
  },
];

export default function IrqMetrics({ data }) {
  if (!data) return null;

  return (
    <Card title="Image Quality Metrics" icon={Sun}>
      <div
        className="grid grid-cols-2 gap-3"
        style={{ minHeight: 340, alignContent: "flex-start" }}
      >
        {metrics.map(({ key, label, icon: Icon, color, maxVal }) => {
          const value = data[key] ?? 0;
          const pct = Math.min((value / maxVal) * 100, 100);

          return (
            <div key={key} className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Icon size={14} style={{ color }} />
                  <span className="text-xs text-text-secondary">{label}</span>
                </div>
                <span className="text-sm font-bold text-text-primary">
                  {typeof value === "number" ? value.toFixed(2) : value}
                </span>
              </div>
              <div className="h-1.5 rounded-full bg-bg-card overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700 ease-out"
                  style={{ width: `${pct}%`, backgroundColor: color }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}
