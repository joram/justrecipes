import RecipeCard from "./recipeCard";
import {Card} from "semantic-ui-react";
import React from "react";


function RecipeCards({searchTerm, recipes, selectedRecipes, onRecipeAdd, onRecipeRemove}) {
    let options = [];
    recipes.forEach((recipe, index) => {
        const isSelected = selectedRecipes.includes(recipe);
        options.push(<RecipeCard
            key={recipe.title}
            recipe={recipe}
            onAdd={onRecipeAdd}
            onRemove={onRecipeRemove}
            isSelected={isSelected}
        />);
    });
    return (
        <Card.Group itemsPerRow={3} stackable>
            {options}
        </Card.Group>
    );
}

export default RecipeCards;