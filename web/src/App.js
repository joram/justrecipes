import React from 'react';
import './App.css';
import Recipe from "./recipe";
import RecipeSearch from "./search";
import {BrowserRouter as Router, Route, Switch,} from "react-router-dom";
import RecipesListByCategory from "./recipes_list_by_category";
import Tags from "./tags";
import RecipesListByTag from "./recipes_list_by_tag";


class App extends React.Component {

  render(){
    return <Router>
      <Switch>
        <Route path="/recipe/:pub_id">
          <Recipe />
        </Route>
        <Route path="/category/:category">
          <RecipesListByCategory />
        </Route>
        <Route path="/tag/:tag">
          <RecipesListByTag />
        </Route>
        <Route path="/">
            <RecipeSearch />
            <Tags />
        </Route>
      </Switch>
    </Router>
  }
}

export default App;
