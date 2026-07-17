import { TriangleAlert } from "lucide-react";

const severityColors = {
  High: "bg-red-500",
  Medium: "bg-yellow-500",
  Low: "bg-green-500",
};

export default function RecentAlerts({alerts}) {
    if (!alerts || alerts.length === 0) {
    return (
        <div className="bg-white rounded-xl border shadow-sm p-5">
        <h2 className="text-lg font-semibold mb-5">
            Recent Alerts
        </h2>

        <div className="flex justify-center items-center h-40 text-gray-500">
            No active alerts
        </div>
        </div>
    );
    }
  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">
      <h2 className="text-lg font-semibold mb-5">Recent Alerts</h2>

      <div className="space-y-4">
        {alerts.map((alert,index) => (
          <div
            key={index}
            className="flex items-center justify-between border-b pb-3 last:border-none"
          >
            <div className="flex items-center gap-3">
              <div className="bg-red-500 p-2 rounded-lg">
                <TriangleAlert className="text-white" size={18} />
              </div>

              <div>
                <p className="font-medium">{alert.disease}</p>
                <p className="text-sm text-gray-500">{alert.alert}</p>
              </div>
            </div>

            <span className="text-xs text-gray-400">
              {alert.cases} cases
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}