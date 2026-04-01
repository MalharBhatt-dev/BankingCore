document.addEventListener("DOMContentLoaded", function () {
    loadAdminStats();
    loadLastSecurityEvent();
    loadSecurityEvents();
    loadLockedAccounts();
});
async function loadAdminStats() {
    const data = await apiRequest("/admin/stats");
    document.getElementById("total_balance").innerText = data.total_balance;
    document.getElementById("total_accounts").innerText = data.total_accounts;
    document.getElementById("locked_accounts").innerText = data.locked_accounts;
}

async function loadLastSecurityEvent() {
    const data = await apiRequest("/admin/events");
    const element = document.getElementById("last_lock_event");

    if (!data.events || data.events.lenght === 0) {
        element.innerText = "No Events yet";
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

async function loadSecurityEvents() {
    const data = await apiRequest("/admin/events");
    const table = document.getElementById("event_table");
    table.innerHTML = "";
    data.events.forEach(event => {
        const date = new Date(event.timestamp).toLocaleString("en-IN", {
            day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit"
        });
        const evtTagClass = event.event.includes("LOCK") ? "bg-rose-100 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-200 dark:border-rose-500/20" : "bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-500/20";

        const row = `
        <tr class="hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition duration-200">
        <td class="p-3 px-6 text-center font-mono text-zinc-900 dark:text-zinc-100">#${event.account_number}</td>
        <td class="p-3 px-6 text-center">
            <span class="px-2.5 py-1 text-xs rounded-full border ${evtTagClass}">${event.event}</span>
        </td>
        <td class="p-3 px-6 text-center text-zinc-900 dark:text-zinc-100 font-semibold">₹ ${event.balance}</td>
        <td class="p-3 px-6 text-center text-zinc-500 dark:text-zinc-400 text-xs">${date}</td>
        </tr>
        `;
        table.innerHTML += row;
    });
}

async function loadLockedAccounts() {
    const data = await apiRequest("/admin/locked-accounts");
    const table = document.getElementById("locked_accounts_table");
    table.innerHTML = "";
    data.accounts.forEach(acc => {

        const row = `
        <tr class="hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition duration-200">
        <td class="p-3 px-6 text-center font-mono text-zinc-900 dark:text-zinc-100">#${acc.account_number}</td>
        <td class="p-3 px-6 text-center font-medium text-zinc-900 dark:text-zinc-100">${acc.name}</td>
        <td class="p-3 px-6 text-center text-zinc-500 dark:text-zinc-400">${acc.failed_attempts}</td>
        <td class="p-3 px-6 text-center text-rose-600 dark:text-rose-400 font-semibold">Locked 🔒</td>
        <td class="p-3 px-6 text-center">
            <button onclick="openUnlockForm(${acc.account_number})" class="bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-100 hover:scale-105 active:scale-95 px-4 py-1.5 rounded-lg text-xs font-semibold cursor-pointer transition-all shadow-sm">Unlock</button>
        </td>
        </tr>
        `;

        table.innerHTML += row;

    });
}

function openUnlockForm(accountNumber) {
    const hide_table = document.getElementById("accounts_table")
    const formContainer = document.getElementById("unlock_form_container");
    const input = document.getElementById("account_number");
    hide_table.classList.add("hidden");
    formContainer.classList.remove("hidden");
    input.value = accountNumber;
}

async function unlockAccount() {

    const account_number = document.getElementById("account_number").value;
    const admin_key = document.getElementById("admin_key").value;

    if (!account_number || !admin_key) {
        alert("Please fill all fields.");
        return;
    }

    try {
        const data = await apiRequest(`/admin/unlock`, "POST", { "account_number": account_number, "admin_key": admin_key });
        const hide_table = document.getElementById("accounts_table")
        const formContainer = document.getElementById("unlock_form_container");
        hide_table.classList.remove("hidden");
        formContainer.classList.add("hidden");
        alert(data.message);
    }
    catch (error) {
        console.log("Unlock failed", error)
    }
}