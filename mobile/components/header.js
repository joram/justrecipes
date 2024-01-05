
import React from 'react';
import {ImageBackground, useColorScheme, StyleSheet, Text} from "react-native";
import {
    Colors,
} from 'react-native/Libraries/NewAppScreen';

function Header({imgUri, text}) {
    const isDarkMode = useColorScheme() === 'dark';
    return (
        <ImageBackground
            accessibilityRole="image"
            source={{uri:imgUri}}
            style={[
                styles.background,
                {
                    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
                },
            ]}
            imageStyle={styles.logo}>
            <Text
                style={[
                    styles.text,
                    {
                        color: isDarkMode ? Colors.white : Colors.black,
                    },
                ]}>
                {text}
            </Text>
        </ImageBackground>
    );
};

const styles = StyleSheet.create({
    background: {
        paddingBottom: 40,
        paddingTop: 30,
        paddingHorizontal: 32,
    },
    logo: {
        opacity: 0.2,
        overflow: 'visible',
        resizeMode: 'cover',
        /*
         * These negative margins allow the image to be offset similarly across screen sizes and component sizes.
         *
         * The source logo.png image is 512x512px, so as such, these margins attempt to be relative to the
         * source image's size.
         */
        marginLeft: -128,
        marginBottom: -192,
    },
    text: {
        fontSize: 40,
        fontWeight: '700',
        textAlign: 'center',
    },
});

export default Header;
