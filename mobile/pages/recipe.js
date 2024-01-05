import React, {useEffect, useState} from "react";
import {FlatList, ScrollView, StyleSheet, Text, useColorScheme, View} from "react-native";
import {Colors} from "react-native/Libraries/NewAppScreen";
import Header from "../components/header";
import {getRecipe} from "../utils/recipes";
import BouncyCheckbox from "react-native-bouncy-checkbox";

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
        <>
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
        </>
    );
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


function Ingredient({ingredient}) {
    const text = `${ingredient.amount}${ingredient.unit} - ${ingredient.name}`
    return <BouncyCheckbox text={text} style={{marginTop:5, marginLeft:20}}/>
}

Ingredient.propTypes = {};

function RecipeIngredients({recipe}){
    let ingredients = [];
    if(recipe){
        ingredients = recipe.ingredients
    }

    function renderIngredient(ingredient){
        return <Ingredient ingredient={ingredient.item} />
    }

    return <>
        <FlatList data={ingredients} renderItem={renderIngredient}></FlatList>
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
            <Text style={{height:150}} />
        </View>
    </ScrollView>
}


export default RecipePage;