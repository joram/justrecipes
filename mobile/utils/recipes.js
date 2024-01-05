function getRecipe(name) {
    const filepath = `custom/${name}.json`;
    return RNFS.readFileAssets(filepath, 'utf8').then((res) => {
        return JSON.parse(res)
    }).catch((err) => {
        console.log(err.message, err.code);

    })
}