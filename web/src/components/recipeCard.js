import {Button, Card, Image} from "semantic-ui-react";
import React, {useEffect} from "react";


function RecipeCard({recipe, onAdd, isSelected=false}){
    let [selected, setSelected] = React.useState(isSelected);

    function onClick(){
        onAdd(recipe);
        setSelected(true);
    }

    let header = <>
        <Button basic color='green' onClick={onClick}>Add</Button>
    </>;
    let isSelectedText = null;
    if (selected){
        isSelectedText = <Card.Meta style={{backgroundColor:"yellow"}}>
            Selected</Card.Meta>
        header = <Card.Content>
            <Button basic color='red'>Remove</Button>
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