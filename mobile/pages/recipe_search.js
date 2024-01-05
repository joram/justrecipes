import _ from 'lodash';
import React from 'react';
import {SearchBar} from '@rneui/themed';
import recipeManifest from "./recipe_manifest.json";

const shuffle = (array) => {
    return array.map((a) => ({ sort: Math.random(), value: a }))
        .sort((a, b) => a.sort - b.sort)
        .map((a) => a.value);
};

function RecipeSearchPage({resultsCallback}) {
    let [searchText, setSearchText] = React.useState("");

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

        resultsCallback(filtered_recipes)
    }

    let count = 0;
    if(recipeManifest) count = recipeManifest.recipes.length;
    const placeholder = `Type Here... (${count} recipes)`

    return <SearchBar
        placeholder={placeholder}
        onChangeText={setSearchText}
        value={searchText}
        onSubmitEditing={() => searchRecipes(searchText)}
    />
}

export default RecipeSearchPage;