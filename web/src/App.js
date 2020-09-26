import React from 'react';
import './App.css';
import Recipe from "./recipe";
import RecipeSearch from "./search";



class App extends React.Component {

  constructor(props) {
      super(props);
      this.state = {
        recipe: null,
      };
  }


  selectedCallback(id) {
    let state = this.state
    state.recipe = id
    this.setState(state)
  }

  render(){
    let page = <RecipeSearch selectedCallback={this.selectedCallback.bind(this)}/>
    if(this.state.recipe !== null) {
      page = <Recipe pub_id={this.state.recipe} />
    }
    return <div className="App">
      {page}
    </div>
  }
}

export default App;
