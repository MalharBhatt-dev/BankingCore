(function () {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        document.documentElement.classList.add("dark");
    }
})();

document.addEventListener("DOMContentLoaded", function(){loadTransactions();});

async function loadTransactions(){
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/transactions`);
    renderTransactions(data.transactions);
}

function renderTransactions(transactions){
    const table = document.getElementById("transaction_table");
    table.innerHTML = "";
    transactions.forEach(txn => {
        const row = `
        <tr class="border-b hover:bg-gray-100 dark:hover:bg-gray-700 transition">
        <td class="p-3 text-left">${txn.transaction_type}</td>
        <td class="p-3 text-center">₹ ${txn.amount}</td>
        <td class="p-3 text-center">₹ ${txn.balance_after}</td>
        <td class="p-3 text-center">${txn.timestamp}</td>
        </tr>
        `;
        table.innerHTML += row;
    });
}

function toggleDarkMode() {
    document.documentElement.classList.toggle("dark");

    if (document.documentElement.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}