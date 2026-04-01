const API_BASE = "http://127.0.0.1:5000";

function getAccountNumber(){
    return localStorage.getItem("account_number");
}

function getAccessToken(){
    return localStorage.getItem("access_token");
}

function getRefreshToken(){
    return localStorage.getItem("refresh_token");
}

function setToken(access,refresh){
    localStorage.setItem("access_token",access);
    localStorage.setItem("refresh_token",refresh);
}

async function refreshAccessToken(){

    const refreshToken = getRefreshToken();

    const response = await fetch(API_BASE + "/auth/refresh",{
        method:"POST",
        headers:{
            "Authorization": `Bearer ${refreshToken}`
        }
    });

    if(!response.ok){
        logout();
        throw new Error("Session expired");
    }

    const data = await response.json();

    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    if(accountNumber){
        localStorage.setItem("account_number",accountNumber);
    }

    return data.access_token;
}

async function apiRequest(endpoint, method="GET", data=null){
    let accessToken = getAccessToken();
    const refreshToken = getRefreshToken();

    if (!accessToken && refreshToken){
        console.log("No Access token -> refreshing...")
        accessToken = await refreshAccessToken();
    }

    let headers = {
        "Content-Type":"application/json",
    };

    if(accessToken){
        headers["Authorization"]=`Bearer ${accessToken}`;
    }

    let response = await fetch(API_BASE+endpoint,{method:method,headers:headers,
        body:data ? JSON.stringify(data) : null
    });

    //token expired
    if (response.status == 401 && refreshToken){
        console.log("Access Token expired -> refreshing...");

        accessToken = await refreshAccessToken();

        headers["Authorization"] = `Bearer ${accessToken}`;

        response = await fetch(API_BASE+endpoint,{method:method,headers:headers,body:data?JSON.stringify(data):null});
    }
        const result = await response.json();

        if(!response.ok){
            alert(response.error || "Something went wrong.");
            throw new Error(result.error);
        }
        return result;
    }


async function logout(){

    const refreshToken = getRefreshToken();
    if(refreshToken){
        await fetch(API_BASE+"/auth/logout",{method:"POST",headers:{"Authorization":"Bearer "+refreshToken}});
    }
    localStorage.clear();
    window.location.href="../../index.html";
}

// Toggle Theme
function toggleDarkMode() {
    const html = document.documentElement;
    const btn = document.getElementById("themeBtn");

    html.classList.toggle("light");
    html.classList.toggle("dark");

    const isDark = html.classList.contains("dark");

    localStorage.setItem("theme", isDark ? "dark" : "light");
    btn.textContent = isDark ? "☀️" : "🌙";
}