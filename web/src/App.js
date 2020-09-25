import React from 'react';
import './App.css';
import {List, Rail, Grid, Segment} from 'semantic-ui-react'


class Ingredient extends React.Component {
  render(){
    return <List.Item>
      <List.Content>
        <List.Header>{this.props.ingredient.name}</List.Header>
        <List.Description>
          {this.props.ingredient.spoken}
        </List.Description>
      </List.Content>
    </List.Item>
  }
}


class Ingredients extends React.Component {
  render(){
    let ingredients = []
    console.log(this.props.ingredients)
    this.props.ingredients.forEach(ingredient => {
      ingredients.push(<Ingredient ingredient={ingredient} />)
    })

    return (<List horizontal={false}>
          {ingredients}
      </List>
    )
  }
}


class Instructions extends React.Component {
  render() {
    let steps = []
    this.props.instructions.forEach(step => {
      steps.push(<List.Item>{step}</List.Item>)
    })
    return <List>
      {steps}
    </List>
  }
}


class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      recipe: null
    };
  }

  componentDidMount() {
    let host = "https://recipes.oram.ca"
    if(window.location.hostname==="localhost")
      host = "http://localhost:5000"

    fetch(`${host}/api/v0/recipe/recipe_da2ddeea30c98822dbfa6182dc4f465a100e919d438691913bc8a1c7`)
    .then(res => res.json())
    .then(recipe => {
      this.setState({
        isLoaded: true,
        recipe: recipe
      });
    })
  }

  render(){
    let ingredients = [];
    let instructions = [];
    if (this.state.recipe !== null){
      ingredients = this.state.recipe.ingredients
      instructions = this.state.recipe.instructions
    }
    console.log(this.state.recipe)

    return <div className="App">

      <Grid centered columns={2}>
          <Grid.Column>
              <Rail position='left'>
                <Segment>
                  <Ingredients ingredients={ingredients} />
                </Segment>
              </Rail>
              <Segment>
                 <Instructions instructions={instructions} />
              </Segment>
          </Grid.Column>
      </Grid>
    </div>
  }
}

export default App;
