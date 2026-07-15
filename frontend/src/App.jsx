import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Prediction from "./pages/Prediction";
import Treatment from "./pages/Treatment";
import Outbreak from "./pages/Outbreak";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/prediction" element={<Prediction />} />
        <Route path="/treatment" element={<Treatment />} />
        <Route path="/outbreak" element={<Outbreak />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;