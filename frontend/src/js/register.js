const API_BASE = "http://127.0.0.1:5000";

async function registerAccount(){
    console.log("Register button clicked");
    const name = document.getElementById("name").value;
    const pin = document.getElementById("pin").value;
    const deposit = parseFloat(document.getElementById("deposit").value);
    if(!name || !pin || !deposit){
        alert("Please fill all fields");
        return;
    }
    try{
        const response = await fetch(API_BASE + "/accounts",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                name:name,pin:pin,initial_deposit:deposit
            })
        });
        console.log("Response status:", response.status);
        const data = await response.json();
        console.log("Response data:", data);
        if(response.status === 201){
            // alert("Account created successfully!\nAccount Number: " + data.account_number);
            console.log("redirecting to the login page.");
            window.location.href = "index.html";
        }else{
            alert(data.error || "Registration failed");
        }
    }catch(error){
        console.error(error);
        alert("Something went wrong");
    }
}

function toggleDarkMode() {
    const html = document.documentElement;
    html.classList.toggle("dark");

    const btn = document.getElementById("themeBtn");

    if (html.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
        btn.textContent = "☀️";
    } else {
        localStorage.setItem("theme", "light");
        btn.textContent = "🌙";
    }
}

// Load saved theme
window.onload = () => {
    const theme = localStorage.getItem("theme");
    const btn = document.getElementById("themeBtn");

    if (theme === "dark") {
        document.documentElement.classList.add("dark");
        btn.textContent = "☀️";
    }
};