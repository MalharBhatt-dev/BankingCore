document.addEventListener("DOMContentLoaded",loadRequests);

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

        const table = document.getElementById("request_table");

        table.innerHTML="";

        data.requests.forEach(req => {

           const row = `
<tr class="border-b hover:bg-gray-100">

<td class="p-3 text-left">${req.query_type}</td>

<td class="p-3 text-center">${req.description}</td>

<td class="p-3 text-center">${req.status}</td>

<td class="p-3 text-center">${req.created_at}</td>

<td class="p-3 text-center">${req.employee_id}</td>

<td class="p-3 text-center">
${req.status === "APPROVED" ?
`<button onclick="openRequestForm(${req.id}, '${req.query_type}')"
class="bg-blue-900 text-white px-3 py-1 rounded-lg  hover:bg-blue-700 cursor-pointer transition">
Submit
</button>` : `<button onclick="openRequestForm(${req.id}, '${req.query_type}')"
class="bg-gray-300 text-white px-3 py-1 rounded-lg  cursor-pointer transition" disabled>
Submit
</button>`}
</td>

</tr>
`;

            table.innerHTML += row;

        });

    }
    catch(error){
        console.error("Failed loading requests",error);
    }
}

let currentRequestId = null;

function openRequestForm(requestId, queryType){

currentRequestId = requestId;

const table = document.getElementById("dynamic_table");
const container = document.getElementById("request_form_container");
const fields = document.getElementById("dynamic_form_fields");

table.classList.add("hidden");
container.classList.remove("hidden");

fields.innerHTML = "";

switch(queryType){

case "CHANGE_PIN":

fields.innerHTML = `
<label class="font-semibold">New PIN</label>
<input type="password" id="new_pin"
class="border p-2 rounded w-full" placeholder="Enter new PIN number">
<button
onclick="submitRequest('CHANGE_PIN')"
class="mt-4 bg-blue-900 text-white px-4 py-2 rounded-lg  hover:bg-blue-700 cursor-pointer transition">
Submit
</button>
`;

break;

case "CHANGE_ACCOUNT_NAME":

fields.innerHTML = `
<label class="font-semibold>New Account Name</label>
<input type="text" id="new_name"
class="border p-2 rounded w-full" placeholder="Enter new PIN number" placeholder="Enter the Account Holder Name">
<button
onclick="submitRequest('CHANGE_ACCOUNT_NAME')"
class="mt-4 bg-blue-900 text-white px-4 py-2 rounded-lg  hover:bg-blue-700 cursor-pointer transition">
Submit
</button>
`;

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

const fields = document
.querySelectorAll("#dynamic_form_fields input, #dynamic_form_fields textarea");

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
result = updateAccount(query_type,payload);
if (result["message"] == True){
    const complete_data = await apiRequest(`/requests/${currentRequestId}/complete`,"GET");
    alert(complete_data.message);
}

location.reload();

}
catch(error){
console.error("Submission failed:",error);
}

}

async function updateAccount(query_type,payload){
if(query_type == 'CHANGE_ACCOUNT_NAME'){
    try {
        const update_data = await apiRequest(
            `/update/account_holder_name`,"POST",payload
            
        );
        alert(update_data.message);
    }
    catch(error){
        console.log("Updation Failed:",error);
    }
}
else if(query_type == 'CHANGE_PIN'){
    try {
        const update_data = await apiRequest(
            `/update/pin_number`,"POST",payload
            
        );
        alert(update_data.message);
    }
    catch(error){
        console.log("Updation Failed:",error);
    }
}
//NOTE : //h future request query implementation :
// else if(query_type == 'UPDATE_CONTACT'){
//     try {
//         const update_data = await apiRequest(
//             `/update/contact`,"POST",payload
            
//         );
//         alert(update_data.message);
//     }
//     catch(error){
//         console.log("Updation Failed:",error);
//     }
// }
// else if(query_type == 'CLOSE_ACCOUNT'){
//     try {
//         const update_data = await apiRequest(
//             `/update/account_close`,"POST",payload
            
//         );
//         alert(update_data.message);
//     }
//     catch(error){
//         console.log("Updation Failed:",error);
//     }
// }

}