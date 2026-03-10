import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import Card from "../ui/Card";
import { Camera } from "lucide-react";

const COLORS = ["#8b5cf6", "#22b8cf", "#ff922b", "#51cf66"];
const LABELS = {
  landscape: "Landscape",
  portrait: "Portrait",
  square: "Square",
  macro: "Macro",
};

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="glass-card p-3 !rounded-xl text-xs">
      <p className="text-text-primary font-medium mb-1">
        {payload[0].payload.name}
      </p>
      <p className="text-accent">{payload[0].value.toLocaleString()} photos</p>
    </div>
  );
}

export default function ShotTypesChart({ data }) {
  if (!data) return null;

  const chartData = Object.entries(data)
    .filter(([key]) => key !== "macro")
    .map(([key, val]) => ({ name: LABELS[key] || key, value: val.count }))
    .filter((d) => d.value > 0);

  if (!chartData.length) return null;

  return (
    <Card title="Shot Types" icon={Camera}>
      <div style={{ width: "100%", height: 340, minHeight: 340 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 20, right: 30, left: 10, bottom: 20 }}
          >
            <XAxis
              type="number"
              tick={{ fontSize: 10 }}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              type="category"
              dataKey="name"
              tick={{ fontSize: 11, fill: "#8888a0" }}
              tickLine={false}
              axisLine={false}
              width={80}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={24}>
              {chartData.map((_, i) => (
                <Cell
                  key={i}
                  fill={COLORS[i % COLORS.length]}
                  fillOpacity={0.75}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
