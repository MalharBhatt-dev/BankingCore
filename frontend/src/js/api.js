const API_BASE = "http://127.0.0.1:5000";

function getAccessToken(){
    return localStorage.getItem("access_token");
}

function getAccountNumber(){
    return localStorage.getItem("account_number");
}

async function apiRequest(endpoint, method="GET", data=null){
    const headers = {
        "Content-Type": "application/json"
    };
    
    const token = getAccessToken();
    if(token){
        headers["Authorization"] = "Bearer " + token;
    }
    
    const response = await fetch(API_BASE + endpoint,{
        method: method,
        headers: headers,
        body: data ? JSON.stringify(data) : null
    });
    
    const result = await response.json();
    if(!response.ok){
        alert(result.error || "Something went wrong");
        throw new Error(result.error);
    }
    return result;
}

function logout(){
    localStorage.clear();
    window.location.href="index.html";
}