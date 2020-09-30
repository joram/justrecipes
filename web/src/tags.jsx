import React from "react";
import {Grid, List, Segment} from "semantic-ui-react";
import {Link, withRouter} from "react-router-dom";


class Tags extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            meta: {
              tags: [],
            },
            num_columns: Math.floor(window.innerWidth/200),
            columns: [],
        };
    }

    updateDimensions = () => {
        let state = this.state
        let old_num_columns = state.num_columns
        state.num_columns = Math.floor(window.innerWidth/200)
        if(old_num_columns !== state.num_columns) {
            state.columns = this.calculateColumns(state.num_columns, state.meta.tags)
        }
        this.setState(state);
        console.log(state.width)
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateDimensions.bind(this));
    }

    componentDidMount() {
        window.addEventListener('resize', this.updateDimensions.bind(this));
        let host = "https://recipes.oram.ca"
        if(window.location.hostname==="localhost")
          host = "http://localhost:5000"
        fetch(`${host}/api/v0/meta`)
        .then(res => res.json())
        .then(meta => {
          let num_columns = Math.floor(window.innerWidth/200)
          this.setState({
            meta: meta,
            num_columns: num_columns,
            columns: this.calculateColumns(num_columns, meta.tags)
          });
        })
    }

    calculateColumns(num_columns, tags){
        let keyedTags = {}
        tags.forEach(tag => {
            if(tag.count>=5)
                keyedTags[tag.tag] = tag
        })

        let firstChar = ""
        let items = []
        Object.keys(keyedTags).sort().forEach(tagName => {
            let tag = keyedTags[tagName]
            if(tagName[0] !== firstChar) {
                firstChar = tagName[0]
                console.log(firstChar)
                items.push(<List.Header key={`tag_${firstChar}`}>{firstChar}</List.Header>
            )
            }

            items.push(<List.Item key={`tag_${tag.tag}`}>
                <Link to={`/tag/${tag.tag}`}>{tag.tag} ({tag.count})</Link>
            </List.Item>
            )
        })

        let columns = []
        if(num_columns > 8)
            num_columns = 8
        let rows_per_column = items.length/num_columns
        let i,j;
        for (i=0,j=items.length; i<j; i+=rows_per_column) {
            let column_list = items.slice(i,i+rows_per_column);
            columns.push(<Grid.Column>
                <List key={`tag_${i}`}>{column_list}</List>
            </Grid.Column>)
        }
        console.log(`using ${num_columns} columns for ${items.length} columns, chunked into ${rows_per_column}`)
        return columns
    }

    render() {
        return <Segment basic>
            <Grid columns={this.state.num_columns} divided>
                {this.state.columns}
            </Grid>
        </Segment>
    }
}

export default withRouter(Tags);