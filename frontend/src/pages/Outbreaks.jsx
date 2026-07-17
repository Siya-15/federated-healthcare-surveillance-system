import { useEffect, useState } from "react";
import api from "../services/api";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

function Outbreak() {

  const [disease, setDisease] =
    useState("Flu");

  const [trends, setTrends] =
    useState([]);

  const [alerts, setAlerts] =
    useState([]);

  useEffect(() => {
    fetchTrends();
    fetchAlerts();
  }, [disease]);

  const fetchTrends = async () => {

    try {

      const response =
        await api.get(
          `/disease-trends/${disease}`
        );

      setTrends(response.data);

    } catch (error) {

      console.error(error);

    }
  };

  const fetchAlerts = async () => {

    try {

      const response =
        await api.get("/alerts");

      setAlerts(response.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (
    <div style={{ padding: "20px" }}>

      <h1>
        Outbreak Monitoring
      </h1>

      <select
        value={disease}
        onChange={(e) =>
          setDisease(e.target.value)
        }
      >

        <option>
          Flu
        </option>

        <option>
          Covid
        </option>

        <option>
          Dengue
        </option>

        <option>
          Malaria
        </option>

      </select>

      <h2>
        Trend Data
      </h2>

      <LineChart
        width={800}
        height={350}
        data={trends}
      >

        <CartesianGrid
          strokeDasharray="3 3"
        />

        <XAxis dataKey="date" />

        <YAxis />

        <Tooltip />

        <Legend />

        <Line
          type="monotone"
          dataKey="cases"
        />

      </LineChart>

            <h2>Active Alerts</h2>

      {
        alerts.map(
          (alert, index) => (

            <div
              key={index}
              style={{
                border: "1px solid #ddd",
                borderLeft:
                  "5px solid red",
                padding: "15px",
                marginBottom: "10px"
              }}
            >

              <strong>
                {alert.disease}
              </strong>

              <p>
                {alert.alert}
              </p>

            </div>

          )
        )
      }

    </div>
  );
}

export default Outbreak;