import { Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "../pages/Dashboard";
import ClinicalAssessment from "../pages/ClinicalAssessment";
import Surveillance from "../pages/Surveillance";
import Outbreaks from "../pages/Outbreaks";
import Patients from "../pages/Patients";
import Analytics from "../pages/Analytics";
import FederatedLearning from "../pages/FederatedLearning";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/clinical-assessment" element={<ClinicalAssessment />} />
      <Route path="/surveillance" element={<Surveillance />} />
      <Route path="/outbreaks" element={<Outbreaks />} />
      <Route path="/patients" element={<Patients />} />
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/federated-learning" element={<FederatedLearning />}/>
    </Routes>
  );
}