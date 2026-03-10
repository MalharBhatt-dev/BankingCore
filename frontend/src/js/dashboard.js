document.addEventListener("DOMContentLoaded", async function(){
    
    if(!getRefreshToken()){
        window.location.href="index.html";
        return;
    }
    if(!getAccountNumber()){
        window.location.href="index.html";
        return;
    }
    await loadAccountType();
    await loadAccountNumber();
    await loadBalance();
    await loadLastTransaction();
});

async function loadAccountNumber(){
    const account = getAccountNumber();
    document.getElementById("account_info").innerText = account;
}

async function loadAccountType(){
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}/account_type`);
    document.getElementById("account_type").innerText = data.account_type;
}

async function loadBalance(){
    const account = getAccountNumber();
    const data = await apiRequest(`/accounts/${account}`);
    document.getElementById("balance").innerText = data.balance;
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