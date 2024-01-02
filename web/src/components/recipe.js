import {Container, Grid, Header, Table} from "semantic-ui-react";
import ImageCarousel from "./imageCarousel";
import React, {useEffect} from "react";

function RecipeImages({recipe}){
    return ImageCarousel(recipe.image_urls);
}

function RecipeIngredients({recipe}){
    return <>
        <Header as='h3'>Ingredients</Header>
        <Table>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Ingredient</Table.HeaderCell>
                    <Table.HeaderCell>Amount</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {recipe.ingredients.map( (ingredient, index) => {
                    return <Table.Row key={index}>
                        <Table.Cell>{ingredient.name}</Table.Cell>
                        <Table.Cell>{ingredient.amount} {ingredient.unit}</Table.Cell>
                    </Table.Row>
                })}
            </Table.Body>
        </Table>
    </>
}

function RecipeInstructions({recipe}){
    return <>
        <Header as='h3'>Instructions</Header>
        <Table striped>
            {recipe.instructions.map((instruction, index) => {
                    return <Table.Row>
                        <Table.Cell key={index}>{instruction}</Table.Cell>
                    </Table.Row>
                }
            )}
        </Table>
    </>
}

function RecipeNutrients({recipe}) {
    return <>
        <Header as='h3'>Nutrients</Header>
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
        <Header as='h3'>Metadata</Header>
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
        if (recipeTitle == null) {
            return null;
        }

        fetch(filepath)
            .then(response => response.json())
            .then(data => {
                setRecipe(data)

            });
    }, [filepath]);


    if (!recipe) return (<div>Loading...</div>);

    return <Container>
        <h1>{recipeTitle}</h1>
        <RecipeImages recipe={recipe} />
        <Grid columns={4} divided>
            <Grid.Row>
                <Grid.Column>
                    <RecipeMetadata recipe={recipe} />
                </Grid.Column>
                <Grid.Column>
                    <RecipeIngredients recipe={recipe} />
                </Grid.Column>
                <Grid.Column>
                    <RecipeInstructions recipe={recipe} />
                </Grid.Column>
                <Grid.Column>
                    <RecipeNutrients recipe={recipe} />
                </Grid.Column>
            </Grid.Row>
        </Grid>
    </Container>
}


export default Recipe;