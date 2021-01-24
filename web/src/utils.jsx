function call_api(path, callback){
    let host = "https://recipes.oram.ca"
    if(window.location.hostname==="localhost")
      host = "http://localhost:5000"
    let url = `${host}${path}`
    console.log(url)
    fetch(url)
        .then(res => res.json())
        .then(response => {
            callback(response)
        })
}

export default call_api