import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <Link to="/">Dashboard</Link> |{" "}
      <Link to="/prediction">Prediction</Link> |{" "}
      <Link to="/treatment">Treatment</Link> |{" "}
      <Link to="/outbreak">Outbreak</Link>
    </nav>
  );
}

export default Navbar;