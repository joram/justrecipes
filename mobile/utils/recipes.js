import recipeManifest from "../recipe_manifest.json";
import * as RNFS from "react-native-fs";
import _ from "lodash";

function getRecipe(name) {
    const filepath = `custom/${name}.json`;
    return RNFS.readFileAssets(filepath, 'utf8').then((res) => {
        return JSON.parse(res)
    }).catch((err) => {
        console.log(err.message, err.code);

    })
}

function getRandomRecipeName(){
    const recipe = recipeManifest.recipes[Math.floor(Math.random() * recipeManifest.recipes.length)];
    return recipe.title
}

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
    recipeManifest.recipes.forEach(recipe => {
        if (isMatch(recipe) && recipe.image != null && recipe.image !== "@type") {
            filtered_recipes.push(recipe)
        }
    })

    // shuffle the recipes
    filtered_recipes = shuffle(filtered_recipes)
    if (filtered_recipes.length > numChoices) {
        filtered_recipes = filtered_recipes.slice(0, numChoices+1)
    }

    return filtered_recipes
}

export { getRecipe, getRandomRecipeName, searchRecipes }