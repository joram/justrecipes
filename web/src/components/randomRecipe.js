import recipe_manifest from "./recipe_manifest.json";
import Recipe from "./components/recipe";

function RandomRecipe() {
    let [recipes, setRecipes] = React.useState(null);
    let [recipeName, setRecipeName] = React.useState(null);

    function update_recipe() {
        if (recipes != null) {
            return;
        }
        setRecipes(recipe_manifest.recipes);
        const random_recipe = recipes[Math.floor(Math.random() * recipes.length)];
        console.log(random_recipe)
    }

    if (recipes == null) {
        update_recipe();
        return null
    }

    return Recipe({recipeTitle: random_recipe.title});
}

export default RandomRecipe;
