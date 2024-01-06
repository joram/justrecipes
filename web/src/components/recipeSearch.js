import _ from 'lodash';
import React from 'react';
import {Search} from 'semantic-ui-react';
import recipe_manifest from '../recipe_manifest.json';
import {useNavigate} from "react-router-dom";
import {numTotalRecipes} from "../utils.py/search_recipes";

const BreakException = {msg: "break"};

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
                    navigate("/recipe/"+recipe.title);

                }
            }
        });
        console.log("got "+_recipes.length+" recipes")
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

        let done = false
        while(!done) {
            if (recipes == null) {
                break;
            }
            try {
                recipes.forEach(recipe => {
                    if (isMatch(recipe)) {
                        newResults.push(recipe)
                    }
                    if (newResults.length > 10) {
                        done = true;
                        throw BreakException;
                    }
                })
            } catch (e) {
                if (e !== BreakException) throw e;
            }
            done = true;
        }

        setValue(data.value)
        setResults(newResults)
    }, [recipes])



    return (
        <Search
            loading={false}
            placeholder={`Search ${numTotalRecipes()} recipes`}
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