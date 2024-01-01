import _ from 'lodash';
import React from 'react';
import {Search} from 'semantic-ui-react';
import recipe_manifest from './recipe_manifest.json';
import {useNavigate} from "react-router-dom";

function SearchExampleStandard() {
    const navigate = useNavigate();
    let [recipes, setRecipes] = React.useState(null);
    let [results, setResults] = React.useState([]);
    let [value, setValue] = React.useState("");

    function update_recipes() {
        if (recipes != null) {
            return;
        }
        let _recipes = recipe_manifest.recipes;
        _recipes = _recipes.map((recipe) => {
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
        setRecipes(_recipes);
    }

    React.useEffect(() => {
        update_recipes();
    })


    const timeoutRef = React.useRef()

    const handleSearchChange = React.useCallback((e, data) => {
        clearTimeout(timeoutRef.current)
        console.log("searching", data)

        const re = new RegExp(_.escapeRegExp(data.value), 'i');
        const isMatch = (result) => re.test(result.title);
        let newResults = []
        recipes.forEach(recipe => {
            if(isMatch(recipe)) {
                newResults.push(recipe)
            }
        })

        setValue(data.value)
        setResults(newResults)
    }, [recipes])



    return (
        <Search
            loading={false}
            placeholder='Search...'
            onResultSelect={(e, data) =>
                console.log("selected", data)
            }
            onSearchChange={handleSearchChange}
            results={results}
            value={value}
        />
    )
}

export default SearchExampleStandard