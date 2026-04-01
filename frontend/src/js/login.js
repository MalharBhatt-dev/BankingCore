// Apply theme on load
(function () {
    const theme = localStorage.getItem("theme");
    const btn = document.getElementById("themeBtn");

    if (theme === "dark") {
        document.documentElement.classList.add("dark");
        if (btn) btn.textContent = "☀️";
    }
})();

document.addEventListener("DOMContentLoaded",function(){
    const token = localStorage.getItem("access_token");
    const role = localStorage.getItem("role");

    if(token && role){
        document.body.innerHTML = `
        <div class="flex items-center justify-center h-screen">
            <div class="text-center">
                <p class="text-lg font-semibold">Redirecting ...</p>
                <div class="animate-spin mt-4">⏳</div>
            </div>
        </div>
        `;
        setTimeout(()=>{
        if(role === "admin"){
            window.location.href = "../frontend/src/admin_dashboard.html";
        } else if(role === "employee"){
            window.location.href = "../frontend/src/employee_dashboard.html";
        } else {
            window.location.href = "../frontend/src/dashboard.html";
        }
    },500); 
    }
});

window.onclick = function(e){
    const modal = document.getElementById("loginModal");
    if(e.target === modal){
        closeLoginModal();
    }
}

function openLoginModal(){
    document.getElementById("loginModal").classList.remove("hidden");
    document.getElementById("loginModal").classList.add("flex");
}

function closeLoginModal(){
    document.getElementById("loginModal").classList.add("hidden");
    document.getElementById("loginModal").classList.remove("flex");
}

let currentRole = "user";

function setRole(role){
    currentRole = role;

    //Reset button styles
    document.getElementById("role_user").classList.remove("bg-blue-900","text-white","dark:bg-blue-700");
    document.getElementById("role_employee").classList.remove("bg-blue-900","text-white","dark:bg-blue-700");
    document.getElementById("role_admin").classList.remove("bg-blue-900","text-white","dark:bg-blue-700");

    document.getElementById("role_user").classList.add("bg-gray-200","dark:bg-gray-700");
    document.getElementById("role_employee").classList.add("bg-gray-200","dark:bg-gray-700");
    document.getElementById("role_admin").classList.add("bg-gray-200","dark:bg-gray-700");

    //Activate Selected
    document.getElementById("role_"+role).classList.remove("bg-gray-200","dark:bg-gray-700");
    document.getElementById("role_"+ role).classList.add("bg-blue-900","text-white","dark:bg-blue-700");

    //Show/hide Admin key
    const adminKey = document.getElementById("admin_key_box");

    if (role === "admin"){
        adminKey.classList.remove("hidden");
    }else{
        adminKey.classList.add("hidden");
    }

}

async function login(event) {
    event.preventDefault();
    const errorMsg = document.getElementById("errorMsg");
    
    loginBtn.disabled = true;
    btnText.textContent = "Logging in...";
    spinner.classList.remove("hidden");

    const account_number = document.getElementById("account_number").value;
    const pin = document.getElementById("pin_number").value;
    const admin_key = document.getElementById("admin_key").value;
    const rememberMe = document.getElementById("rememberMe").checked;

    try {
        const response = await fetch("http://127.0.0.1:5000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                account_number:account_number,
                pin:pin,
                role:currentRole
             })
        });

        const data = await response.json();

        if (response.ok) {
            if (rememberMe) {
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);
                localStorage.setItem("account_number", account_number);
                localStorage.setItem("role",currentRole);

                const token = localStorage.getItem("access_token");
                const role = localStorage.getItem("role");
                if(token && role){
                    document.body.innerHTML = `
                        <div class="flex items-center justify-center h-screen">
                            <div class="text-center">
                                <p class="text-lg font-semibold">Redirecting ...</p>
                                <div class="animate-spin mt-4">⏳</div>
                            </div>
                        </div>
                    `;
                    setTimeout(()=>{
                        if(role === "admin"){
                            window.location.href = "../frontend/src/admin_dashboard.html";
                        } else if(role === "employee"){
                            window.location.href = "../frontend/src/employee_dashboard.html";
                        } else {
                            window.location.href = "../frontend/src/dashboard.html";
                        }
                    },500); 
                }
            } else {
                sessionStorage.setItem("access_token", data.access_token);
                sessionStorage.setItem("refresh_token", data.refresh_token);
                sessionStorage.setItem("account_number", account_number);
                sessionStorage.setItem("role", currentRole);
            }
            
        } else {
            errorMsg.textContent = data.error || "Invalid Credentials";
            errorMsg.classList.remove("hidden");
        }

    } catch (error) {
        console.error(error);

        const accountInput = document.getElementById("account_number");
        const pinInput = document.getElementById("pin_number");

        accountInput.classList.add("border-red-500");
        pinInput.classList.add("border-red-500");

        errorMsg.textContent = "Server error. Please try again.";
        errorMsg.classList.remove("hidden");

    } finally {
        loginBtn.disabled = false;
        btnText.textContent = "Login";
        spinner.classList.add("hidden");
    }
}

async function demoLogin(role){

    let account_number = "";
    let pin = "";
    let current_role = role;
    
    //Demo credentials
    if (role === "admin"){
        account_number = "1003";
        pin = "1234";
    }else if(role === "employee"){
        account_number = "1005";
        pin = "5555";
    }else{
        account_number = "1002";
        pin = "2345" ;
    }

    try{
        const response =  await fetch("http://127.0.0.1:5000/auth/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body: JSON.stringify({
                account_number:account_number,
                pin:pin,
                role:current_role
            })
        });

        const data = await response.json();

        if(response.ok){
            localStorage.setItem("access_token",data.access_token);
            localStorage.setItem("refresh_token",data.refresh_token);
            localStorage.setItem("account_number",account_number);
            localStorage.setItem("role",current_role);

            const token = localStorage.getItem("access_token");
            const role = localStorage.getItem("role");
                if(token && role){
                    document.body.innerHTML = `
                        <div class="flex items-center justify-center h-screen">
                            <div class="text-center">
                                <p class="text-lg font-semibold">Redirecting ...</p>
                                <div class="animate-spin mt-4">⏳</div>
                            </div>
                        </div>
                    `;
                    setTimeout(()=>{
                        if(role === "admin"){
                            window.location.href = "../frontend/src/admin_dashboard.html";
                        } else if(role === "employee"){
                            window.location.href = "../frontend/src/employee_dashboard.html";
                        } else {
                            window.location.href = "../frontend/src/dashboard.html";
                        }
                    },500); 
                }
        }
    }catch(error){
        console.log(error);
        
        const accountInput = document.getElementById("account_number");
        const pinInput = document.getElementById("pin_number");

        accountInput.classList.add("border-red-500");
        pinInput.classList.add("border-red-500");

        errorMsg.textContent = "Server error. Please try again.";
        errorMsg.classList.remove("hidden");
    } finally {
        loginBtn.disabled = false;
        btnText.textContent = "Login";
        spinner.classList.add("hidden");
    }
}

// Toggle PIN
function togglePin() {
    const pinInput = document.getElementById("pin_number");
    const icon = document.getElementById("toggleIcon");

    if (pinInput.type === "password") {
        pinInput.type = "text";
        icon.textContent = "🙈";
    } else {
        pinInput.type = "password";
        icon.textContent = "👁️";
    }
}

// Toggle Theme
function toggleDarkMode() {
    const html = document.documentElement;
    const btn = document.getElementById("themeBtn");

    html.classList.toggle("dark");

    const isDark = html.classList.contains("dark");

    localStorage.setItem("theme", isDark ? "dark" : "light");
    btn.textContent = isDark ? "☀️" : "🌙";
}