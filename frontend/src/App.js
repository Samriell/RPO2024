// App.js
import React from "react";
import NavigationBar from "./components/NavigationBar";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <NavigationBar />
        <div className="container-fluid">
          <Routes>
            <Route path="/home" element={<Home />} /> {/* Обратите внимание, что путь начинается с / */}
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
