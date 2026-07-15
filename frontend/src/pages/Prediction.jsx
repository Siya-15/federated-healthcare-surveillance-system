import { useState } from "react";
import api from "../services/api";

function Prediction() {

  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [result, setResult] = useState(null);
  const [treatment, setTreatment] = useState(null);

  const symptomOptions = [
  "fever",
  "cough",
  "fatigue",
  "headache",
  "chills"
];

  const predictDisease = async () => {
    try {

      const response = await api.post(
        "/predict",
        {
          symptoms: selectedSymptoms.join(",")
        }
      );

      setResult(response.data);

    } catch (error) {
      console.error(error);
    }
  };

  const toggleSymptom = (symptom) => {

  if (
    selectedSymptoms.includes(symptom)
  ) {

    setSelectedSymptoms(
      selectedSymptoms.filter(
        (s) => s !== symptom
      )
    );

  } else {

    setSelectedSymptoms([
      ...selectedSymptoms,
      symptom
    ]);

  }
  };

  const getTreatmentRecommendation =
  async (disease) => {

    try {

      const response = await api.post(
        "/recommend-treatment",
        {
          disease
        }
      );

      setTreatment(response.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (
    <div
      style={{
        padding: "20px"
      }}
    >
      <h1>Disease Prediction</h1>

      <div>

  {
    symptomOptions.map(
      (symptom) => (

        <div key={symptom}>

          <input
            type="checkbox"
            checked={
              selectedSymptoms.includes(
                symptom
              )
            }
            onChange={() =>
              toggleSymptom(symptom)
            }
          />

          {symptom}

        </div>

      )
    )
  }

</div>

      <button
        onClick={predictDisease}
        style={{
          marginLeft: "10px"
        }}
      >
        Predict
      </button>

      {result && (
        <div
          style={{
            marginTop: "20px"
          }}
        >
          <h2>Prediction Result</h2>

          <div
              style={{
                border: "1px solid #ddd",
                padding: "20px",
                borderRadius: "10px",
                maxWidth: "400px"
              }}
            >

              <h3>
                Predicted Disease
              </h3>

              <h1>
                {result.predicted_disease}
              </h1>

              <button
                onClick={() =>
                  getTreatmentRecommendation(
                    result.predicted_disease
                  )
                }
              >
                Get Treatment Recommendation
              </button>

              {
        treatment && (

          <div
            style={{
              marginTop: "20px",
              border: "1px solid #ddd",
              padding: "15px",
              borderRadius: "10px"
            }}
          >

            <h3>
              Recommended Treatment
            </h3>

            <p>
              {
                treatment.recommended_treatment
              }
            </p>

            <p>
              Success Rate:
              {" "}
              {
                treatment.success_rate
              }%
            </p>

          </div>

        )
      }

              <div
                style={{
                  backgroundColor: "#e8f5e9",
                  padding: "10px",
                  borderRadius: "8px",
                  display: "inline-block"
                }}
              >
                Confidence:
                {" "}
                {result.confidence}%
              </div>
            </div>
        </div>
      )}

    </div>
  );
}

export default Prediction;