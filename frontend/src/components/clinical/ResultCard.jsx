
export default function ResultCard({
  title,
  value,
  icon: Icon,
  color = "text-slate-900",
}) {
  return (
    <div className="bg-slate-50 border rounded-xl p-4">
      <div className="flex justify-between items-center">
        <p className="text-gray-500">{title}</p>
        {Icon && <Icon size={20} className="text-slate-500" />}
      </div>

      <h3 className={`text-2xl font-bold mt-3 ${color}`}>
        {value}
      </h3>
    </div>
  );
}