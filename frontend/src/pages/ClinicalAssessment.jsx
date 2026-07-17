import { useState } from "react";
import api from "../services/api";

import PatientForm from "../components/clinical/PatientForm";
import AssessmentResult from "../components/clinical/AssessmentResult";

export default function ClinicalAssessment() {

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAssessment = async (data) => {

    try {

      setLoading(true);

      const response = await api.post(
        "/clinical-assessment",
        {
          symptoms: data.symptoms,
          age: Number(data.age),
        }
      );

      setResult(response.data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);

    }

  };

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold">
          Clinical Assessment
        </h1>

        <p className="text-gray-500">
          AI-powered patient assessment
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        <PatientForm
          onAssess={handleAssessment}
          loading={loading}
        />

        <AssessmentResult
          result={result}
        />

      </div>

    </div>
  );
}