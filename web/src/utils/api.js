const jwt = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjkxNDEzY2Y0ZmEwY2I5MmEzYzNmNWEwNTQ1MDkxMzJjNDc2NjA5MzciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxODQ0MjI5ODY3NTYtbW5lYXNzcWJoZDduc3JiZG10YmpjYnBlZDFrZmkyMzQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIxODQ0MjI5ODY3NTYtbW5lYXNzcWJoZDduc3JiZG10YmpjYnBlZDFrZmkyMzQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDUxMDU5MTk4NjM5MjMyNTgxMzUiLCJlbWFpbCI6ImpvaG4uYy5vcmFtQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYmYiOjE3MDQ1OTEyNjcsIm5hbWUiOiJKb2huIE9yYW0iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTGFkbmFXcm9IUVlmcF80UXRobkFLd1k2UklPT0RrSHB4UHZTVGtxdVkyTTBUUj1zOTYtYyIsImdpdmVuX25hbWUiOiJKb2huIiwiZmFtaWx5X25hbWUiOiJPcmFtIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE3MDQ1OTE1NjcsImV4cCI6MTcwNDU5NTE2NywianRpIjoiMjk5NjAxZjk0ODViN2IwYTlhZWQ4ZDc3MzE4MTQyZDRjZDRiZjIxNCJ9.a07EgRknuRgjDexMGzXeYoMUodd3pds0o7m05yKB1nxuuZ9POY81i1sIKxLLwyrRCqbSFIi7aX9GIhTR0hnf7s98VU6a_ncWjHjXaXEg83CzZ5CPzO3t7VpFDhO4vTJWo6_XWzHoJ2jfm-x2a_mzddNG6G_nMdD7n_4zlEe3Ikgsw-pDhvP93AMk43N_ZOHnSLg6uUJ_-iRWOC1PqgUP3PE9dlzgwfywZn8dy7firzCDLhvMsey0to2-LZ2RCenW_pPQnihSSNv00Etd-Hhfq3PaGkygrFXe8gMXJccTbBath-ls0_VqLA8qK_kzi_PgJehY5Fw6KnjkBKzYuHmt7Q"

function build_plan_id(year, week){
    return year + "_" + week;
}

function setJWT(jwt){
    localStorage.setItem("jwt", jwt)
}

function getJWT() {
    return localStorage.getItem("jwt")
}

function apiGetPlan(year, week){
    const url = `https://recipes-api.oram.ca/plans/${build_plan_id(year, week)}`
    return fetch(url, {
        method: 'GET',
        headers: {
            'Accept': "*/*",
            'Content-Type': 'application/json',
            'jwt': getJWT(),
        },
    }).then(response => response.json()).then(data => {
        return data
    })
}


async function apiAddRecipeToPlan(year, week, recipe_name){
    const url = `https://recipes-api.oram.ca/plan/${build_plan_id(year, week)}/recipe`
    return await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': "*/*",
            'Content-Type': 'application/json',
            'jwt': getJWT(),
        },
        body: JSON.stringify({
            "recipe_name": recipe_name
        })
    }).then(response => response.json()).then(data => {
        return data
    })
}

export {apiGetPlan, apiAddRecipeToPlan, setJWT}