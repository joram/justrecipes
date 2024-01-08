import Recipe from "./recipe";
import React, {useEffect} from "react";
import {randomRecipe} from "../utils/search_recipes";


function RandomRecipeDetails({searchTerm}) {
    let [recipeTitle, setRecipeTitle] = React.useState(null);

    useEffect(() => {
        if (recipeTitle !== null) {
            return;
        }
        const random_recipe = randomRecipe("");
        setRecipeTitle(random_recipe.title);
    }, [recipeTitle]);

    return <Recipe key={recipeTitle} recipeTitle={recipeTitle} />;
}

export default RandomRecipeDetails;
