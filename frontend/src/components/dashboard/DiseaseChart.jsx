import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";



const COLORS = [
  "#2563eb",
  "#10b981",
  "#f59e0b",
  "#ef4444",
];

export default function DiseaseChart({data}) {
    if (!data || data.length === 0) {
    return (
        <div className="bg-white rounded-xl shadow-sm border p-5">
        <h3 className="text-lg font-semibold mb-4">
            Disease Distribution
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
        Disease Distribution
      </h3>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              outerRadius={90}
              label
            >
              {data.map((entry, index) => (
                <Cell
                  key={index}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>

            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}