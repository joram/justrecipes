/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React, {useEffect} from 'react';
import type {PropsWithChildren} from 'react';
import * as RNFS from 'react-native-fs';

import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  useColorScheme,
  View,
} from 'react-native';

import {
  Colors,
  DebugInstructions,
  Header,
  LearnMoreLinks,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';

type SectionProps = PropsWithChildren<{
  title: string;
}>;

function Section({children, title}: SectionProps): React.JSX.Element {
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

function RecipePage({backgroundStyle, recipeName}) {
  const isDarkMode = useColorScheme() === 'dark';
  const filepath = 'recipes/' + recipeName + '.json';
    RNFS.readFile('/storage/emulated/0/DATA/data.json', 'ascii')
        .then((res) => {
            console.log(res);
            const d = JSON.parse(res);
            this.setState({ content: res, fruitType: d.type });
        })
        .catch((err) => {
            console.log(err.message, err.code);
        });

    let sections = [];
    for (let i = 0; i < 10; i++) {
        sections.push(<Section title={`Section ${i}`} key={i}>
        <Text>Section {i} content</Text>
        </Section>);
    }

  return <ScrollView
      contentInsetAdjustmentBehavior="automatic"
      style={backgroundStyle}>
    <Header />
    <View style={{ backgroundColor: isDarkMode ? Colors.black : Colors.white, }}>
      {sections}
    </View>
  </ScrollView>
}

function App(): React.JSX.Element {
  const isDarkMode = useColorScheme() === 'dark';

  const backgroundStyle = {
    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
  };

  return (
    <SafeAreaView style={backgroundStyle}>
      <StatusBar
        barStyle={isDarkMode ? 'light-content' : 'dark-content'}
        backgroundColor={backgroundStyle.backgroundColor}
      />
      <RecipePage backgroundStyle={backgroundStyle} recipeName=" Air Fryer Green Bean Fries "/>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
  },
  sectionTitle: {
    fontSize: 24,
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
});

export default App;
