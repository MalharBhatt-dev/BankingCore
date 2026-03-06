document.addEventListener("DOMContentLoaded", function(){

    const account = getAccountNumber();

    if(!account){
        window.location.href="index.html";
        return;
    }

    document.getElementById("account_info").innerText = account;

    loadBalance();

});

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