import './App.css';
import 'semantic-ui-css/semantic.min.css'
import SearchExampleStandard from "./search";
import {Link, Outlet, Route, Routes} from "react-router-dom";
import React from "react";
import RecipePage from "./RecipePage";

function SearchPage() {
    return <SearchExampleStandard />
}

function Layout() {
    return (
        <div>
            {/* A "layout route" is a good place to put markup you want to
          share across all the pages on your site, like navigation. */}
            <nav>
                <ul>
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/search">search</Link>
                    </li>
                </ul>
            </nav>

            <hr />

            {/* An <Outlet> renders whatever child route is currently active,
          so you can think about this <Outlet> as a placeholder for
          the child routes we defined above. */}
            <Outlet />
        </div>
    );
}

function App() {
  return (
    <div className="App">
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route index element={<SearchPage />} />
                <Route path="/recipe/:recipeTitle" element={<RecipePage />} />
            </Route>
        </Routes>
    </div>
  );
}

export default App;
