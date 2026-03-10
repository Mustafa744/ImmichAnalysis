import React, { useState } from "react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import Card from "../ui/Card";
import {
  TrendingUp,
  BarChart as BarChartIcon,
  LineChart as LineChartIcon,
} from "lucide-react";

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card p-3 !rounded-xl text-xs">
      <p className="text-text-primary font-medium mb-1">{label}</p>
      <p className="text-accent">{payload[0].value.toLocaleString()} photos</p>
    </div>
  );
}

export default function DailyTimeline({ data }) {
  const [chartType, setChartType] = useState("line");

  if (!data?.length) return null;

  // Downsample if too many points for performance
  const displayData =
    data.length > 365
      ? data.filter((_, i) => i % Math.ceil(data.length / 365) === 0)
      : data;

  const ChartComponent = chartType === "line" ? AreaChart : BarChart;

  return (
    <Card title="Daily Timeline" icon={TrendingUp}>
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
            margin={{ top: 20, right: 30, left: 10, bottom: 20 }}
          >
            {chartType === "line" && (
              <defs>
                <linearGradient id="grad-daily" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0} />
                </linearGradient>
              </defs>
            )}
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
            {chartType === "line" ? (
              <Area
                type="monotone"
                dataKey="count"
                stroke="#8b5cf6"
                strokeWidth={2}
                fill="url(#grad-daily)"
                dot={false}
                activeDot={{
                  r: 4,
                  stroke: "#8b5cf6",
                  strokeWidth: 2,
                  fill: "#0a0a0f",
                }}
              />
            ) : (
              <Bar dataKey="count" fill="#8b5cf6" radius={[2, 2, 0, 0]} />
            )}
          </ChartComponent>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
