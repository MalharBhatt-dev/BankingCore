async function login(event){

event.preventDefault();

const account_number = document.getElementById("account_number").value;
const pin = document.getElementById("pin_number").value;

const response = await fetch("http://127.0.0.1:5000/auth/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({
account_number: account_number,
pin: pin
})
});

const data = await response.json();

if(response.ok){

localStorage.setItem("access_token",data.access_token);
localStorage.setItem("refresh_token",data.refresh_token);
localStorage.setItem("account_number",account_number);

window.location.href="dashboard.html";

}else{
alert(data.error);
}
}