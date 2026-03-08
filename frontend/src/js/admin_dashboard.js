document.addEventListener("DOMContentLoaded",function(){
    loadAdminStats();
    loadLastSecurityEvent();
    loadSecurityEvents();
    loadLockedAccounts();
    });
async function loadAdminStats(){
    const data = await apiRequest("/admin/stats");
    document.getElementById("total_balance").innerText = data.total_balance;
    document.getElementById("total_accounts").innerText = data.total_accounts;
    document.getElementById("locked_accounts").innerText = data.locked_accounts;
}

async function loadLastSecurityEvent(){
    const data = await apiRequest("/admin/events");
    const element = document.getElementById("last_lock_event");
    
    if(!data.events || data.events.lenght === 0){
        element.innerText="No Events yet";
        return;
    }
    
    const last = data.events[0];

    const date = new Date(last.timestamp);

    const formattedDate = date.toLocaleString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });

    const eventText =
        last.event === "ACCOUNT_UNLOCKED"
        ? `🔓 Unlocked Account #${last.account_number}`
        : `🔒 Locked Account #${last.account_number}`;

    element.innerText =
        `${eventText}\n${formattedDate}`;
  
}

async function loadSecurityEvents(){
    const data = await apiRequest("/admin/events");
    const table = document.getElementById("event_table");
    table.innerHTML = "";
    data.events.forEach(event => {
          const row = `
        <tr class="border-b hover:bg-gray-100">

        <td class="p-3">${event.account_number}</td>

        <td class="p-3">${event.event}</td>

        <td class="p-3">₹ ${event.balance}</td>

        <td class="p-3">${event.timestamp}</td>

        </tr>
        `;
        table.innerHTML += row;
    });
}

async function loadLockedAccounts(){
    const data = await apiRequest("/admin/locked-accounts");
    const table = document.getElementById("locked_accounts_table");
    table.innerHTML = "";
    data.accounts.forEach(acc => {

        const row = `
        <tr class="border-b hover:bg-gray-100">

        <td class="p-3">${acc.account_number}</td>

        <td class="p-3">${acc.name}</td>

        <td class="p-3">${acc.failed_attempts}</td>

        <td class="p-3 text-red-600 font-semibold">Locked</td>

        <td class="p-3">

            <button
            onclick="openUnlockForm(${acc.account_number})"
            class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">

            Unlock

            </button>

        </td>

        </tr>
        `;

        table.innerHTML += row;

    });
}

function openUnlockForm(accountNumber){
    const hide_table = document.getElementById("accounts_table")
    const formContainer = document.getElementById("unlock_form_container");
    const input = document.getElementById("account_number");
    hide_table.classList.add("hidden");
    formContainer.classList.remove("hidden");
    input.value = accountNumber;
}

