import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from "recharts";
import { BarChart2 } from "lucide-react";

const PIE_COLORS = ["#2563eb", "#fbbf24", "#22c55e"]; // Matched, Missing, Transferable

interface SkillsDistributionChartProps {
  data: {
    matched: number;
    missing: number;
    transferable: number;
  };
}

export default function SkillsDistributionChart({
  data,
}: SkillsDistributionChartProps) {
  const chartData = [
    { name: "Matched", value: data.matched },
    { name: "Missing", value: data.missing },
    { name: "Transferable", value: data.transferable },
  ];

  return (
    <div className="bg-white p-6 rounded-2xl shadow flex flex-col items-center">
      <h3 className="font-bold mb-4 flex items-center gap-2 text-blue-700">
        <BarChart2 />
        Skills Distribution
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={chartData}
            innerRadius={40}
            outerRadius={70}
            paddingAngle={2}
            dataKey="value"
            label={({ name }) => name}
          >
            {chartData.map((entry, idx) => (
              <Cell
                key={entry.name}
                fill={PIE_COLORS[idx % PIE_COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
      <div className="flex justify-center mt-2 gap-4 text-sm">
        <span className="text-blue-600">Matched: {chartData[0].value}</span>
        <span className="text-yellow-600">Missing: {chartData[1].value}</span>
        <span className="text-green-600">
          Transferable: {chartData[2].value}
        </span>
      </div>
    </div>
  );
}
