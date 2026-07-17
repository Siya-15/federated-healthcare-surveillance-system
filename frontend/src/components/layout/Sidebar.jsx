import {
  LayoutDashboard,
  Stethoscope,
  Activity,
  MapPinned,
  Network,
  Users,
  BarChart3,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const menuItems = [
  { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard" },
  { icon: Stethoscope, label: "Clinical Assessment", path: "/clinical-assessment" },
  { icon: Activity, label: "Disease Surveillance", path: "/surveillance" },
  { icon: MapPinned, label: "Regional Outbreaks", path: "/outbreaks" },
  { icon: Users, label: "Patients", path: "/patients" },
  { icon: BarChart3, label: "Analytics", path: "/analytics" },
  { icon: Network, label: "Federated Learning", path: "/federated-learning" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-xl font-bold">
          Health<span className="text-blue-400">AI</span>
        </h1>
        <p className="text-sm text-slate-400">
          Federated Surveillance
        </p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map(({ icon: Icon, label,path }) => (
          <NavLink
            key={label}
            to={path}
            className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 transition ${
                isActive
                    ? "bg-blue-600 text-white"
                    : "hover:bg-slate-800 text-slate-300"
                }`
            }
            >
            <Icon size={20} />
            {label}
            </NavLink>
        ))}
      </nav>
    </aside>
  );
}