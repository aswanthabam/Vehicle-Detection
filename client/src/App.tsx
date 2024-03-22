import { Route, Routes } from "react-router";
import "./App.css";
import { TopBar } from "./components/TopBar/TopBar";
import { Home } from "./pages/Home/Home";
import { About } from "./pages/About/About";
import { Footer } from "./components/Footer/Footer";
import { Contact } from "./pages/Contact/Contact";

function App() {
  return (
    <div className="app">
      <TopBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact/>} />
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
      <Footer></Footer>
    </div>
  );
}

export default App;
