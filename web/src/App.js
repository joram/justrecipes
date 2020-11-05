  import React from 'react';
import './App.css';
import Recipe from "./recipe";
import RecipeSearch from "./search";
import {BrowserRouter as Router, Link, Route, Switch,} from "react-router-dom";
import Tags from "./tags";
import {IconContext} from "react-icons";

import {Grid, Container, Header, Image, Segment} from "semantic-ui-react";
import RecipesListBySearch from "./recipes_list_by_search";
  import SearchTags from "./search_tags";
  import Ingredients from "./ingredients";

class App extends React.Component {

  render(){
    return <div>

    <Router>

      {/* HEADER */}
      <Segment inverted basic>
        <Grid>
          <Grid.Row columns={3}>
            <Grid.Column>
              <Header floated="left" size="huge">
                <Link to="/" style={{color:"white"}}>
                  <IconContext.Provider value={{ style: { verticalAlign: 'middle' } }}>
                    <Image src="cooking.png" size="mini" style={{float:"left", paddingRight: "5px"}}/>
                    Recipes
                  </IconContext.Provider>
                </Link>
              </Header>
            </Grid.Column>
            <Grid.Column>
              <RecipeSearch history={this.props.history}/>
            </Grid.Column>
            <Grid.Column>
              <SearchTags />
              <Link to="/tags/list">Tags</Link>
              <Link to="/ingredients/list">Ingredients</Link>
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Segment>

      {/* BODY */}
      <Container>
        <Switch>
          <Route path="/recipe/:pub_id">
            <Recipe/>
          </Route>
          <Route path="/search">
            <RecipesListBySearch />
          </Route>
          <Route path="/tags/list">
            <Tags/>
          </Route>
          <Route path="/ingredients/list">
            <Ingredients/>
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
