import React from "react";
import {List, Segment} from "semantic-ui-react";
import {Link, withRouter} from "react-router-dom";


class RecipesListByCategory extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            recipes: [],
        };
        this.category = this.props.match.params.category
    }

    componentDidMount() {
        let host = "https://recipes.oram.ca"
        if(window.location.hostname==="localhost")
          host = "http://localhost:5000"
        fetch(`${host}/api/v0/recipes/search?category=${this.category}`)
        .then(res => res.json())
        .then(recipes => {
          this.setState({
            recipes: recipes,
          });
          console.log(this.state)
        })
    }

    render() {
        let recipe_links = [<List.Header>{this.category}</List.Header>]
        console.log(this.state.recipes)
        this.state.recipes.forEach(recipe => {
            recipe_links.push(<List.Item><Link to={`/recipe/${recipe.id}`}>{recipe.title}</Link></List.Item>)
        })

        return <Segment>
            <List>{recipe_links}</List>
        </Segment>
    }
}

export default withRouter(RecipesListByCategory);