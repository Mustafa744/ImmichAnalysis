import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import Card from "../ui/Card";
import { Palette } from "lucide-react";

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card p-3 !rounded-xl text-xs">
      <p className="text-text-primary font-medium mb-2">Bin {label}</p>
      {payload.map((entry) => (
        <div key={entry.name} className="flex items-center gap-2">
          <span
            className="w-2 h-2 rounded-full"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-text-secondary">{entry.name}:</span>
          <span className="text-text-primary font-medium">
            {entry.value?.toFixed(2)}
          </span>
        </div>
      ))}
    </div>
  );
}

export default function ColorHistogram({ data }) {
  if (!data || !data.r_hist) return null;

  const chartData = data.r_hist.map((_, i) => ({
    bin: i,
    Red: data.r_hist[i],
    Green: data.g_hist[i],
    Blue: data.b_hist[i],
  }));

  return (
    <Card title="Color Histogram" icon={Palette}>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 5, right: 5, left: -20, bottom: 0 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255,255,255,0.04)"
            />
            <XAxis
              dataKey="bin"
              tick={{ fontSize: 10 }}
              tickLine={false}
              axisLine={false}
            />
            <YAxis tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line
              type="monotone"
              dataKey="Red"
              stroke="#ff6b6b"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="Green"
              stroke="#51cf66"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="Blue"
              stroke="#339af0"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
