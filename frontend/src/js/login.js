// Apply theme on load
(function () {
    const theme = localStorage.getItem("theme");
    const btn = document.getElementById("themeBtn");

    if (theme === "dark") {
        document.documentElement.classList.add("dark");
        if (btn) btn.textContent = "☀️";
    }
})();

async function login(event) {
    event.preventDefault();

    const btn = document.getElementById("loginBtn");
    const text = document.getElementById("btnText");
    const spinner = document.getElementById("spinner");
    const errorMsg = document.getElementById("errorMsg");

    btn.disabled = true;
    text.textContent = "Logging in...";
    spinner.classList.remove("hidden");

    const account_number = document.getElementById("account_number").value;
    const pin = document.getElementById("pin_number").value;
    const rememberMe = document.getElementById("rememberMe").checked;

    try {
        const response = await fetch("http://127.0.0.1:5000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ account_number, pin })
        });

        const data = await response.json();

        if (response.ok) {
            if (rememberMe) {
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);
                localStorage.setItem("account_number", account_number);
            } else {
                sessionStorage.setItem("access_token", data.access_token);
                sessionStorage.setItem("refresh_token", data.refresh_token);
                sessionStorage.setItem("account_number", account_number);
            }

            window.location.href = "dashboard.html";
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
        btn.disabled = false;
        text.textContent = "Login";
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