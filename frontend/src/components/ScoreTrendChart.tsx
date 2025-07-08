import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";
import { BarChart2 } from "lucide-react";

interface ScoreTrendChartProps {
  data: { area: string; score: number }[];
}

export default function ScoreTrendChart({ data }: ScoreTrendChartProps) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow flex flex-col items-center">
      <h3 className="font-bold mb-4 flex items-center gap-2 text-blue-700">
        <BarChart2 />
        Score Trend
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data}>
          <XAxis dataKey="area" stroke="#888" fontSize={12} />
          <YAxis domain={[0, 10]} />
          <Bar dataKey="score" fill="#2563eb" radius={6} />
          <Tooltip />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
