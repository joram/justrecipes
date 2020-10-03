import React from 'react';
import './App.css';
import Recipe from "./recipe";
import RecipeSearch from "./search";
import {BrowserRouter as Router, Link, Route, Switch,} from "react-router-dom";
import Tags from "./tags";
import RecipesListByTag from "./recipes_list_by_tag";
import {IconContext} from "react-icons";
import {GiPieSlice} from "react-icons/gi";

import {Container, Header, Segment} from "semantic-ui-react";

class App extends React.Component {

  render(){
    return <div>

    <Router>

      {/* HEADER */}
      <Segment inverted basic>
        <Header floated="left" size="huge">
          <Link to="/" style={{color:"white"}}>
            <IconContext.Provider value={{ style: { verticalAlign: 'middle' } }}>
              <GiPieSlice style={{marginTop: "-5px", marginRight: "5px"}}/>
              Recipes
            </IconContext.Provider>
          </Link>
        </Header>
        <Container>
        <RecipeSearch/>

        </Container>
      </Segment>

      {/* BODY */}
      <Container>
        <Switch>
          <Route path="/recipe/:pub_id">
            <Recipe/>
          </Route>
          <Route path="/tag/:tag">
            <RecipesListByTag />
          </Route>
          <Route path="/">
            <Tags/>
          </Route>
        </Switch>
      </Container>
    </Router>
    </div>
  }
}

export default App;
