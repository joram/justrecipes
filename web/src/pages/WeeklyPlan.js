import {Button, Card, Container, Menu, Segment, Sidebar, SidebarPushable, SidebarPusher,} from "semantic-ui-react";
import React, {useEffect} from "react";
import RecipeCard from "../components/recipeCard";
import {searchRecipes} from "../utils.py/search_recipes";

function RecipeCards({searchTerm, recipes, selectedRecipes, onRecipeAdd}) {
    let options = [];
    recipes.forEach((recipe, index) => {
        const isSelected = selectedRecipes.includes(recipe);
        options.push(<RecipeCard recipe={recipe} onAdd={onRecipeAdd} isSelected={isSelected}/>);
    });
    return (
        <Card.Group itemsPerRow={3} stackable>
            {options}
        </Card.Group>
    );
}
const RecipeListSidebar = ({children, recipeTitles}) => {

    console.log("sidebar shows: ",recipeTitles)
    return (
        <SidebarPushable as={Segment}>
            <Sidebar
                as={Menu}
                animation='push'
                inverted
                // onHide={() => setVisible(false)}
                vertical
                visible={true}
                width='thin'
            >
                {recipeTitles.map((recipeTitle, index) => {
                    return <Menu.Item as='a' key={index}>
                        {recipeTitle}
                    </Menu.Item>
                })}
                <Menu.Item>
                    <Button basic>Make Shopping List</Button>
                </Menu.Item>
            </Sidebar>

            <SidebarPusher>
                {children}
            </SidebarPusher>
        </SidebarPushable>
    )
}
function WeekPlanPage() {
    let [selectedRecipes, setSelectedRecipes] = React.useState([]);
    let [tabSelection, setTabSelection] = React.useState("fish");
    let [fishRecipes, setFishRecipes] = React.useState([]);
    let [chickenRecipes, setChickenRecipes] = React.useState(null);
    let [beefRecipes, setBeefRecipes] = React.useState(null);
    let [porkRecipes, setPorkRecipes] = React.useState(null);
    let [vegetarianRecipes, setVegetarianRecipes] = React.useState(null);

    function onRecipeAdd(recipe) {
        setSelectedRecipes([...selectedRecipes, recipe]);
    }
    function changeTab(section) {
        const numChoices = 6;
        if(section === "fish" && fishRecipes === []){
            setFishRecipes(searchRecipes("fish", numChoices))
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
        setTabSelection(section);
    }

    function currentRecipes() {
        if (tabSelection === "fish") {
            return fishRecipes;
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
        if (tabSelection === "selected") {
            return selectedRecipes;
        }
        return []
    }

    useEffect(() => {
        setFishRecipes(searchRecipes("fish"))

    }, []);

    const recipes = currentRecipes();
    console.log(recipes)
    return <>
        <Container>
            <Menu tabular>
                <Menu.Item active={tabSelection==="fish"} onClick={() => {changeTab("fish")}}> Fish Recipes </Menu.Item>
                <Menu.Item active={tabSelection==="chicken"}  onClick={() => {changeTab("chicken")}}> Chicken Recipes </Menu.Item>
                <Menu.Item active={tabSelection==="beef"}  onClick={() => {changeTab("beef")}}> Beef Recipes </Menu.Item>
                <Menu.Item active={tabSelection==="pork"}  onClick={() => {changeTab("pork")}}> Pork Recipes </Menu.Item>
                <Menu.Item active={tabSelection==="vegetarian"}  onClick={() => {changeTab("vegetarian")}}> Vegetarian Recipes </Menu.Item>
                <Menu.Item position="right" color="blue" active={tabSelection==="selected"}  onClick={() => {changeTab("selected")}}> Selected Recipes </Menu.Item>
            </Menu>
            <Segment>
                <RecipeCards key={tabSelection} searchTerm={tabSelection} recipes={recipes} selectedRecipes={selectedRecipes} onRecipeAdd={onRecipeAdd} />
            </Segment>
        </Container>
    </>
}

export default WeekPlanPage;