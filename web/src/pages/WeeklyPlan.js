import {Container, Menu, Segment,} from "semantic-ui-react";
import React, {useEffect} from "react";
import {searchRecipes} from "../utils/search_recipes";
import RecipeCards from "../components/recipeCards";
import {apiAddRecipeToPlan, apiGetPlan, apiRemoveRecipeFromPlan} from "../utils/api";

function WeekPlanPage() {
    let [selectedRecipes, setSelectedRecipes] = React.useState([]);
    let [tabSelection, setTabSelection] = React.useState("fish");
    let [fishRecipes, setFishRecipes] = React.useState([]);
    let [shrimpRecipes, setShrimpRecipes] = React.useState(null);
    let [chickenRecipes, setChickenRecipes] = React.useState(null);
    let [beefRecipes, setBeefRecipes] = React.useState(null);
    let [porkRecipes, setPorkRecipes] = React.useState(null);
    let [vegetarianRecipes, setVegetarianRecipes] = React.useState(null);
    let [tofuRecipes, setTofuRecipes] = React.useState(null);
    let [beanRecipes, setBeanRecipes] = React.useState(null);

    useEffect(() => {
        apiGetPlan(2021, 1).then((data) => {
            let alreadySelectedRecipes = [];
            data.recipes.forEach((recipe_title) => {
                searchRecipes(recipe_title, 1).forEach((recipe) => {
                    alreadySelectedRecipes.push(recipe)
                })
            })
            setSelectedRecipes(alreadySelectedRecipes)
        });
    }, []);

    function onRecipeAdd(recipe) {
        setSelectedRecipes([...selectedRecipes, recipe]);
        apiAddRecipeToPlan(2021, 1, recipe.title).then(r => console.log(r))
    }

    function onRecipeRemove(recipe) {
        setSelectedRecipes(selectedRecipes.filter((r) => r !== recipe));
        apiRemoveRecipeFromPlan(2021, 1, recipe.title).then(r => console.log(r))
    }

    function changeTab(section) {
        const numChoices = 6;
        if(section === "fish" && fishRecipes === []){
            setFishRecipes(searchRecipes("fish", numChoices))
        }
        if(section === "shrimp" && shrimpRecipes == null){
            setShrimpRecipes(searchRecipes("shrimp", numChoices))
        }
        if(section === "chicken" && chickenRecipes == null){
            setChickenRecipes(searchRecipes("chicken", numChoices))
        }
        if(section === "beef" && beefRecipes == null){
            setBeefRecipes(searchRecipes("beef", numChoices))
        }
        if(section === "pork" && porkRecipes == null){
            setPorkRecipes(searchRecipes("pork", numChoices))
        }
        if(section === "vegetarian" && vegetarianRecipes == null){
            setVegetarianRecipes(searchRecipes("vegetarian", numChoices))
        }
        if(section === "tofu" && tofuRecipes == null){
            setTofuRecipes(searchRecipes("tofu", numChoices))
        }
        if(section === "bean" && beanRecipes == null){
            setBeanRecipes(searchRecipes("bean", numChoices))
        }

        setTabSelection(section);
    }

    function currentRecipes() {
        if (tabSelection === "fish") {
            return fishRecipes;
        }
        if (tabSelection === "shrimp") {
            return shrimpRecipes;
        }
        if (tabSelection === "chicken") {
            return chickenRecipes;
        }
        if (tabSelection === "beef") {
            return beefRecipes;
        }
        if (tabSelection === "pork") {
            return porkRecipes;
        }
        if (tabSelection === "vegetarian") {
            return vegetarianRecipes;
        }
        if (tabSelection === "tofu") {
            return tofuRecipes;
        }
        if (tabSelection === "bean") {
            return beanRecipes;
        }
        if (tabSelection === "selected") {
            return selectedRecipes;
        }
        return []
    }

    useEffect(() => {
        setFishRecipes(searchRecipes("fish"))

    }, []);

    const recipes = currentRecipes();
    return <>
        <Container>
            <Menu tabular>
                <Menu.Item active={tabSelection==="fish"} onClick={() => {changeTab("fish")}}> Fish </Menu.Item>
                <Menu.Item active={tabSelection==="shrimp"} onClick={() => {changeTab("shrimp")}}> Shrimp </Menu.Item>
                <Menu.Item active={tabSelection==="chicken"}  onClick={() => {changeTab("chicken")}}> Chicken </Menu.Item>
                <Menu.Item active={tabSelection==="beef"}  onClick={() => {changeTab("beef")}}> Beef </Menu.Item>
                <Menu.Item active={tabSelection==="pork"}  onClick={() => {changeTab("pork")}}> Pork </Menu.Item>
                <Menu.Item active={tabSelection==="vegetarian"}  onClick={() => {changeTab("vegetarian")}}> Vegetarian </Menu.Item>
                <Menu.Item active={tabSelection==="tofu"}  onClick={() => {changeTab("tofu")}}> Tofu </Menu.Item>
                <Menu.Item active={tabSelection==="bean"}  onClick={() => {changeTab("bean")}}> Beans </Menu.Item>
                <Menu.Item position="right" color="blue" active={tabSelection==="selected"}  onClick={() => {changeTab("selected")}}> {selectedRecipes.length} Selected Recipes </Menu.Item>
            </Menu>
            <Segment>
                <RecipeCards
                    key={tabSelection}
                    searchTerm={tabSelection}
                    recipes={recipes}
                    selectedRecipes={selectedRecipes}
                    onRecipeAdd={onRecipeAdd}
                    onRecipeRemove={onRecipeRemove}
                />
            </Segment>
        </Container>
    </>
}

export default WeekPlanPage;