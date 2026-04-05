document.addEventListener("DOMContentLoaded",() => {
        const theme = localStorage.getItem("theme");
        if (theme === "dark") {
            document.documentElement.classList.add("dark");document.getElementById("themeBtn").textContent = "☀️";
        }
        loadRequests();
    });

window.onclick = function(e){
    const modal = document.getElementById("request_form_container");
    if(e.target === modal){
        closeLoginModal();
    }
}

function openRequestSubmitModal(){
    document.getElementById("request_form_container").classList.remove("hidden");
    document.getElementById("request_form_container").classList.add("flex");
}

function closeRequestSubmitModal(){
    document.getElementById("request_form_container").classList.add("hidden");
    document.getElementById("request_form_container").classList.remove("flex");
}

async function createRequest(){

    const selectedEmployee = document.querySelector('input[name="employee"]:checked');
    let employee_id = null
    employee_id = selectedEmployee ? selectedEmployee.value : null;
    const query_type = document.getElementById("query_type").value;
    const description = document.getElementById("description").value;

    if(!employee_id){
        alert("Please select employee");
        return;
    }
    if(!query_type){
        alert("Please select request type");
        return;
    }

    try{

        const data = await apiRequest(
            "/requests",
            "POST",
            {
                employee_id:employee_id,
                query_type: query_type,
                description: description
            }
        );

        alert(data.message);

    }
    catch(error){
        console.error("Request creation failed:",error);
    }

}

async function loadRequests(){

    try{

        const data = await apiRequest("/requests/my");
console.log(data);
if(!data.requests || data.requests.length === 0){
    table.innerHTML = `<tr>
    <td colspan="6" class="text-center py-10 text-gray-500">NO Requests found 📭
    </td>
    </tr>`;
    return;
}
        const table = document.getElementById("request_table");

        table.innerHTML="";
        let rows = "";
        data.requests.forEach(req => {

           rows += `
<tr class="border-b hover:bg-gray-100 dark:hover:bg-gray-700">

<td class="p-3 text-left">${req.query_type}</td>

<td class="p-3 text-center">${req.description}</td>

<td class="p-3 text-center">
<span class="px-2 py-1 text-xs rounded-full ${req.status == "APPROVED" ? "bg-green-100 text-green-600":
    req.status=="PENDING"? "bg-yellow-100 text-yellow-600" : "bg-red-100 text-red-500"
}">${req.status}</span>
</td>

<td class="p-3 text-center text-sm text-gray-500">
${new Date(req.created_at).toLocaleString("en-IN",{
    day:"2-digit",
    month:"short",
    year:"numeric",
    hour:"2-digit",
    minute:"2-digit"
})}
</td>

<td class="p-3 text-center">${req.employee_id}</td>

<td class="p-3 text-center">
${req.status === "APPROVED" ?
`<button onclick="openRequestForm(${req.id}, '${req.query_type}')"
class="bg-blue-900 text-white px-3 py-1 rounded-lg  hover:bg-blue-700 cursor-pointer transition">
Submit
</button>` : `<button onclick="openRequestForm(${req.id}, '${req.query_type}')"
class="bg-gray-200 dark:bg-gray-600 text-gray-500 text-white px-3 py-1 rounded-lg  cursor-not-allowed transition" disabled>
Submit
</button>`}
</td>

</tr>
`;

});
table.innerHTML = rows;

    }
    catch(error){
        console.error("Failed loading requests",error);
    }
}

let currentRequestId = null;

function openRequestForm(requestId, queryType){

currentRequestId = requestId;

openRequestSubmitModal();

const fields = document.getElementById("dynamic_form_fields");
const button = document.getElementById("dynamic_submit_button");

fields.innerHTML = "";

switch(queryType){

case "CHANGE_PIN":
    fields.innerHTML = `
    <input type="password" id="new_pin" placeholder=" " class="peer w-full bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-300 dark:border-gray-600 rounded-2xl px-5 pt-7 pb-3 focus:ring-2 focus:ring-cyan-500 focus:border-transparent outline-none transition-all font-medium">
    <label class="absolute left-5 top-2.5 text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2.5 peer-focus:text-xs peer-focus:uppercase peer-focus:tracking-wider peer-focus:text-cyan-500">New PIN</label>
    <button type="button" id="toggleIcon" onclick="togglePin()" class="absolute right-5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-xl">👁️</button>
    `;
    button.addEventListener(onclick,submitRequest('CHANGE_PIN'));
    
    break;

case "CHANGE_ACCOUNT_NAME":
    fields.innerHTML = `
    <input type="text" id="new_name" class="peer w-full bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white border border-gray-300 dark:border-gray-600 rounded-2xl px-5 pt-7 pb-3 focus:ring-2 focus:ring-cyan-500 focus:border-transparent outline-none transition-all font-medium">
    <label class="absolute left-5 top-2.5 text-gray-500 dark:text-gray-400 text-xs font-semibold uppercase tracking-wider transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:normal-case peer-placeholder-shown:tracking-normal peer-focus:top-2.5 peer-focus:text-xs peer-focus:uppercase peer-focus:tracking-wider peer-focus:text-cyan-500">New Account Name</label>
    `;
    button.addEventListener(onclick,submitRequest('CHANGE_ACCOUNT_NAME'));
    
    break;

//NOTE : //h future request query implementation :
// case "UPDATE_CONTACT":

// fields.innerHTML = `
// <label class="font-semibold">Phone</label>
// <input type="text" id="phone"
// class="border p-2 rounded w-full" placeholder="Enter new Phone number">

// <label>Email</label>
// <input type="email" id="email"
// class="border p-2 rounded w-full" placeholder="Enter new Email ID">

// <button
// onclick="submitRequest('UPDATE_CONTACT')"
// class="mt-4 bg-blue-900 text-white px-4 py-2 rounded-lg  hover:bg-blue-700 cursor-pointer transition">
// Submit
// </button>
// `;

// break;

// case "UPDATE_KYC":

// fields.innerHTML = `
// <label class="font-semibold">Address</label>
// <input type="text" id="address"
// class="border p-2 rounded w-full" placeholder="Enter new Address">

// <label class="font-semibold">ID Number</label>
// <input type="text" id="id_number"
// class="border p-2 rounded w-full" placeholder="Enter new ID number">

// <button
// onclick="submitRequest('UPDATE_KYC')"
// class="mt-4 bg-blue-900 text-white px-4 py-2 rounded-lg  hover:bg-blue-700 cursor-pointer transition">
// Submit
// </button>
// `;

// break;

// case "CLOSE_ACCOUNT":

// fields.innerHTML = `
// <label class="font-semibold">Reason</label>
// <textarea id="reason"
// class="border p-2 rounded w-full" placeholder="Enter your reason:"></textarea>

// <button
// onclick="submitRequest('CLOSE_ACCOUNT')"
// class="mt-4 bg-blue-900 text-white px-4 py-2 rounded-lg  hover:bg-blue-700 cursor-pointer transition">
// Submit
// </button>
// `;

// break;


}
}

async function submitRequest(query_type){
    document.getElementById("dynamic_submit_button").disabled = true;
    document.getElementById("btnText").textContent = "Logging in...";
    document.getElementById("spinner").classList.remove("hidden");
const fields = document.querySelectorAll("#dynamic_form_fields input, #dynamic_form_fields textarea");

const payload = {};

fields.forEach(field=>{
payload[field.id] = field.value;
});

try{

const data = await apiRequest(
`/requests/${currentRequestId}/submit`,
"POST",
payload
);
alert(data.message);
const result =await updateAccount(query_type,payload);
if (result  && result.success){
    const complete_data = await apiRequest(`/requests/${currentRequestId}/complete`,"GET");
    alert(complete_data.message);
}

location.reload();

}
catch(error){
console.error("Submission failed:",error);
}

}

async function updateAccount(query_type, payload){

    try {
        let endpoint = "";

        if(query_type === 'CHANGE_ACCOUNT_NAME'){
            endpoint = "/update/account_holder_name";
        }
        else if(query_type === 'CHANGE_PIN'){
            endpoint = "/update/pin_number";
        }
        else{
            return null;
        }

        const update_data = await apiRequest(endpoint, "POST", payload);
        alert(update_data.message);

        return update_data; // ✅ IMPORTANT

    } catch(error){
        console.log("Updation Failed:", error);
        return null;
    }
}


