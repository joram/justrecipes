import React from "react";
import {Icon, Search, Segment} from "semantic-ui-react";
import { withRouter } from "react-router-dom";


class RecipeSearch extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          isLoaded: true,
          recipes: [],
        };
        this.timer = null
    }

    handleResultSelect(e, data) {
        console.log(data.result.title)
        this.state.recipes.forEach(recipe => {
            if(recipe.title === data.result.title) {
                console.log(recipe)
                let path = `/recipe/${recipe.id}`;
                this.props.history.push(path);
            }

        })
    }

    handleSearchChange(e, data) {
        let state = this.state
        state.isLoaded = false
        this.setState(state)

        if(data.value.length < 3){
            return
        }

        let host = "https://recipes.oram.ca"
        if(window.location.hostname==="localhost")
          host = "http://localhost:5000"

        clearTimeout(this.timer);
        this.timer = setTimeout(() => {
            fetch(`${host}/api/v0/recipes/search?title=${data.value}`)
            .then(res => res.json())
            .then(recipes => {
              this.setState({
                isLoaded: true,
                recipes: recipes
              });
            })
        }, 500);


    }

    render() {

        return <Segment>
            <Search
              onResultSelect={this.handleResultSelect.bind(this)}
              onSearchChange={this.handleSearchChange.bind(this)}
              results={this.state.recipes}
              fluid={true}
              loading={!this.state.isLoaded}
              icon={<Icon name='search' inverted circular link />}
                placeholder='Search...'
            />

        </Segment>
    }
}

export default withRouter(RecipeSearch);