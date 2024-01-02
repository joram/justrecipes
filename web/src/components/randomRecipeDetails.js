import _ from 'lodash';
import recipe_manifest from "../recipe_manifest.json";
import Recipe from "./recipe";
import React, {useEffect} from "react";


function RandomRecipe({searchTerm}) {
    let [recipeTitle, setRecipeTitle] = React.useState(null);

    useEffect(() => {
        if (recipeTitle !== null) {
            return;
        }

        let filtered_recipes = recipe_manifest.recipes;
        if (searchTerm) {
            filtered_recipes = [];
            const re = new RegExp(_.escapeRegExp(searchTerm), 'i');
            const isMatch = (result) => re.test(result.title);
            recipe_manifest.recipes.forEach(recipe => {
                if (isMatch(recipe)) {
                    filtered_recipes.push(recipe)
                }
            })
        }

        const random_recipe = filtered_recipes[Math.floor(Math.random() * filtered_recipes.length)];
        setRecipeTitle(random_recipe.title);
    });

    if (recipeTitle == null) {
        return null
    }

    return <Recipe recipeTitle={recipeTitle} />;
}

export default RandomRecipe;
