import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import Card from "../ui/Card";
import { Clock } from "lucide-react";

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
      <p className="text-text-primary font-medium mb-1">
        {hourLabels[label] ?? label}
      </p>
      <p className="text-chart-cyan">
        {payload[0].value.toLocaleString()} photos
      </p>
    </div>
  );
}

export default function HourlyDistribution({ data }) {
  if (!data?.length) return null;

  return (
    <Card title="Hourly Distribution" icon={Clock}>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 5, left: -20, bottom: 0 }}
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
            <Bar
              dataKey="count"
              radius={[4, 4, 0, 0]}
              fill="#22b8cf"
              fillOpacity={0.7}
              activeBar={{ fill: "#22b8cf", fillOpacity: 1 }}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
