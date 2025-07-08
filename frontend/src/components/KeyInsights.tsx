import { CheckCircle } from "lucide-react";
import type { KeyInsights as KeyInsightsData } from "../types";

interface KeyInsightsProps {
  insights: KeyInsightsData;
  onOpenStrengths: () => void;
  onOpenGaps: () => void;
  onOpenRisks: () => void;
}

export default function KeyInsights({
  insights,
  onOpenStrengths,
  onOpenGaps,
  onOpenRisks,
}: KeyInsightsProps) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow">
      <h3 className="text-blue-800 font-bold mb-4 flex gap-2 items-center">
        <CheckCircle /> Key Insights
      </h3>
      <div className="space-y-3">
        <button
          onClick={onOpenStrengths}
          className="w-full text-left p-3 bg-green-50 hover:bg-green-100 rounded-lg transition"
        >
          <strong className="text-green-800">Top Strengths</strong>
          <p className="text-sm text-gray-600">
            {insights.top_strengths.length} strengths identified.
          </p>
        </button>
        <button
          onClick={onOpenGaps}
          className="w-full text-left p-3 bg-yellow-50 hover:bg-yellow-100 rounded-lg transition"
        >
          <strong className="text-yellow-800">Critical Gaps</strong>
          <p className="text-sm text-gray-600">
            {insights.critical_gaps.length} gaps to address.
          </p>
        </button>
        <button
          onClick={onOpenRisks}
          className="w-full text-left p-3 bg-red-50 hover:bg-red-100 rounded-lg transition"
        >
          <strong className="text-red-800">Risk Factors</strong>
          <p className="text-sm text-gray-600">
            {insights.risk_factors.length} potential risks.
          </p>
        </button>
      </div>
    </div>
  );
}
