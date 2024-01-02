import _ from 'lodash';
import recipe_manifest from "../recipe_manifest.json";
import Recipe from "./recipe";
import React, {useEffect} from "react";
import {randomRecipe} from "../utils.py/search_recipes";


function RandomRecipeDetails({searchTerm}) {
    let [recipeTitle, setRecipeTitle] = React.useState(null);

    useEffect(() => {
        if (recipeTitle !== null) {
            return;
        }
        const random_recipe = randomRecipe("");
        setRecipeTitle(random_recipe.title);
    });

    if (recipeTitle == null) {
        return null
    }

    return <Recipe recipeTitle={recipeTitle} />;
}

export default RandomRecipeDetails;
