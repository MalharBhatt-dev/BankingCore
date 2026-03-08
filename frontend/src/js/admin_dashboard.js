document.addEventListener("DOMContentLoaded",loadAdminStats);
async function loadAdminStats(){
    const data = await apiRequest("/admin/stats");
    document.getElementById("total_balance").innerText = data.total_balance;
    document.getElementById("total_accounts").innerText = data.total_accounts;
    document.getElementById("locked_accounts").innerText = data.locked_accounts;
    document.getElementById("last_lock_event").innerText = data.last_locked_account;
}