import React from "react";
import {Card, Image, List, Segment} from "semantic-ui-react";
import {Link, withRouter} from "react-router-dom";

function img_src(recipe){
    if(recipe.images !== undefined && recipe.images.x512 !== undefined && recipe.images.x512.length > 0)
        return recipe.images.x512[0]
    return "/placeholder.png"
}

class RecipeCard extends React.Component {
    render() {
        return <Card key={this.props.recipe.id} as={Link} to={`/recipe/${this.props.recipe.id}`}>
            <Image src={img_src(this.props.recipe)}/>
            <Card.Content>
                <Card.Header>{this.props.recipe.title}</Card.Header>
            </Card.Content>
        </Card>
    }
}

class RecipesListByTag extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            recipes: [],
            num_columns: this.numCols(),
        };
        this.tag = this.props.match.params.tag
    }

    numCols() {
        let num_columns = Math.ceil(window.innerWidth/400)
        if(num_columns > 5)
            return 5
        return num_columns
    }

    updateDimensions = () => {
        let state = this.state
        state.num_columns = this.numCols()
        this.setState(state);
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateDimensions.bind(this));
    }

    componentDidMount() {
        window.addEventListener('resize', this.updateDimensions.bind(this));
        let host = "https://recipes.oram.ca"
        if(window.location.hostname==="localhost")
          host = "http://localhost:5000"
        fetch(`${host}/api/v0/recipes/search?tag=${this.tag}`)
        .then(res => res.json())
        .then(recipes => {
          this.setState({
            recipes: recipes,
          });
        })
    }

    render() {
        let recipe_links = [<List.Header>{this.category}</List.Header>]
        this.state.recipes.forEach(recipe => {
            recipe_links.push(<RecipeCard recipe={recipe} />)
        })



        return <Segment>
            <Card.Group itemsPerRow={this.state.num_columns}>
                {recipe_links}
            </Card.Group>
        </Segment>
    }
}

export default withRouter(RecipesListByTag);