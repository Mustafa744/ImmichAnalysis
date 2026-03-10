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
import { Clock } from "lucide-react";

const COLORS = [
  "#22b8cf", // cyan
  "#8b5cf6", // purple
  "#ff922b", // orange
  "#51cf66", // green
  "#fcc419", // yellow
  "#ff6b6b", // red
  "#339af0", // blue
  "#cc5de8", // violet
  "#20c997", // teal
];

const hourLabels = [
  "12am",
  "1am",
  "2am",
  "3am",
  "4am",
  "5am",
  "6am",
  "7am",
  "8am",
  "9am",
  "10am",
  "11am",
  "12pm",
  "1pm",
  "2pm",
  "3pm",
  "4pm",
  "5pm",
  "6pm",
  "7pm",
  "8pm",
  "9pm",
  "10pm",
  "11pm",
];

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card p-3 !rounded-xl text-xs">
      <p className="text-text-primary font-medium mb-2">
        {hourLabels[label] ?? label}
      </p>
      {payload.map((entry, index) => (
        <div key={index} className="flex items-center gap-2 mb-1">
          <span
            className="w-2 h-2 rounded-full"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-text-secondary">{entry.name}:</span>
          <span className="text-text-primary font-medium">
            {entry.value.toLocaleString()} photos
          </span>
        </div>
      ))}
    </div>
  );
}

export default function MultiHourlyDistribution({ data, countries }) {
  if (!data?.length || !countries?.length) return null;

  return (
    <Card
      title="Photo Frequency Comparison"
      icon={Clock}
      className="mt-6 mx-2 md:mx-6 mb-8"
    >
      <div style={{ width: "100%", height: 400, minHeight: 400 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={data}
            margin={{ top: 20, right: 30, left: 10, bottom: 20 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255,255,255,0.04)"
            />
            <XAxis
              dataKey="hour"
              tick={{ fontSize: 10 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(h) => hourLabels[h] ?? h}
              interval={2}
            />
            <YAxis tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Legend wrapperStyle={{ paddingTop: "20px" }} />
            {countries.map((country, idx) => (
              <Line
                key={country}
                type="monotone"
                dataKey={country}
                name={country}
                stroke={COLORS[idx % COLORS.length]}
                strokeWidth={2}
                dot={false}
                activeDot={{
                  r: 4,
                  stroke: COLORS[idx % COLORS.length],
                  strokeWidth: 2,
                  fill: "#0a0a0f",
                }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
