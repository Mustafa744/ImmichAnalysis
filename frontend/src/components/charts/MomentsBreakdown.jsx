import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import Card from "../ui/Card";
import { Sunrise } from "lucide-react";

const COLORS = ["#ff922b", "#339af0", "#fcc419", "#8b5cf6", "#51cf66"];
const LABELS = {
  golden_hour: "Golden Hour",
  night: "Night",
  morning: "Morning",
  midday: "Midday",
  afternoon: "Afternoon",
};

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const { name, value } = payload[0];
  return (
    <div className="glass-card p-3 !rounded-xl text-xs">
      <p className="text-text-primary font-medium">{name}</p>
      <p className="text-accent">{value.toLocaleString()} photos</p>
    </div>
  );
}

export default function MomentsBreakdown({ data }) {
  if (!data) return null;

  const chartData = Object.entries(data)
    .map(([key, val]) => ({ name: LABELS[key] || key, value: val.count }))
    .filter((d) => d.value > 0);

  if (!chartData.length) return null;

  return (
    <Card title="Moments" icon={Sunrise}>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={55}
              outerRadius={90}
              paddingAngle={3}
              dataKey="value"
              stroke="none"
            >
              {chartData.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              iconType="circle"
              iconSize={8}
              wrapperStyle={{ fontSize: 11 }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
