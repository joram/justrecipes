import React from 'react';
import {SearchBar} from '@rneui/themed';
import recipeManifest from "../recipe_manifest.json";
import {searchRecipes} from "../utils/recipes";


function RecipeSearchBox({resultsCallback}) {
    let [searchText, setSearchText] = React.useState("");

    let count = 0;
    if(recipeManifest) count = recipeManifest.recipes.length;
    const placeholder = `Type Here... (${count} recipes)`

    return <SearchBar
        placeholder={placeholder}
        onChangeText={setSearchText}
        value={searchText}
        onSubmitEditing={() => {
            resultsCallback(searchRecipes(searchText))
        }}
    />
}

export default RecipeSearchBox;