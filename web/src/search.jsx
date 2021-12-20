import React from "react";
import {Form, Icon, Search  } from "semantic-ui-react";
import {withRouter} from "react-router-dom";
import call_api from "./utils";


class RecipeSearch extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
          loading: false,
          recipes: [],
          open:false,
        };
        this.timer = null
        this.search_text = ""
    }

    handleResultSelect(e, data) {
        let path = `/recipe/${data.result.pub_id}`;
        this.props.history.push(path);
        e.preventDefault()
        let state = this.state;
        state.open = false;
        this.setState(state);
    }

    handleSearchSubmit(e, data) {
        let path = `/search?title=${this.search_text}`;
        this.props.history.push(path);
        e.preventDefault()
        let state = this.state;
        state.open = false;
        this.setState(state);
    }

    handleSearchChange(e, data) {
        let state = this.state
        state.open = true
        state.loading = true
        this.setState(state)
        this.search_text = data.value

        if(data.value.length < 3){
            return
        }

        clearTimeout(this.timer);
        this.timer = setTimeout(() => {
            call_api(`/api/v0/recipes/search?title=${data.value}`, (response) =>{

                let max = 10
                if(response.recipes.length < max)
                    max = response.recipes.length
                this.setState({
                    open: true,
                    loading: false,
                    recipes: response.recipes.slice(0,max)
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
                    open={this.state.open}
                />
            </Form>
            </>
    }
}

export default withRouter(RecipeSearch);