import React from 'react';
import './App.css';
import {Image, List, Menu, Segment, Sidebar} from 'semantic-ui-react'
import {withRouter} from "react-router-dom";


class Ingredient extends React.Component {
  render(){
    return <Menu.Item>{this.props.ingredient}</Menu.Item>
  }
}

class DetailedIngredient extends React.Component {
  render(){
    return <Menu.Item>
      <span className="ingredient_quantity">{Math.round(this.props.ingredient.quantity * 100) / 100} </span>
      <span className="ingredient_unit">{this.props.ingredient.unit} </span>
      <span className="ingredient_name">{this.props.ingredient.name}</span>
    </Menu.Item>
  }
}


class Ingredients extends React.Component {
  render(){
    let ingredients = []
    this.props.ingredients.forEach(ingredient => {
      ingredients.push(<Ingredient ingredient={ingredient} key={`ingredient_${ingredients.length}`}/>)
    })

    return (<Sidebar
      as={Menu}
      icon='labeled'
      vertical
      visible={true}
      animation="slide out"
      width={"thin"}
    >
      <br/>
      <Menu.Header as={"h3"}>Ingredients</Menu.Header>
      {ingredients}
    </Sidebar>)
  }
}

class DetailedIngredients extends React.Component {
  render(){
    let ingredients = []
    this.props.ingredients.forEach(ingredient => {
      ingredients.push(<DetailedIngredient ingredient={ingredient} key={`ingredient_${ingredients.length}`}/>)
    })

    return (<Sidebar
      as={Menu}
      icon='labeled'
      vertical
      visible={true}
      animation="slide out"
      width={"thin"}
    >
      <br/>
      <Menu.Header as={"h3"}>Ingredients</Menu.Header>
      {ingredients}
    </Sidebar>)
  }
}


class Instructions extends React.Component {
  render() {
    let i = 1;
    let steps = []
    this.props.instructions.forEach(step => {
      steps.push(<List.Item key={"instruction_"+i} >

        <List.Content floated={"left"}>
          {i}) {step}
        </List.Content>
      </List.Item>)
      i += 1;
    })
    return <List divided relaxed>
      <List.Header><h3>{this.props.title}</h3></List.Header>
      {steps}
      <List.Item>
        <List.Content>
          original recipe (<a href={this.props.url}>here</a>)
        </List.Content>
      </List.Item>
    </List>
  }
}


class Recipe extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      recipe: null
    };
  }

  componentDidMount() {
    this.loadRecipe()
  }

  loadRecipe(){
    let host = "https://recipes.oram.ca"
    if(window.location.hostname==="localhost")
      host = "http://localhost:5000"
    let pub_id = this.props.match.params.pub_id;
    fetch(`${host}/api/v0/recipe/${pub_id}`)
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
    let detailed_ingredients = [];
    let instructions = [];
    let title = "";
    let src = ""
    let url = ""
    if (this.state.recipe !== null){
      ingredients = this.state.recipe.ingredients
      detailed_ingredients = this.state.recipe.ingredient_details
      instructions = this.state.recipe.instructions
      title = this.state.recipe.title
      url = this.state.recipe.url
      if(this.state.recipe.images !== undefined){
        src = this.state.recipe.images[0]
      }
    }

    return <>
      <Sidebar.Pushable style={{overflowY:"scroll"}}>
        {/*<Ingredients ingredients={ingredients} />*/}
        <DetailedIngredients ingredients={detailed_ingredients} />
        <Sidebar.Pusher>
          <Segment basic>
            <Image src={src} size="large"/>
            <Instructions instructions={instructions} title={title} url={url} />
          </Segment>
        </Sidebar.Pusher>
      </Sidebar.Pushable>
    </>
  }
}

export default withRouter(Recipe);
