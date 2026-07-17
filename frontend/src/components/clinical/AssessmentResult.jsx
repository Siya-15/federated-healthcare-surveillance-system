import ResultCard from "./ResultCard";
import { Stethoscope } from "lucide-react";

export default function AssessmentResult({ result }) {

  if (!result) {
  return (
    <div className="bg-white rounded-xl border shadow-sm p-6 flex flex-col items-center justify-center text-center">

      <Stethoscope
        size={48}
        className="text-blue-500 mb-4"
      />

      <h2 className="text-xl font-semibold">
        Run a Clinical Assessment
      </h2>

      <p className="text-gray-500 mt-2">
        Enter symptoms and age to generate
        AI-powered predictions.
      </p>

    </div>
  );
}

  return (
    <div className="bg-white rounded-xl border shadow-sm p-6">

      <h2 className="text-xl font-semibold mb-6">
        Assessment Results
      </h2>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 gap-4">

        <ResultCard
          title="Disease"
          value={result.disease_prediction.predicted_disease}
        />

        <ResultCard
          title="Treatment"
          value={result.treatment_recommendation.recommended_treatment}
          color="text-green-600"
        />

        <ResultCard
          title="Recovery"
          value={`${result.recovery_prediction.expected_recovery_days} days`}
          color="text-purple-600"
        />
        <ResultCard
            title="Confidence"
            value={`${result.disease_prediction.confidence}%`}
            color="text-blue-600"
        />

      </div>

      {/* Confidence */}
      <div className="mt-6">
        <p className="text-gray-500 font-medium">Confidence</p>

        <div className="mt-2 h-3 rounded-full bg-gray-200">
          <div
            className="h-3 rounded-full bg-blue-600"
            style={{
              width: `${result.disease_prediction.confidence}%`,
            }}
          />
        </div>

        <p className="mt-2 text-sm">
          {result.disease_prediction.confidence}%
        </p>
      </div>

      {/* Risk Badge */}
      <div className="mt-6">
        <p className="text-gray-500 font-medium">
          Complication Risk
        </p>

        <span
          className={`inline-block mt-2 px-3 py-1 rounded-full text-sm font-semibold ${
            result.complication_prediction.risk_level === "Low"
              ? "bg-green-100 text-green-700"
              : result.complication_prediction.risk_level === "Moderate"
              ? "bg-yellow-100 text-yellow-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {result.complication_prediction.risk_level}
        </span>
      </div>

      {/* Clinical Summary */}
      <div className="mt-6 bg-blue-50 border border-blue-200 rounded-xl p-4">
        <h3 className="font-semibold mb-2">
          Clinical Summary
        </h3>

        <p className="leading-7 text-gray-700">
          {result.clinical_summary}
        </p>
      </div>

    </div>
  );
}