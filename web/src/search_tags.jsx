import React from "react";
import {Label} from "semantic-ui-react";
import {withRouter} from "react-router-dom";
let qs = require('qs');


class BaseSearchFilter extends React.Component {
    render() {
        return <Label as='a' color={this.props.color}>
            {this.props.title.title}
            <Label.Detail>{this.props.type}</Label.Detail>
        </Label>
    }
}

const IngredientSearchFilter = (title) => (
     <BaseSearchFilter color="red" title={title} type="ingredient" />
)

const TitleSearchFilter = (title) => (
     <BaseSearchFilter color="orange" title={title} type="title" />
)

const TagSearchFilter = (title) => (
     <BaseSearchFilter color="yellow" title={title} type="tag" />
)

class SearchTags extends React.Component {
    render() {
        let search = this.props.location.search;
        search = search.substring(1)
        search = qs.parse(search)

        let search_filters = []
        if(search.title !== undefined) {
            search.title.split(",").forEach( (title) => {
                search_filters.push(
                    <TitleSearchFilter key={title} title={title}/>
                )
            })
        }
        if(search.tag !== undefined) {
            search.tag.split(",").forEach( (tag) => {
                search_filters.push(
                    <TagSearchFilter key={tag} title={tag}/>
                )
            })
        }
        if(search.ingredient !== undefined) {
            search.ingredient.split(",").forEach( (ingredient) => {
                search_filters.push(
                    <IngredientSearchFilter key={ingredient} title={ingredient}/>
                )
            })
        }

        return <div style={{paddingTop:"5px"}}>
            {search_filters}
        </div>
    }
}

export default withRouter(SearchTags)