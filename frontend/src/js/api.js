const API_BASE = "http://127.0.0.1:5000";

function getAccessToken(){
    return localStorage.getItem("access_token");
}

function getRefreshToken(){
    return localStorage.getItem("refresh_token");
}

function setTokens(access,refresh){
    localStorage.setItem("access_token",access);
    localStorage.setItem("refresh_token",refresh);
}

async function refreshAccessToken(){
    const refreshToken = getRefreshToken();
    const response = await fetch(API_BASE +"/auth/refresh",{
        method:"POST",headers:{"Authorization":"Brearer "+ refreshToken}
    });
    if(!response.ok){
       logout();
       throw new Error("Session Expired"); 
    }
    const data = await response.json();
    setTokens(data.access_token,data.refresh_token);
    return data.access_token;
}

function getAccountNumber(){
    return localStorage.getItem("account_number");
}

async function apiRequest(endpoint, method="GET", data=null){

    let token = getAccessToken();


    const headers = {
        "Content-Type": "application/json",
        "Authorization":"Brearer "+token
    }
    
    const response = await fetch(API_BASE + endpoint,{
        method: method,
        headers: headers,
        body: data ? JSON.stringify(data) : null
    });
    
    if(response.status === 401){
        console.log("Access Token expired. Refreshing...");
        token = await refreshAccessToken();
        headers[Authorization]="Brearer "+token;

        response = await fetch(API_BASE+endpoint,{
            method:method,headers:headers,body:data?JSON.stringify(data):null
        });
    }

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