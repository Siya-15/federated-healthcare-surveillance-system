import { useEffect, useState } from "react";
import api from "../services/api";
import StatCard from "../components/StatCard";
import {
  PieChart,
  Pie,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";

function Dashboard() {

  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [emergingSymptoms, setEmergingSymptoms] = useState([]);
  const [outbreakRisk, setOutbreakRisk] = useState([]);
  const [federatedMetrics, setFederatedMetrics] = useState(null);

  const diseaseData = stats
  ? Object.entries(stats.disease_distribution).map(
      ([name, value]) => ({
        name,
        value
      })
    )
  : [];

  const hospitalData = stats
  ? Object.entries(stats.hospital_distribution).map(
      ([name, value]) => ({
        name,
        value
      })
    )
  : [];

  useEffect(() => {
  fetchStats();
  fetchAlerts();
  fetchEmergingSymptoms();
  fetchOutbreakRisk();
  fetchFederatedMetrics();
}, []);

  const fetchStats = async () => {
    try {
      const response = await api.get("/statistics");
      setStats(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchAlerts = async () => {
    try {
        const response = await api.get("/alerts");
        setAlerts(response.data);
    } catch (error) {
        console.error(error);
    }
    };

  const fetchEmergingSymptoms = async () => {
  try {
    const response = await api.get("/emerging-symptoms");
    setEmergingSymptoms(response.data);
  } catch (error) {
    console.error(error);
  }
};

const fetchOutbreakRisk = async () => {
  try {
    const response = await api.get("/outbreak-risk");
    setOutbreakRisk(response.data);
  } catch (error) {
    console.error(error);
  }
};

const fetchFederatedMetrics = async () => {
  try {
    const response = await api.get("/federated-metrics");
    setFederatedMetrics(response.data);
  } catch (error) {
    console.error(error);
  }
};

  if (!stats) {
    return <h2>Loading...</h2>;
  }

  return (
    <div
      style={{
        padding: "20px",
        maxWidth: "1200px",
        margin: "0 auto"
      }}
    > 
      <h1>Healthcare Dashboard</h1>

      <div
        style={{
          display: "flex",
          gap: "20px",
          marginBottom: "30px"
        }}
      >

      <StatCard
        title="Total Patients"
        value={stats.total_patients}
      />
      <StatCard
        title="Active Alerts"
        value={alerts.length}
      />
      <StatCard
        title="Emerging Symptoms"
        value={emergingSymptoms.length}
      />

      <StatCard
        title="FL Accuracy"
        value={
          federatedMetrics
            ? `${federatedMetrics.global_accuracy}%`
            : "..."
        }
      />
    </div>
      <div style={{ height: "20px" }} />

      <div
          style={{
        display: "flex",
        gap: "30px",
        flexWrap: "wrap"
      }}>

      <div>

      <h2>Disease Distribution</h2>

        <PieChart width={400} height={300}>
        <Pie
            data={diseaseData}
            dataKey="value"
            nameKey="name"
            outerRadius={100}
            label
        />
        <Tooltip />
        <Legend />
        </PieChart>
        </div>

        <div>

        

    <h2>Hospital Distribution</h2>

        <BarChart
        width={500}
        height={300}
        data={hospitalData}
        >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="value" />
        </BarChart>
      </div>
      </div>

    <h2>Active Alerts</h2>

        {alerts.length === 0 ? (
        <p>No active alerts</p>
        ) : (
        alerts.map((alert, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ddd",
              borderLeft: "5px solid orange",
              padding: "15px",
              borderRadius: "8px",
              marginBottom: "10px",
              backgroundColor: "#fff8e1"
            }}
          >
            <h3 style={{ margin: 0 }}>
              ⚠ {alert.disease}
            </h3>

            <p style={{ marginTop: "8px" }}>
              {alert.alert}
            </p>
          </div>
        ))
        )}
      
      <h2>Emerging Symptoms</h2>

      {emergingSymptoms.length === 0 ? (
        <p>No emerging symptoms detected</p>
      ) : (
        emergingSymptoms.map((item, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ddd",
              padding: "12px",
              borderRadius: "8px",
              marginBottom: "10px"
            }}
          >
            ⚠ {item.symptom}

            <div>
              Count: {item.count}
            </div>
          </div>
        ))
      )}

      <h2>Outbreak Risk Analysis</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse"
        }}
      >
        <thead>
          <tr>
            <th>Symptom</th>
            <th>Current</th>
            <th>Previous</th>
            <th>Growth %</th>
            <th>Risk</th>
          </tr>
        </thead>

        <tbody>
          {outbreakRisk.slice(0, 5).map(
            (item, index) => (
              <tr key={index}>
                <td>{item.symptom}</td>
                <td>{item.current_period}</td>
                <td>{item.previous_period}</td>
                <td>{item.increase_percent}%</td>
                <td>{item.risk}</td>
              </tr>
            )
          )}
        </tbody>
      </table>

      <h2>Federated Learning Metrics</h2>

      {federatedMetrics && (
        <div
          style={{
            border: "1px solid #ddd",
            padding: "20px",
            borderRadius: "8px"
          }}
        >
          <p>
            Global Accuracy:
            {" "}
            {federatedMetrics.global_accuracy}%
          </p>

          <p>
            Hospital A:
            {" "}
            {federatedMetrics.hospital_a}%
          </p>

          <p>
            Hospital B:
            {" "}
            {federatedMetrics.hospital_b}%
          </p>

          <p>
            Hospital C:
            {" "}
            {federatedMetrics.hospital_c}%
          </p>
        </div>
      )}
          
    </div>
  );
}

export default Dashboard;