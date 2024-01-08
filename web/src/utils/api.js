
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
        mode: 'cors',
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

async function apiRemoveRecipeFromPlan(year, week, recipe_title){
    const url = `https://recipes-api.oram.ca/plan/${build_plan_id(year, week)}/recipe`
    return await fetch(url, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
            'Accept': "*/*",
            'Content-Type': 'application/json',
            'jwt': getJWT(),
        },
        body: JSON.stringify({
            "recipe_name": recipe_title
        })
    }).then(response => response.json()).then(data => {
        return data
    })

}

export {apiGetPlan, apiAddRecipeToPlan, apiRemoveRecipeFromPlan, setJWT}