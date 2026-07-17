import { Sparkles } from "lucide-react";



export default function EmergingSymptoms({symptoms}) {
    if (!symptoms || symptoms.length === 0) {
    return (
        <div className="bg-white rounded-xl border shadow-sm p-5">
        <h2 className="text-lg font-semibold mb-5">
            Emerging Symptoms
        </h2>

        <div className="h-40 flex items-center justify-center text-gray-500">
            No emerging symptoms detected
        </div>
        </div>
    );
    }
  return (
    <div className="bg-white rounded-xl border shadow-sm p-5">
      <h2 className="text-lg font-semibold mb-5">
        Emerging Symptoms
      </h2>

      <div
        key={index}
        className="flex items-center justify-between bg-slate-50 rounded-lg p-3"
        >
        <div className="flex items-center gap-3">

            <Sparkles
            className="text-blue-600"
            size={18}
            />

            <div>
            <p className="font-medium capitalize">
                {symptom.symptom}
            </p>

            <p className="text-sm text-gray-500">
                {symptom.alert}
            </p>
            </div>

        </div>

        <span className="text-sm font-semibold text-blue-600">
            {symptom.count}
        </span>

        </div>
    </div>
  );
}