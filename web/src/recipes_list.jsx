import React from "react";
import {Card, Image, Segment} from "semantic-ui-react";
import {Link, withRouter} from "react-router-dom";

function img_src(recipe){
    if(recipe.images !== undefined && recipe.images.x512 !== undefined && recipe.images.x512.length > 0)
        return recipe.images.x512[0]
    return "/placeholder.png"
}

class RecipeCard extends React.Component {
    render() {
        return <Card key={this.props.recipe.id} as={Link} to={`/recipe/${this.props.recipe.pub_id}`}>
            <Image src={img_src(this.props.recipe)}/>
            <Card.Content>
                <Card.Header>{this.props.recipe.title}</Card.Header>
            </Card.Content>
        </Card>
    }
}

class RecipesList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            num_columns: this.numCols(),
        };
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
    }

    render() {
        let recipe_links = []
        this.props.recipes.forEach(recipe => {
            recipe_links.push(<RecipeCard key={recipe.pub_id} recipe={recipe} />)
        })

        return <Segment basic>
            <Card.Group itemsPerRow={this.state.num_columns}>
                {recipe_links}
            </Card.Group>
        </Segment>
    }
}

export default withRouter(RecipesList);