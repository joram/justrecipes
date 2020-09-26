import React from "react";
import {Grid, Search, Segment} from "semantic-ui-react";

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
                this.props.selectedCallback(recipe.id)
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

        return <Grid columns={3}>
            <Grid.Row>
              <Grid.Column/>
              <Grid.Column>
                    <Search
                      onResultSelect={this.handleResultSelect.bind(this)}
                      onSearchChange={this.handleSearchChange.bind(this)}
                      results={this.state.recipes}
                      fluid={true}
                      loading={!this.state.isLoaded}
                    />
              </Grid.Column>
              <Grid.Column/>
            </Grid.Row>
        </Grid>
    }
}

export default RecipeSearch;