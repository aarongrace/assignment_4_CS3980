import { Link, useLocation } from "react-router-dom";
import { useProfileStore } from '../contexts/profileStore';
import "./navbar.css";

const Navbar = () => {
  const role = useProfileStore((state) => state.role);

  const location = useLocation();
  // Hide navbar on the root path
  if (location.pathname === "/") {
    return null;
  }


  return (
    <header className="App-header">
      <div className="game-title">Clash of Colonies</div>
      <nav className="nav-links">
        <Link to="/" className="nav-link">Welcome</Link>
        <Link to="/profile" className="nav-link">Profile</Link>
      </nav>
    </header>
  );
};

export default Navbar;
