import {Button, Card, Image} from "semantic-ui-react";
import React from "react";


function RecipeCard({recipe, onAdd, onRemove, isSelected=false}){
    let [selected, setSelected] = React.useState(isSelected);

    function onAddClick(){
        onAdd(recipe);
        setSelected(true);
    }

    function onRemoveClick(){
        onRemove(recipe);
        setSelected(false);
    }

    let header = <>
        <Button basic color='green' onClick={onAddClick}>Add</Button>
    </>;
    let isSelectedText = null;
    if (selected){
        isSelectedText = <Card.Meta style={{backgroundColor:"yellow"}}>
            Selected</Card.Meta>
        header = <Card.Content>
            <Button basic color='red' onClick={onRemoveClick}>Remove</Button>
        </Card.Content>
    }
    return <Card>
        <Card.Content>
            <Card.Header>{recipe.title}</Card.Header>
            {isSelectedText}
        </Card.Content>
        <Image src={recipe.image} wrapped ui={false} />
        <Card.Content extra>
            {header}
        </Card.Content>
    </Card>
}


export default RecipeCard;