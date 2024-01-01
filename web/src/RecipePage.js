import {useParams} from "react-router-dom";
import React, {useEffect} from "react";
import Recipe from "./components/recipe";

function RecipePage() {
    let {recipeTitle} = useParams();
    return <Recipe recipeTitle={recipeTitle} />;
}

export default RecipePage;