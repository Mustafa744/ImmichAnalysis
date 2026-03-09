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
import { MapPin } from "lucide-react";

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="glass-card p-3 !rounded-xl text-xs">
      <p className="text-text-primary font-medium mb-1">{d.city}</p>
      <p className="text-text-muted">{d.country}</p>
      <p className="text-accent mt-1">{d.count.toLocaleString()} photos</p>
    </div>
  );
}

export default function TopLocations({ data }) {
  if (!data?.length) return null;

  const chartData = data.slice(0, 8).map((d) => ({
    ...d,
    label: d.city?.length > 12 ? d.city.slice(0, 12) + "…" : d.city,
  }));

  return (
    <Card title="Top Locations" icon={MapPin}>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 5, right: 5, left: -10, bottom: 0 }}
          >
            <XAxis
              dataKey="label"
              tick={{ fontSize: 10 }}
              tickLine={false}
              axisLine={false}
              interval={0}
              angle={-20}
              textAnchor="end"
              height={50}
            />
            <YAxis tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="count" radius={[4, 4, 0, 0]} barSize={28}>
              {chartData.map((_, i) => (
                <Cell
                  key={i}
                  fill={`hsl(${260 + i * 15}, 70%, ${55 + i * 3}%)`}
                  fillOpacity={0.8}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
