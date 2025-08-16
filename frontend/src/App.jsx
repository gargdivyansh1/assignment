import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Homefeed from "./components/HomeFeed";
import Explanations from "./components/Explanations";

function App() {
  const userId = 1;

  return (
    <Router>
      <div className="bg-gray-50 min-h-screen">
        <nav className="bg-white shadow p-4 flex flex-col md:flex-row justify-between items-start md:items-center space-y-2 md:space-y-0">
          <div className="flex items-center space-x-2">
            <h1 className="font-bold text-xl">FlatZ Feed</h1>
            <span className="text-sm text-gray-500">
              (Currently showing for 1 user; dynamic user can be added via login)
            </span>
          </div>
          <div className="space-x-4">
            <Link to="/" className="text-blue-500 hover:underline">Homefeed</Link>
            <Link to="/explanations" className="text-blue-500 hover:underline">Explanations</Link>
          </div>
        </nav>


        <Routes>
          <Route path="/" element={<Homefeed userId={userId} />} />
          <Route path="/explanations" element={<Explanations userId={userId} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
