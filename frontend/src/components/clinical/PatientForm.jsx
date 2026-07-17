import { useState } from "react";
import { Loader2 } from "lucide-react";

export default function PatientForm({ onAssess, loading }) {
  const [formData, setFormData] = useState({
    symptoms: "",
    age: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onAssess(formData);
  };

  return (
    <div className="bg-white rounded-xl border shadow-sm p-6">
      <h2 className="text-xl font-semibold mb-6">
        Patient Information
      </h2>

      <form onSubmit={handleSubmit} className="space-y-5">

        <div>
          <label className="block mb-2 font-medium">
            Symptoms
          </label>

          <input
            type="text"
            placeholder="fever,cough,fatigue"
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.symptoms}
            onChange={(e) =>
              setFormData({
                ...formData,
                symptoms: e.target.value,
              })
            }
          />
        </div>

        <div>
          <label className="block mb-2 font-medium">
            Age
          </label>

          <input
            type="number"
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.age}
            onChange={(e) =>
              setFormData({
                ...formData,
                age: e.target.value,
              })
            }
          />
        </div>

        <button
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-3 flex justify-center items-center gap-2 transition disabled:opacity-50"
        >
            {loading && <Loader2 className="animate-spin" size={18} />}

            {loading ? "Assessing..." : "Assess Patient"}
        </button>

      </form>
    </div>
  );
}