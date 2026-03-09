import React, { useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import Card from "../ui/Card";
import {
  TrendingUp,
  BarChart as BarChartIcon,
  LineChart as LineChartIcon,
} from "lucide-react";

const COLORS = [
  "#8b5cf6", // purple
  "#22b8cf", // cyan
  "#ff922b", // orange
  "#51cf66", // green
  "#fcc419", // yellow
  "#ff6b6b", // red
  "#339af0", // blue
  "#cc5de8", // violet
  "#20c997", // teal
];

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card p-3 !rounded-xl text-xs">
      <p className="text-text-primary font-medium mb-2">{label}</p>
      {payload.map((entry, index) => (
        <div key={index} className="flex items-center gap-2 mb-1">
          <span
            className="w-2 h-2 rounded-full"
            style={{ backgroundColor: entry.color || entry.fill }}
          />
          <span className="text-text-secondary">{entry.name}:</span>
          <span className="text-text-primary font-medium">
            {entry.value ? entry.value.toLocaleString() : 0} photos
          </span>
        </div>
      ))}
    </div>
  );
}

export default function MultiDailyTimeline({ data, countries }) {
  const [chartType, setChartType] = useState("line");

  if (!data?.length || !countries?.length) return null;

  const displayData =
    data.length > 365
      ? data.filter((_, i) => i % Math.ceil(data.length / 365) === 0)
      : data;

  const ChartComponent = chartType === "line" ? LineChart : BarChart;

  return (
    <Card title="Timeline Comparison" icon={TrendingUp}>
      <div className="flex justify-end mb-4 pr-6">
        <div className="flex items-center bg-bg-card border border-border rounded-lg p-1">
          <button
            onClick={() => setChartType("line")}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
              chartType === "line"
                ? "bg-accent/20 text-accent"
                : "text-text-muted hover:text-text-primary"
            }`}
          >
            <LineChartIcon size={14} /> Line
          </button>
          <button
            onClick={() => setChartType("bar")}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-all ${
              chartType === "bar"
                ? "bg-accent/20 text-accent"
                : "text-text-muted hover:text-text-primary"
            }`}
          >
            <BarChartIcon size={14} /> Bar
          </button>
        </div>
      </div>
      <div style={{ width: "100%", height: 340, minHeight: 340 }}>
        <ResponsiveContainer width="100%" height="100%">
          <ChartComponent
            data={displayData}
            margin={{ top: 5, right: 30, left: -20, bottom: 0 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255,255,255,0.04)"
            />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 10 }}
              tickLine={false}
              axisLine={false}
              interval="preserveStartEnd"
            />
            <YAxis tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ paddingTop: "20px" }} />
            {countries.map((country, idx) => {
              if (chartType === "line") {
                return (
                  <Line
                    key={country}
                    type="monotone"
                    dataKey={country}
                    name={country}
                    stroke={COLORS[idx % COLORS.length]}
                    strokeWidth={2}
                    dot={false}
                    connectNulls={false}
                    activeDot={{
                      r: 4,
                      stroke: COLORS[idx % COLORS.length],
                      strokeWidth: 2,
                      fill: "#0a0a0f",
                    }}
                  />
                );
              }
              return (
                <Bar
                  key={country}
                  dataKey={country}
                  name={country}
                  fill={COLORS[idx % COLORS.length]}
                  radius={[2, 2, 0, 0]}
                />
              );
            })}
          </ChartComponent>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
