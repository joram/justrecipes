import React, {useEffect} from "react";
import {ScrollView, StyleSheet, Text, useColorScheme, View} from "react-native";
import {Colors} from "react-native/Libraries/NewAppScreen";
import * as RNFS from "react-native-fs";
import Header from "../componenents/header";
import { ListItem } from '@rneui/themed';

const styles = StyleSheet.create({
    sectionContainer: {
        marginTop: 15,
        paddingHorizontal: 24,
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: '600',
    },
    sectionDescription: {
        marginTop: 8,
        fontSize: 18,
        fontWeight: '400',
    },
    highlight: {
        fontWeight: '700',
    },
    tinyLogo: {
        width: 107,
        height: 165,
        padding: 10
    },
});

function Section({children, title}) {
    const isDarkMode = useColorScheme() === 'dark';
    return (
        <View style={styles.sectionContainer}>
            <Text
                style={[
                    styles.sectionTitle,
                    {
                        color: isDarkMode ? Colors.white : Colors.black,
                    },
                ]}>
                {title}
            </Text>
            <Text
                style={[
                    styles.sectionDescription,
                    {
                        color: isDarkMode ? Colors.light : Colors.dark,
                    },
                ]}>
                {children}
            </Text>
        </View>
    );
}

function getRecipe(name) {
    const filepath = `custom/${name}.json`;
    return RNFS.readFileAssets(filepath, 'utf8').then((res) => {
        return JSON.parse(res)
    }).catch((err) => {
        console.log(err.message, err.code);

    })
}

function RecipeInstructions({recipe}){
    if(!recipe) return null

    let sections = [];
    if(recipe){
        let i = 1;
        recipe.instructions.forEach(instruction => {
            sections.push(<Section title={`Step ${i}`} key={i}>
                <Text>{instruction}</Text>
            </Section>);
            i += 1
        })
    }
    return <>
        {sections}
    </>
}


function RecipeIngredients({recipe}){
    if(!recipe) return null
    let ingredients = [];
    recipe.ingredients.forEach(ingredient => {
        ingredients.push(<ListItem key={ingredient.name}>
            <ListItem.Content>
                <ListItem.Title>{ingredient.name}</ListItem.Title>
                <ListItem.Subtitle>{ingredient.amount}{ingredient.unit}</ListItem.Subtitle>
            </ListItem.Content>
        </ListItem>);
    });

    return <>
        <Text>Ingredients</Text>
        {ingredients}
    </>
}


function RecipeImage({recipe}){
    if(!recipe) return null
    const uri = recipe.image_urls[0]
    console.log(uri)
    return <Header imgUri={uri} text={recipe.name}/>
}

function RecipePage({backgroundStyle, recipeName}) {
    const isDarkMode = useColorScheme() === 'dark';
    let [recipe, setRecipe] = React.useState(null);

    useEffect(() => {
        getRecipe(recipeName).then((recipe) => {
            if(recipe){
                setRecipe(recipe);
            }
        });
    }, [recipeName]);

    return <ScrollView contentInsetAdjustmentBehavior="automatic" style={backgroundStyle}>
        <View style={{ backgroundColor: isDarkMode ? Colors.black : Colors.white, }}>

            <RecipeImage recipe={recipe} />
            <RecipeIngredients recipe={recipe} />
            <RecipeInstructions recipe={recipe} />
        </View>
    </ScrollView>
}


export default RecipePage;