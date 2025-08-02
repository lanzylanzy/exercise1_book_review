import React from "react";
//引入 react-router-dom 路由库里的三个组件
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
//引入两个页面组件，让路由能找到这些页面。
import SearchPage from "./SearchPage/SearchPage";
import BookPage from "./Bookpage/BookPage";

function App() {
  return (
    // Router 是路由容器，包裹所有路由
    <Router>
      {/* Routes 用来包裹所有的 Route 路由规则 */}
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/book" element={<BookPage />} />
      </Routes>
    </Router>
  );
}

export default App;
