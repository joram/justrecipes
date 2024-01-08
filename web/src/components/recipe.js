import {Container, Grid, Header, Segment, Tab, Table} from "semantic-ui-react";
import ImageCarousel from "./imageCarousel";
import React, {useEffect} from "react";

function RecipeImages({recipe}){
    return ImageCarousel(recipe.image_urls);
}

function RecipeIngredients({recipe}){
    return <>
        <Table>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Ingredient</Table.HeaderCell>
                    <Table.HeaderCell>Amount</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {recipe.ingredients.map( (ingredient, index) => {
                    const roundedAmount = Math.round(ingredient.amount * 100) / 100;
                    return <Table.Row key={index}>
                        <Table.Cell>{ingredient.name}</Table.Cell>
                        <Table.Cell>{roundedAmount} {ingredient.unit}</Table.Cell>
                    </Table.Row>
                })}
            </Table.Body>
        </Table>
    </>
}

function RecipeInstructions({recipe}){

    const instructions = recipe.instructions.map((instruction, index) => {
        return <Segment basic key={index} style={{paddingTop:5, paddingBottom:5}}>
            <h5>Step {index+1}</h5>
            {instruction}
        </Segment>
        }
    )

    return <>
        <Header as='h3'>Instructions</Header>
        <Segment.Group>
            {instructions}
        </Segment.Group>
    </>
}

function RecipeNutrients({recipe}) {
    return <>
        <Table striped>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Nutrient</Table.HeaderCell>
                    <Table.HeaderCell>Amount</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {recipe.nutrition_infos.map( (nutrient, index) => {
                    if (nutrient.amount === 0){
                        return null;
                    }
                    return <Table.Row key={index}>
                        <Table.Cell>{nutrient.name}</Table.Cell>
                        <Table.Cell>{nutrient.amount}{nutrient.unit}</Table.Cell>
                    </Table.Row>
                })}
            </Table.Body>
        </Table>
    </>
}

function RecipeMetadata(props) {
    const routeDomain = props.recipe.source_url.split("/")[2]

    return <>
        <Table>
            <Table.Body>
                <Table.Row>
                    <Table.Cell>Total Time</Table.Cell>
                    <Table.Cell>{props.recipe.minutes} minutes</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Yield</Table.Cell>
                    <Table.Cell>{props.recipe.servings} servings</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Source</Table.Cell>
                    <Table.Cell><a href={props.recipe.source_url}>{routeDomain}</a></Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Tags</Table.Cell>
                    <Table.Cell>{props.recipe.categories.join(", ")}</Table.Cell>
                </Table.Row>
            </Table.Body>
        </Table>
    </>
}


function Recipe({recipeTitle}){
    let [recipe, setRecipe] = React.useState(null);
    const filepath = `/recipes/${recipeTitle}.json`;


    useEffect(() => {
        if (recipe !== null) {
            return;
        }

        fetch(filepath)
            .then(response => response.json())
            .then(data => {
                setRecipe(data)
            });
    });


    if (!recipe) return (<div>Loading...</div>);


    const panes = [
        { menuItem: 'Ingredients', render: () => <Tab.Pane><RecipeIngredients recipe={recipe}/></Tab.Pane> },
        { menuItem: 'Details', render: () => <Tab.Pane>
                <RecipeMetadata recipe={recipe}/>
                <RecipeNutrients recipe={recipe}/>
            </Tab.Pane> },
    ]

    const tabbedSidebar = <Tab panes={panes} />


    const informationTable = <Table>
        <Table.Body>
            <Table.Row verticalAlign={"top"}>
                <Table.Cell width={1}>
                    {tabbedSidebar}
                </Table.Cell>
                <Table.Cell width={5}>
                    <RecipeInstructions recipe={recipe}/>
                </Table.Cell>
            </Table.Row>
        </Table.Body>
    </Table>
    return <Container>
        <Segment basic><RecipeImages recipe={recipe} /></Segment>
        <Segment basic>{informationTable}</Segment>
    </Container>
}


export default Recipe;