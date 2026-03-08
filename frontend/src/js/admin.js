async function adminLogin(event){
    event.preventDefault()

    const account_number = document.getElementById("admin_account_number").value;
    const pin = document.getElementById("admin_pin").value;

    const response = await fetch ("http://127.0.0.1:5000/auth/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({account_number:account_number,pin:pin})
    });
    const data = await response.json();

    if(response.ok){
        localStorage.setItem("access_token",data.access_token);
        localStorage.setItem("refresh_token",data.refresh_token);
        localStorage.setItem("account_number",account_number);

        window.location.href="admin_dashboard.html";
    }else{
        alert(data.error);
    }
}

async function unlockAccount(){
    
    const account_number = document.getElementById("account_number").value;
    const admin_key = document.getElementById("admin_key").value;

    if(!account_number || !admin_key){
        alert("Please fill all fields.");
        return;
    }

    try{
       const data = await apiRequest(`/admin/unlock`,"POST",{"account_number":account_number,"admin_key":admin_key});
       alert(data.message); 
    }
    catch(error){
        console.log("Unlock failed",error)
    }
}

function adminLogout(){
    localStorage.clear();
    window.location.href="admin.html";
}