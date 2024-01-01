import recipe_manifest from "../recipe_manifest.json";
import Recipe from "./recipe";
import React, {useEffect} from "react";


function RandomRecipe() {
    let [recipeTitle, setRecipeTitle] = React.useState(null);

    useEffect(() => {
        if (recipeTitle !== null) {
            return;
        }
        const random_recipe = recipe_manifest.recipes[Math.floor(Math.random() * recipe_manifest.recipes.length)];
        setRecipeTitle(random_recipe.title);
    });

    if (recipeTitle == null) {
        return null
    }

    return <Recipe recipeTitle={recipeTitle} />;
}

export default RandomRecipe;
