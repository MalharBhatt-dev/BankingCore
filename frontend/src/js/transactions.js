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
        <tr class="border-b hover:bg-gray-100">
        <td class="p-3">${txn.transaction_type}</td>
        <td class="p-3">₹ ${txn.amount}</td>
        <td class="p-3">₹ ${txn.balance_after}</td>
        <td class="p-3">${txn.timestamp}</td>
        </tr>
        `;
        table.innerHTML += row;
    });
}