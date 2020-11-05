import React from "react";
import {Form, Icon, Search  } from "semantic-ui-react";
import {withRouter} from "react-router-dom";

class RecipeSearch extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          loading: false,
          recipes: [],
        };
        this.timer = null
        this.search_text = ""
    }

    handleResultSelect(e, data) {
        let path = `/recipe/${data.result.pub_id}`;
        this.props.history.push(path);
        e.preventDefault()
    }

    handleSearchSubmit(e, data) {
        let path = `/search?title=${this.search_text}`;
        this.props.history.push(path);
        e.preventDefault()
    }

    handleSearchChange(e, data) {
        let state = this.state
        state.loading = true
        this.setState(state)
        this.search_text = data.value

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
                let max = 10
                if(recipes.length < max)
                    max = recipes.length
                recipes = recipes.slice(0,max)
              this.setState({
                loading: false,
                recipes: recipes
              });
            })
        }, 500);


    }

    render() {
        return <>
            <Form onSubmit={this.handleSearchSubmit.bind(this)}>
                <Search
                    label="Recipes"
                    onResultSelect={this.handleResultSelect.bind(this)}
                    onSearchChange={this.handleSearchChange.bind(this)}
                    results={this.state.recipes}
                    loading={this.state.loading}
                    icon={<Icon name='search' inverted circular link />}
                    placeholder='Search Recipes...'
                />
            </Form>
            </>
    }
}

export default withRouter(RecipeSearch);