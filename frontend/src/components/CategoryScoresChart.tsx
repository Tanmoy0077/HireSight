import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  Tooltip,
} from "recharts";
import { BarChart2 } from "lucide-react";

interface CategoryScoresChartProps {
  data: { category: string; score: number }[];
}

export default function CategoryScoresChart({
  data,
}: CategoryScoresChartProps) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow mb-8">
      <h3 className="font-bold mb-4 flex items-center gap-2 text-blue-700">
        <BarChart2 />
        Category Scores
      </h3>
      <ResponsiveContainer width="100%" height={220}>
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="category" />
          <Radar
            dataKey="score"
            stroke="#2563eb"
            fill="#2563eb"
            fillOpacity={0.5}
          />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
