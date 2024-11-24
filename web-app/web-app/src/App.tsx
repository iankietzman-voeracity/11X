import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Dashboard from "./Dashboard";
import Home from "./Home";
import Layout from "./Layout";
import "./App.css";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="dashboard" element={<Dashboard />} />
          </Route>
        </Routes>
      </Router>
    </>
  );
}

export default App;
