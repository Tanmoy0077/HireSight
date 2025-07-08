import { useState } from "react";
import { useLocation } from "react-router-dom";
import Modal from "../components/Modal";
import SummaryOverview from "../components/SummaryOverview";
import SkillsDistributionChart from "../components/SkillsDistributionChart";
import ScoreTrendChart from "../components/ScoreTrendChart";
import CategoryScoresChart from "../components/CategoryScoresChart";
import KeyInsights from "../components/KeyInsights";
import ActionButtons from "../components/ActionButtons";
import type { AnalysisData, SuggestedQuestion } from "../types";

export default function DashboardPage() {
  const location = useLocation();
  const data: AnalysisData = location.state?.analysisData;

  // Modal states
  const [openRec, setOpenRec] = useState(false);
  const [openDev, setOpenDev] = useState(false);
  const [openInterview, setOpenInterview] = useState(false);
  const [openStrengths, setOpenStrengths] = useState(false);
  const [openGaps, setOpenGaps] = useState(false);
  const [openRisks, setOpenRisks] = useState(false);

  // Group interview questions by category
  const questionsByCategory =
    data.interview_preparation.suggested_questions.reduce((acc, q) => {
      if (!acc[q.category]) {
        acc[q.category] = [];
      }
      acc[q.category].push(q);
      return acc;
    }, {} as Record<string, SuggestedQuestion[]>);

  // Radar - Per Skill Category
  const radarData = data.charts_data.radar_chart.categories.map((c, i) => ({
    category: c,
    score: data.charts_data.radar_chart.scores[i],
  }));

  // Score trend bar chart
  const scoreBar = data.charts_data.score_trend.labels.map((x, idx) => ({
    area: x,
    score: data.charts_data.score_trend.values[idx],
  }));

  // Top area
  const { candidate_summary: cs, scoring_overview: so } = data;

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-8 max-w-5xl">
        <SummaryOverview candidateSummary={cs} scoringOverview={so} />

        {/* CHARTS */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <SkillsDistributionChart
            data={data.charts_data.skills_distribution}
          />

          <ScoreTrendChart data={scoreBar} />
        </div>
        <CategoryScoresChart data={radarData} />

        {/* INSIGHTS, QUESTIONS, RECOMMENDATION - with modals */}
        <div className="grid md:grid-cols-2 gap-6 mb-4">
          <KeyInsights
            insights={data.key_insights}
            onOpenStrengths={() => setOpenStrengths(true)}
            onOpenGaps={() => setOpenGaps(true)}
            onOpenRisks={() => setOpenRisks(true)}
          />
          <ActionButtons
            onOpenInterview={() => setOpenInterview(true)}
            onOpenRec={() => setOpenRec(true)}
            onOpenDev={() => setOpenDev(true)}
          />
        </div>

        {/* Executive summary */}
        <div className="bg-white rounded-2xl p-6 shadow mb-8">
          <h3 className="font-bold mb-2 text-blue-700">Executive Summary</h3>
          <p className="text-gray-800">{data.executive_summary}</p>
        </div>

        {/* --- MODALS --- */}
        <Modal
          open={openInterview}
          onClose={() => setOpenInterview(false)}
          title="Interview Preparation"
        >
          <div className="space-y-4">
            <div className="mb-4">
              <h4 className="font-semibold text-lg mb-2">Focus Areas</h4>
              <ul className="list-disc ml-6 space-y-1 text-gray-700">
                {data.interview_preparation.focus_areas.map((a, i) => (
                  <li key={i}>{a}</li>
                ))}
              </ul>
            </div>
            <div className="mb-4">
              <h4 className="font-semibold text-lg mb-2">
                Suggested Questions
              </h4>
              <div className="space-y-3">
                {Object.entries(questionsByCategory).map(
                  ([category, questions]) => (
                    <div key={category}>
                      <h5 className="font-semibold text-md mb-1 text-blue-700">
                        {category}
                      </h5>
                      <ul className="list-decimal ml-6 space-y-2 text-gray-700">
                        {questions.map((q, i) => (
                          <li key={i}>
                            {q.question}
                            <span
                              className={`text-xs ml-2 px-2 py-0.5 rounded-full ${
                                q.difficulty === "Hard"
                                  ? "bg-red-100 text-red-800"
                                  : q.difficulty === "Medium"
                                  ? "bg-yellow-100 text-yellow-800"
                                  : "bg-gray-100 text-gray-800"
                              }`}
                            >
                              {q.difficulty}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )
                )}
              </div>
            </div>
            <div>
              <h4 className="font-semibold text-lg mb-2">
                Assessment Priorities
              </h4>
              <ul className="list-disc ml-6 space-y-1 text-gray-700">
                {data.interview_preparation.assessment_priorities.map(
                  (p, i) => (
                    <li key={i}>{p}</li>
                  )
                )}
              </ul>
            </div>
          </div>
        </Modal>

        <Modal
          open={openRec}
          onClose={() => setOpenRec(false)}
          title="Final Recommendations"
        >
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-lg mb-1">Hiring Decision</h4>
              <p className="bg-blue-50 text-blue-800 p-3 rounded-lg">
                {data.recommendations.hiring_decision}
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-lg mb-1">Salary Range</h4>
              <p className="bg-green-50 text-green-800 p-3 rounded-lg font-mono">
                {data.recommendations.salary_range}
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-lg mb-2">Onboarding Plan</h4>
              <ul className="list-decimal ml-6 space-y-2 text-gray-700">
                {data.recommendations.onboarding_plan.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ul>
            </div>
          </div>
        </Modal>

        <Modal
          open={openDev}
          onClose={() => setOpenDev(false)}
          title="Development Plan"
        >
          <div className="space-y-4">
            {data.recommendations.development_plan.map((dev, i) => (
              <div
                key={i}
                className="bg-gray-50 p-4 rounded-lg border border-gray-200"
              >
                <div className="flex justify-between items-baseline mb-1">
                  <h4 className="font-bold text-md text-blue-800">
                    {dev.area}
                  </h4>
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full ${
                      dev.priority === "High"
                        ? "bg-red-100 text-red-800"
                        : dev.priority === "Medium"
                        ? "bg-yellow-100 text-yellow-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {dev.priority}
                  </span>
                </div>
                <p className="text-gray-700 mb-2">{dev.action}</p>
                <div className="text-xs text-gray-500">
                  <p>
                    <strong>Timeline:</strong> {dev.timeline}
                  </p>
                  <p>
                    <strong>Expected Impact:</strong> {dev.expected_impact}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </Modal>

        <Modal
          open={openStrengths}
          onClose={() => setOpenStrengths(false)}
          title="Top Strengths"
        >
          <ul className="list-disc ml-6 text-green-700">
            {data.key_insights.top_strengths.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </Modal>

        <Modal
          open={openGaps}
          onClose={() => setOpenGaps(false)}
          title="Critical Gaps"
        >
          <ul className="list-disc ml-6 text-yellow-800">
            {data.key_insights.critical_gaps.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </Modal>

        <Modal
          open={openRisks}
          onClose={() => setOpenRisks(false)}
          title="Risk Factors"
        >
          <ul className="space-y-2">
            {data.key_insights.risk_factors.map((rf, i) => (
              <li key={i}>
                <span className="font-semibold">{rf.type}</span>{" "}
                <span
                  className={`text-xs px-2 py-0.5 rounded-full ${
                    rf.severity === "High"
                      ? "bg-red-100 text-red-800"
                      : rf.severity === "Medium"
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {rf.severity}
                </span>
                <p className="text-gray-600 pl-2">{rf.description}</p>
              </li>
            ))}
          </ul>
        </Modal>
      </main>
    </div>
  );
}
