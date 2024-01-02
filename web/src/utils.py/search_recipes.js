function searchRecipes() {
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
        return filtered_recipes
}

function randomRecipe(){
        const random_recipe = filtered_recipes[Math.floor(Math.random() * filtered_recipes.length)];

}