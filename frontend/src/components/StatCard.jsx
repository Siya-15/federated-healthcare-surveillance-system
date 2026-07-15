function StatCard({ title, value }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: "20px",
        borderRadius: "10px",
        width: "200px",
        boxShadow: "0px 2px 8px rgba(0,0,0,0.1)"
      }}
    >
      <h3>{title}</h3>
      <h1>{value}</h1>
    </div>
  );
}

export default StatCard;