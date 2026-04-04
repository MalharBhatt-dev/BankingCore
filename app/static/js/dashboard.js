(function () {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        document.documentElement.classList.add("dark");
    }
})();

document.addEventListener("DOMContentLoaded", async function () {

    if (!getRefreshToken()) {
        window.location.href = "index.html";
        return;
    }
    if (!getAccountNumber()) {
        window.location.href = "index.html";
        return;
    }
    await loadLastTransaction();
    await loadAccountNumber();
    await loadBalance();
});

async function loadAccountNumber() {
    const account = getAccountNumber();
    document.getElementById("account_info").innerText = account;

}


async function loadBalance() {
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}`);
    document.getElementById("balance").innerText = data.balance;
    document.getElementById("balance_top").innerText = data.balance;
}

async function deposit() {
    const amount = document.getElementById("deposit_amount").value;
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/deposit`, "POST", {
        amount: amount
    });
    alert(data.message);
    loadBalance();
}

async function withdraw() {
    const amount = document.getElementById("withdraw_amount").value;
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/withdraw`, "POST", {
        amount: amount
    });
    alert(data.message);
    loadBalance();
}

async function loadLastTransaction() {
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/transactions`);
    const element = document.getElementById("last_transaction");
    if (!data.transactions || data.transactions.length === 0) {
        element.innerHTML = `
        <span class="text-gray-500">No transactions yet 📭</span>`;
        return;
    }

    const last = data.transactions[0];
    console.log(last);

    let color = "";
    let bg = "";
    let icon = "";

    if (last.transaction_type.includes("DEPOSIT")) {
        color = "text-green-600";
        bg = "bg-green-100";
        icon = "💰";
    }
    else if (last.transaction_type.includes("WITHDRAW")) {
        color = "text-red-500";
        bg = "bg-red-100";
        icon = "💸";
    }
    else {
        color = "text-blue-500";
        bg = "bg-blue-100";
        icon = "🔄";
    }

    const date = new Date(last.timestamp).toLocaleString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        day: "2-digit",
        month: "short",
        year: "numeric"
    });

    element.innerHTML = `
    <div class="flex items-center justify-between">
    
    <!--LEFT-->
    <div class="flex flex-col">
    <span class="text-sm text-gray-500 dark:text-gray-400">
    ${last.transaction_type}
    </span>
    <span class="text-xs text-gray-400">
    ${date}
    </span>
    </div>

    <!--Right-->
    <div class="text-right">
    <span class="px-2 py-1 text-xs rounded-full ${bg}">
    ${icon}
    </span>
    <p class="text-lg font-bold ${color}">₹ ${last.amount}
    </p>
    </div>
    </div> 
    `;
}
