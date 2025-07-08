import type { CandidateSummary, ScoringOverview } from "../types";

interface SummaryOverviewProps {
  candidateSummary: CandidateSummary;
  scoringOverview: ScoringOverview;
}

export default function SummaryOverview({
  candidateSummary: cs,
  scoringOverview: so,
}: SummaryOverviewProps) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow mb-8">
      <div className="grid md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-gray-200">
        {/* Candidate Info */}
        <div className="py-4 md:px-6">
          <h2 className="text-xl font-bold text-gray-800">{cs.name}</h2>
          <p className="text-sm text-gray-500 mt-1">
            {cs.email} | {cs.phone}
          </p>
          <p className="text-blue-700 font-semibold mt-2">{cs.job_title}</p>
          <p className="text-xs text-gray-400 mt-1">
            Analyzed: {new Date(cs.analysis_date).toLocaleDateString()}
          </p>
        </div>

        {/* Score */}
        <div className="py-4 md:px-6 flex flex-col items-center justify-center text-center">
          <span className="text-5xl font-bold text-blue-600">
            {so.overall_fitness_score.toFixed(1)}
          </span>
          <span className="text-sm text-gray-500">Overall Score</span>
          <span className="mt-2 px-3 py-1 rounded-full bg-blue-100 text-blue-800 font-medium text-sm">
            {so.ranking_category}
          </span>
        </div>

        {/* Recommendation */}
        <div className="py-4 md:px-6 flex flex-col items-center justify-center text-center">
          <p className="text-lg font-semibold text-green-800">
            {so.recommendation}
          </p>
          <p className="text-sm text-gray-500 mt-1">
            Confidence: {(so.confidence_level * 100).toFixed(0)}%
          </p>
        </div>
      </div>
    </div>
  );
}
