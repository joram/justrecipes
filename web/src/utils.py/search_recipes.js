import _ from 'lodash';
import recipe_manifest from "../recipe_manifest.json";

const shuffle = (array) => {
    return array.map((a) => ({ sort: Math.random(), value: a }))
        .sort((a, b) => a.sort - b.sort)
        .map((a) => a.value);
};
function searchRecipes(searchTerm, numChoices=5) {
        let filtered_recipes = [];
        const re = new RegExp(_.escapeRegExp(searchTerm), 'i');
        const isMatch = (result) => re.test(result.title);

        // filter the recipes
        recipe_manifest.recipes.forEach(recipe => {
            if (isMatch(recipe) && recipe.image != null && recipe.image !== "@type") {
                filtered_recipes.push(recipe)
            }
        })

        // shuffle the recipes
        filtered_recipes = shuffle(filtered_recipes)
        if (filtered_recipes.length > numChoices) {
            filtered_recipes = filtered_recipes.slice(0, numChoices+1)
        }

        console.log(filtered_recipes)
        return filtered_recipes
}

function randomRecipe(searchTerm){
    let filtered_recipes = searchRecipes(searchTerm)
    return filtered_recipes[Math.floor(Math.random() * filtered_recipes.length)]
}

export {searchRecipes, randomRecipe}