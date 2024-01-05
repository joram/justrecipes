/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React from 'react';

import {Dimensions, SafeAreaView, ScrollView, Text, useColorScheme,} from 'react-native';

import {Colors,} from 'react-native/Libraries/NewAppScreen';
import RecipePage from "./pages/recipe";
import RecipeSearchPage from "./pages/recipe_search";
import {FullWidthCard} from "./componenents/full_width_card";
import {Stack} from '@rneui/layout';
import {Card, Image} from "@rneui/base";

class PostItem extends React.Component {

    state = {
        imgWidth: 0,
        imgHeight: 0,
    }

    componentDidMount() {

        Image.getSize(this.props.imageUrl, (width, height) => {
            // calculate image width and height
            const screenWidth = Dimensions.get('window').width
            const scaleFactor = width / screenWidth
            const imageHeight = height / scaleFactor
            this.setState({imgWidth: screenWidth, imgHeight: imageHeight})
        })
    }

    render() {

        const {imgWidth, imgHeight} = this.state

        return (
            <View>
                <Image
                    style={{width: imgWidth, height: imgHeight}}
                    source={{uri: this.props.imageUrl}}
                />
                <Text style={styles.title}>
                    {this.props.description}
                </Text>
            </View>
        )
    }
}

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

function App(): React.JSX.Element {
    const isDarkMode = useColorScheme() === 'dark';
    let [recipeName, setRecipeName] = React.useState<string>("Affogato");
    let [searchResults, setSearchResults] = React.useState([]);

    const backgroundStyle = {
        backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
    };

    function recipeSearchResults(recipes) {
        setSearchResults(recipes)
    }

    function recipeSelected(recipeName) {
        console.log("selected recipe: " + recipeName)
        setRecipeName(recipeName)
        setSearchResults([])
    }

    let content = <RecipePage backgroundStyle={backgroundStyle} recipeName={recipeName}/>
    if(searchResults.length > 0) {
        content = <RecipeSearchResultsPage recipes={searchResults} onPress={recipeSelected}/>
    }
    return (
    <SafeAreaView style={backgroundStyle}>
        <RecipeSearchPage onSelect={setRecipeName} resultsCallback={recipeSearchResults}/>
        <ScrollView>
            {content}
        </ScrollView>
    </SafeAreaView>
    );
}

export default App;
