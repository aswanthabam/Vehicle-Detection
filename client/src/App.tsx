import { Route, Router, Routes } from "react-router";
import "./App.css";
import { TopBar } from "./components/TopBar/TopBar";
import { Home } from "./pages/Home/Home";

function App() {
  return (
    <div className="app">
      <TopBar />
      <Routes>
        <Route path="/" element={<Home />} />
        {/* <Route path="/about" element={<div>About</div>} />
        <Route path="/contact" element={<div>Contact</div>} /> */}
        <Route
          path="*"
          element={
            <div
              style={{
                width: "99vw",
                height: "100vh",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <h1 style={{
                fontWeight: "bold",
              }}>Not Found 404</h1>
            </div>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
