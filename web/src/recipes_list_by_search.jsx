import React from "react";
import RecipesList from "./recipes_list";
import {withRouter} from "react-router-dom";
import {Pagination} from "semantic-ui-react";
import call_api from "./utils";

let qs = require('qs');

function url_params(params) {
    for (let param in params) {
        if (params[param] === null || params[param] === undefined || params[param] === "") {
            delete params[param];
        }
    }

    let esc = encodeURIComponent;
    return Object.keys(params)
        .map(k => esc(k) + '=' + esc(params[k]))
        .join('&')
}

class RecipesListBySearch extends React.Component {

    constructor(props) {
        super(props);
        let search = this.props.location.search;
        search = search.substring(1)
        search = qs.parse(search)
        this.state = {
            recipes: [],
            page: search.page ? search.page : 1,
            page_count: search.page_count ? search.page_count : 1,
            title: search.title ? search.title : "",
            tag: search.tag ? search.tag : "",
            ingredient: search.ingredient ? search.ingredient : "",
        };

    }

    componentDidMount() {
        this.query_api()
    }


    query_api(){
        let params = url_params({
            title: this.state.title,
            tag: this.state.tag,
            ingredient: this.state.ingredient,
            page: this.state.page,
            page_count: this.state.page_count,
        })
        let path = `/api/v0/recipes/search?`+params
        call_api(path, (response) =>{
          this.setState(response);
          let params = url_params({
            title: this.state.title,
            tag: this.state.tag,
            ingredient: this.state.ingredient,
            page: this.state.page,
            page_count: this.state.page_count,
          })
          let newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?'+params;
          window.history.pushState({path:newurl},'',newurl);
        })
    }

    onPageChange(event, data){
        let state = this.state;
        state.page = data.activePage;
        this.setState(state);
        this.query_api()
    }

    render() {
        return <>
            <RecipesList recipes={this.state.recipes} />
            <div style={{display: 'flex', justifyContent: 'center'}}>
                <Pagination
                    activePage={this.state.page}
                    totalPages={this.state.page_count}
                    onPageChange={this.onPageChange.bind(this)}
                />
            </div>
        </>
    }
}

export default  withRouter(RecipesListBySearch)
