import React from "react";
import {List, Segment} from "semantic-ui-react";
import {Link, withRouter} from "react-router-dom";


class Categories extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            meta: {
              "categories": {},
            }
        };
    }

    componentDidMount() {
        let host = "https://recipes.oram.ca"
        if(window.location.hostname==="localhost")
          host = "http://localhost:5000"
        fetch(`${host}/api/v0/meta`)
        .then(res => res.json())
        .then(meta => {
          this.setState({
            meta: meta,
          });
        })
    }

    render() {

        function build_list(tree, key){
            let items = []
            if(Array.isArray(tree)){
                tree.forEach(category => {
                    items.push(<List.Item key={`category_${category}`}>
                        <Link to={`/category/${category}`}>{category}</Link>
                    </List.Item>)
                })
                return <List key={`category_list_${key}`}>{items}</List>
            }

            Object.keys(tree).forEach(category => {
                items.push(<List.Item key={`category_${category}`}>
                    <Link to={`/category/${category}`}>{category}</Link>
                </List.Item>)
                if(typeof(tree[category]) !== "string"){
                    let subcategory_list = build_list(tree[category], category)
                    items.push(<List.Item key={`subcategory_${category}`}>{subcategory_list}</List.Item>)
                }
            })

            return <List key={`category_list_${key}`}>{items}</List>
        }


        return <Segment>
            {build_list(this.state.meta.categories, "root")}
        </Segment>
    }
}

export default withRouter(Categories);