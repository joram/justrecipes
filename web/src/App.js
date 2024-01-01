import './App.css';
import 'semantic-ui-css/semantic.min.css'
import "pure-react-carousel/dist/react-carousel.es.css";
import RecipeSearch from "./components/recipeSearch";
import {Link, Outlet, Route, Routes} from "react-router-dom";
import React from "react";
import RecipePage from "./RecipePage";
import {Image, Menu} from "semantic-ui-react";
import HomePage from "./HomePage";

function Layout() {
    return (
        <div>
            <Menu attached="top">
                <Menu.Item>
                    <Link to="/">
                        <Image src={"/logo512.jpg"} size="tiny" /></Link>
                </Menu.Item>
                <Menu.Item>
                    <RecipeSearch/>
                </Menu.Item>
                </Menu>
            <Outlet />
        </div>
    );
}

function App() {
  return (
    <div className="App">
        <Routes>
            <Route path="/" element={<Layout />}>
                <Route index element={<HomePage />} />
                <Route path="/recipe/:recipeTitle" element={<RecipePage />} />
            </Route>
        </Routes>
    </div>
  );
}

export default App;
