import React from 'react';
import './App.css';
import Recipe from "./recipe";
import RecipeSearch from "./search";
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";


class App extends React.Component {

  render(){
    return <Router>
      <Switch>
        <Route path="/recipe/:pub_id">
          <Recipe />
        </Route>
        <Route path="/">
          <RecipeSearch />
        </Route>
      </Switch>
    </Router>
  }
}

export default App;
