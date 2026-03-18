(function () {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        document.documentElement.classList.add("dark");
    }
})();

document.addEventListener("DOMContentLoaded", async function(){
    
    if(!getRefreshToken()){
        window.location.href="index.html";
        return;
    }
    if(!getAccountNumber()){
        window.location.href="index.html";
        return;
    }
    await loadAccountNumber();
    await loadBalance();
    await loadLastTransaction();
});

async function loadAccountNumber(){
    const account = getAccountNumber();
    document.getElementById("account_info").innerText = account;

}


async function loadBalance(){
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}`);
    document.getElementById("balance").innerText = data.balance;
    document.getElementById("balance_top").innerText = data.balance;
}

async function deposit(){
    const amount = document.getElementById("deposit_amount").value;
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/deposit`,"POST",{
        amount: amount
    });
    alert(data.message);
    loadBalance();
}

async function withdraw(){
    const amount = document.getElementById("withdraw_amount").value;
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/withdraw`,"POST",{
        amount: amount
    });
    alert(data.message);
    loadBalance();
}

async function loadLastTransaction(){
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/transactions`);
    const element = document.getElementById("last_transaction");
    if(!data.transactions || data.transactions.length === 0){
        element.innerText = "No transactions yet";
        return;
    }
    const last = data.transactions[0];
    element.innerText = `${last.transaction_type} ₹${last.amount}`;
}

function toggleDarkMode() {
    const html = document.documentElement;
    const btn = document.getElementById("themeBtn");

    html.classList.toggle("dark");

    if (html.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
        if (btn) btn.textContent = "☀️";
    } else {
        localStorage.setItem("theme", "light");
        if (btn) btn.textContent = "🌙";
    }
}