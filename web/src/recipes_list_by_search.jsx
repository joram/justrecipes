import React from "react";
import RecipesList from "./recipes_list";
import {withRouter} from "react-router-dom";
let qs = require('qs');

class RecipesListBySearch extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            recipes: [],
        };
        console.log(this.props.location.search)
        let search = this.props.location.search;
        search = search.substring(1)
        search = qs.parse(search)
        console.log(search)

        this.title = search["title"]
        this.tag = search["tag"]
        this.ingredient = search["ingredient"]
    }

    componentDidMount() {
        let host = "https://recipes.oram.ca"
        if(window.location.hostname==="localhost")
          host = "http://localhost:5000"
        let url =`${host}/api/v0/recipes/search?title=${this.title}&tag=${this.tag}&ingredient=${this.ingredient}`
        console.log(url)
        fetch(url)
        .then(res => res.json())
        .then(recipes => {
          this.setState({
            recipes: recipes,
          });
        })
    }

    render() {
        return <RecipesList recipes={this.state.recipes} />
    }
}

export default  withRouter(RecipesListBySearch)
