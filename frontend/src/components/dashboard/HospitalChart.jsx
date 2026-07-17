import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";



export default function HospitalChart({data}) {
    if (!data || data.length === 0) {
    return (
        <div className="bg-white rounded-xl shadow-sm border p-5">
        <h3 className="text-lg font-semibold mb-4">
            Hospital Distribution
        </h3>

        <div className="h-72 flex items-center justify-center text-gray-500">
            No data available
        </div>
        </div>
    );
    }
  return (
    <div className="bg-white rounded-xl shadow-sm border p-5">
      <h3 className="text-lg font-semibold mb-4">
        Hospital Distribution
      </h3>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <XAxis dataKey="hospital" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="patients" fill="#2563eb" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}