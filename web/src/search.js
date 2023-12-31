import _ from 'lodash';
import React from 'react';
import {Search} from 'semantic-ui-react';
import recipe_manifest from './recipe_manifest.json';
import {useNavigate} from "react-router-dom";

console.log(recipe_manifest);
let source = [];


const initialState = {
    loading: false,
    results: [],
    value: '',
}

function exampleReducer(state, action) {
    switch (action.type) {
        case 'CLEAN_QUERY':
            return initialState
        case 'START_SEARCH':
            return { ...state, loading: true, value: action.query }
        case 'FINISH_SEARCH':
            return { ...state, loading: false, results: action.results }
        case 'UPDATE_SELECTION':
            return { ...state, value: action.selection }

        default:
            throw new Error()
    }
}

function SearchExampleStandard() {
    const navigate = useNavigate();

    function calculate_search_source_data() {
        source = recipe_manifest.recipes;
        source = source.map((recipe) => {
            return {
                title: recipe.title,
                image: recipe.image,
                onClick: () => {
                    console.log("going to recipe "+recipe)
                    console.log(recipe)
                    navigate("/recipe/"+recipe.title);

                }
            }
        });

        console.log(source);
    }




    const [state, dispatch] = React.useReducer(exampleReducer, initialState)
    const { loading, results, value } = state

    const timeoutRef = React.useRef()

    const handleSearchChange = React.useCallback((e, data) => {
        clearTimeout(timeoutRef.current)
        dispatch({ type: 'START_SEARCH', query: data.value })

        timeoutRef.current = setTimeout(() => {
            if (data.value.length === 0) {
                dispatch({ type: 'CLEAN_QUERY' })
                return
            }

            const re = new RegExp(_.escapeRegExp(data.value), 'i')
            const isMatch = (result) => re.test(result.title)

            dispatch({
                type: 'FINISH_SEARCH',
                results: _.filter(source, isMatch),
            })
        }, 300)
    }, [])
    React.useEffect(() => {
        calculate_search_source_data();
        return () => {
            clearTimeout(timeoutRef.current)
        }
    }, [])

    return (
        <Search
            loading={loading}
            placeholder='Search...'
            onResultSelect={(e, data) =>
                dispatch({ type: 'UPDATE_SELECTION', selection: data.result.title })
            }
            onSearchChange={handleSearchChange}
            results={results}
            value={value}
        />
    )
}

export default SearchExampleStandard