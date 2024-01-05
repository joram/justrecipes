/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React from 'react';

import {SafeAreaView, ScrollView, useColorScheme,} from 'react-native';

import {Colors,} from 'react-native/Libraries/NewAppScreen';
import RecipePage from "./pages/recipe";
import {getRandomRecipeName} from "./utils/recipes";
import RecipeSearchResultsPage from "./pages/recipe_search";
import RecipeSearchBox from "./components/recipe_search_box";

function App(): React.JSX.Element {
    const isDarkMode = useColorScheme() === 'dark';
    let [recipeName, setRecipeName] = React.useState<string>(null);
    let [searchResults, setSearchResults] = React.useState([]);

    React.useEffect(() => {
        setRecipeName(getRandomRecipeName())
    }, [])
    const backgroundStyle = {
        backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
    };

    function recipeSearchResults(recipes) {
        setSearchResults(recipes)
    }

    function recipeSelected(recipeName) {
        setRecipeName(recipeName)
        setSearchResults([])
    }

    let content = <RecipePage backgroundStyle={backgroundStyle} recipeName={recipeName}/>
    if(searchResults.length > 0) {
        content = <RecipeSearchResultsPage recipes={searchResults} onPress={recipeSelected}/>
    }
    return (
    <SafeAreaView style={backgroundStyle}>
        <RecipeSearchBox onSelect={setRecipeName} resultsCallback={recipeSearchResults}/>
        <ScrollView>
            {content}
        </ScrollView>
    </SafeAreaView>
    );
}

export default App;
