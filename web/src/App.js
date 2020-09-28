import React from 'react';
import './App.css';
import Recipe from "./recipe";
import RecipeSearch from "./search";
import {BrowserRouter as Router, Route, Switch,} from "react-router-dom";
import Categories from "./categories";
import Category from "./category";


class App extends React.Component {

  render(){
    return <Router>
      <Switch>
        <Route path="/recipe/:pub_id">
          <Recipe />
        </Route>
        <Route path="/category/:category">
          <Category />
        </Route>
        <Route path="/">
            <RecipeSearch />
            <Categories />
        </Route>
      </Switch>
    </Router>
  }
}

export default App;
