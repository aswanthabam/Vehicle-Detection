import { Link } from "react-router-dom";
import styles from "./TopBar.module.css";

export const TopBar = () => {
  return (
    <div className={styles.topbar}>
      <h2>Vehicle Detection</h2>
      <div className={styles.menu}>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </div>
    </div>
  );
};
