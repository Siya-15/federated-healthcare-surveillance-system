import {
  Users,
  Building2,
  TriangleAlert,
  Brain,
} from "lucide-react";

import StatCard from "../components/dashboard/StatCard";
import DiseaseChart from "../components/dashboard/DiseaseChart";
import HospitalChart from "../components/dashboard/HospitalChart";
import RecentAlerts from "../components/dashboard/RecentAlerts";
import EmergingSymptoms from "../components/dashboard/EmergingSymptoms";

import { useEffect, useState } from "react";
import {getStatistics,getAlerts,} from "../services/dashboardService";

export default function Dashboard() {

  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [emergingSymptoms, setEmergingSymptoms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
  async function fetchDashboard() {
    try {
      const statistics = await getStatistics();
      const alertData = await getAlerts();
      const symptomData = await getEmergingSymptoms();

      setStats(statistics);
      setAlerts(alertData);
      setEmergingSymptoms(symptomData);
    } catch (error) {
      console.error("Failed to fetch dashboard:", error);
    } finally {
      setLoading(false);
    }
  }

  
  fetchDashboard();
  }, []);
  const diseaseData =
  stats
    ? Object.entries(stats.disease_distribution).map(
        ([name, value]) => ({
          name,
          value,
        })
      )
    : [];

    const hospitalData = stats
  ? Object.entries(stats.hospital_distribution).map(
      ([hospital, patients]) => ({
        hospital,
        patients,
      })
    )
  : [];

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-gray-500 mt-1">
          Federated Healthcare Surveillance Overview
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        <StatCard
          title="Patients"
          value={loading ? "..." : stats?.total_patients}
          icon={Users}
          color="bg-blue-500"
        />

        <StatCard
          title="Hospitals"
          value={loading? "...": Object.keys(stats?.hospital_distribution || {}).length}
          icon={Building2}
          color="bg-green-500"
        />

        <StatCard
          title="Alerts"
          value={loading ? "..." : alerts.length}
          icon={TriangleAlert}
          color="bg-red-500"
        />

        <StatCard
          title="Model Accuracy"
          value="95.3%"
          icon={Brain}
          color="bg-purple-500"
        />

      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">

        <DiseaseChart data={diseaseData} />

        <HospitalChart data={hospitalData}/>

      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <RecentAlerts alerts={alerts}/>
        <EmergingSymptoms symptoms={emergingSymptoms}/>
      </div>

    </div>
  );
}

