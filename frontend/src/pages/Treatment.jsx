import { useState,useEffect } from "react";
import api from "../services/api";

function Treatment() {

  const [disease, setDisease] = useState("");
  const [result, setResult] = useState(null);
  const [rankings, setRankings] =useState(null);

  const getTreatment = async () => {

    try {

      const response = await api.post(
        "/recommend-treatment",
        {
          disease
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);

    }
  };

  const getTreatmentRankings =
  async () => {

    try {

      const response =
        await api.get(
          "/disease-treatment-effectiveness"
        );

      setRankings(
        response.data
      );

    } catch(error) {

      console.error(error);

    }
};

useEffect(() => {
  getTreatmentRankings();
}, []);

  return (
    <div
      style={{
        padding: "20px"
      }}
    >

      <h1>
        Treatment Recommendation
      </h1>

      <input
        type="text"
        value={disease}
        placeholder="Enter Disease"
        onChange={(e) =>
          setDisease(e.target.value)
        }
      />

      <button
        onClick={getTreatment}
        style={{
          marginLeft: "10px"
        }}
      >
        Get Recommendation
      </button>

      {
        result && (

          <div
            style={{
              marginTop: "20px",
              border: "1px solid #ddd",
              padding: "20px",
              borderRadius: "10px"
            }}
          >

            <h2>
              Recommended Treatment
            </h2>

            <h3>
              {result.recommended_treatment}
            </h3>

            <p>
              Success Rate:
              {" "}
              {result.success_rate}%
            </p>

          </div>

        )
      }

      <h2>
        Treatment Effectiveness Rankings
      </h2>

        {
      rankings &&
      rankings[disease] && (

        <div>

          {
            rankings[disease].map(
              (item, index) => (

                <div
                  key={index}
                  style={{
                    border:
                      "1px solid #ddd",
                    padding: "10px",
                    marginBottom: "10px",
                    borderRadius: "8px"
                  }}
                >

                  <strong>
                    {index + 1}.
                    {" "}
                    {item.treatment}
                  </strong>

                  <p>
                    Effectiveness:
                    {" "}
                    {
                      item.effectiveness
                    }%
                  </p>

                </div>

              )
            )
          }

        </div>

      )
    }

    </div>
  );
}

export default Treatment;