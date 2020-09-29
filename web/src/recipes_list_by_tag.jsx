import React from "react";
import {Card, Image, List} from "semantic-ui-react";
import {Link, withRouter} from "react-router-dom";

function img_src(recipe){
    let src = "https://react.semantic-ui.com/images/avatar/large/matthew.png";
    if(recipe.images !== undefined && recipe.images.length > 0){
        src = recipe.images[0]
    }
    return src
}

let CardExampleCard = (recipe) => (
    <Link to={`/recipe/${recipe.id}`}>
        <Card>
            <Image src={img_src(recipe)} />
            <Card.Content>
              <Card.Header>{recipe.title}</Card.Header>
            </Card.Content>
        </Card>
    </Link>
)

class RecipesListByTag extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            recipes: [],
        };
        this.tag = this.props.match.params.tag
    }

    componentDidMount() {
        let host = "https://recipes.oram.ca"
        if(window.location.hostname==="localhost")
          host = "http://localhost:5000"
        fetch(`${host}/api/v0/recipes/search?tag=${this.tag}`)
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
            recipe_links.push(CardExampleCard(recipe))
        })

        return <Card.Group>
            {recipe_links}
        </Card.Group>
    }
}

export default withRouter(RecipesListByTag);