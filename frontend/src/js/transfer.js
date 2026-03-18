(function () {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        document.documentElement.classList.add("dark");
    }
})();

document.addEventListener("DOMContentLoaded", function(){
    account = getAccountNumber();
    if(!account){
        window.location.href="index.html";
        return;
    }
    document.getElementById("sender_account_display").innerText = account;
});

async function transferMoney(){

    const from_account = getAccountNumber();
    const to_account = document.getElementById("to_account").value;
    const amount = document.getElementById("amount").value;

    if(!to_account || !amount){
        alert("Please fill all fields");
        return;
    }

    if(from_account==to_account){
        alert("Cannot transfer the Amount in the same account.")
        return;
    }
    try{

        const data = await apiRequest(
            `/accounts/${from_account}/transfer`,
            "POST",
            {
                to_account: to_account,
                amount:amount
            }
        );

        alert(data.message);

        // refresh page or transaction history
        window.location.reload();

    }
    catch(error){
        console.error("Transfer failed:", error);
    }
}

async function loadAccountNumber(){
    const account = getAccountNumber();
    document.getElementById("from_account").innerText = account;
}

function toggleDarkMode() {
    document.documentElement.classList.toggle("dark");

    // Save preference
    if (document.documentElement.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}