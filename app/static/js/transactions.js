(function () {
    const theme = localStorage.getItem("theme");
    if (theme === "dark") {
        document.documentElement.classList.add("dark");
    }
})();

document.addEventListener("DOMContentLoaded", function () { loadTransactions(); });

async function loadTransactions() {
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/transactions`);
    renderTransactions(data.transactions);
}

function renderTransactions(transactions) {
    const table = document.getElementById("transaction_table");
    table.innerHTML = "";

    if (!transactions || transactions.length === 0) {
        table.innerHTML = `
        <tr>
        <td colspan="4" class="text-center py-10 text-gray-500 dark:text-gray-300"> No transactions yet 📭
        </tr>
        `;
        return;
    }

    transactions.forEach(txn => {
        let typeClass = "";
        let amountClass = "";

        if (txn.transaction_type.includes("DEPOSIT")) {
            typeClass = "bg-green-100 text-green-600";
            amountClass = "text-green-600 font-semibold";
        }
        else if (txn.transaction_type.includes("WITHDRAW")) {
            typeClass = "bg-red-100 text-red-500";
            amountClass = "text-red-500 font-semibold";
        }
        else {
            typeClass = "bg-blue-100 text-blue-500";
            amountClass = "text-blue-500 font-semibold";
        }

        const formattedDate = new Date(txn.timestamp).toLocaleString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });

        const row = `
        <tr class="hover:bg-gray-50 dark:hover:bg-gray-700 transition duration-200 cursor-pointer">

        <td class="p-3">
            <span class="px-2 py-1 text-xs rounded-full ${typeClass}">
            ${txn.transaction_type}
            </span>
        </td>

        <td class="p-3 text-center ${amountClass}">
        ₹ ${txn.amount}
        </td>

        <td class="p-3 text-center text-gray-700 dark:text-gray-300">
        ₹ ${txn.balance_after}
        </td>

        <td class="p-3 text-center text-sm text-gray-500 dark:text-gray-400">
        ${formattedDate}
        </td>
        
        </tr>
        `;
        setTimeout(() => { table.innerHTML += row; }, 50);
    });
}