import React from 'react';
import {Card, Image} from "@rneui/base";
import {Dimensions} from "react-native";
import {Stack} from "@rneui/layout";


function RecipeSearchResult({ title, image_url, onPress }) {
    let [imgWidth, setImgWidth] = React.useState(0);
    let [imgHeight, setImgHeight] = React.useState(0);

    Image.getSize(image_url, (width, height) => {
        // calculate image width and height
        const screenWidth = Dimensions.get('window').width
        const scaleFactor = width / screenWidth
        const imageHeight = height / scaleFactor
        setImgWidth(screenWidth);
        setImgHeight(imageHeight);
    })

    function handlePress() {
        onPress(title)
    }

    return <Card
        key={title}
        onPress={handlePress}
        containerStyle={{paddingBottom:0}}
    >
        <Card.Title onPress={handlePress}>{title}</Card.Title>
        <Card.Image onPress={handlePress} style={{width: imgWidth, height: imgHeight}} source={{ uri: image_url }}/>
    </Card>

}

function RecipeSearchResultsPage({ recipes, onPress }) {
    let results = recipes.map((recipe) => {
        return <RecipeSearchResult title={recipe.title} image_url={recipe.image} onPress={onPress} />
    });
    return <Stack align="center" spacing={2} flexDirection={"row"}>{results}</Stack>
}


export default RecipeSearchResultsPage