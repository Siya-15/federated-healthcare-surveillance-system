import { ArrowUpRight } from "lucide-react";

export default function StatCard({
  title,
  value,
  icon: Icon,
  color = "bg-blue-500",
}) {
  return (
    <div className="bg-white rounded-xl shadow-sm border p-5 hover:shadow-md transition">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-500">{title}</p>

          <h2 className="text-3xl font-bold mt-2">{value}</h2>
        </div>

        <div className={`${color} p-3 rounded-xl`}>
          <Icon className="text-white" size={22} />
        </div>
      </div>

      <div className="flex items-center mt-5 text-green-600 text-sm">
        <ArrowUpRight size={15} />
        <span className="ml-1">Updated today</span>
      </div>
    </div>
  );
}