document.addEventListener("DOMContentLoaded",loadRequests);

async function createRequest(){

    const query_type = document.getElementById("query_type").value;
    const description = document.getElementById("description").value;

    if(!query_type){
        alert("Please select request type");
        return;
    }

    try{

        const data = await apiRequest(
            "/requests",
            "POST",
            {
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
<tr class="border-b">

<td class="p-3">${req.query_type}</td>

<td class="p-3">${req.description}</td>

<td class="p-3">${req.status}</td>

<td class="p-3">

${req.status === "APPROVED" ?
`<button onclick="openRequestForm(${req.id}, '${req.query_type}')"
class="bg-blue-600 text-white px-3 py-1 rounded">
Submit
</button>` : ""}

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

const container = document.getElementById("request_form_container");
const fields = document.getElementById("dynamic_form_fields");

container.classList.remove("hidden");

fields.innerHTML = "";

switch(queryType){

case "CHANGE_PIN":

fields.innerHTML = `
<label>New PIN</label>
<input type="password" id="new_pin"
class="border p-2 w-full mb-3">
`;

break;

case "CHANGE_ACCOUNT_NAME":

fields.innerHTML = `
<label>New Account Name</label>
<input type="text" id="new_name"
class="border p-2 w-full mb-3">
`;

break;

case "UPDATE_CONTACT":

fields.innerHTML = `
<label>Phone</label>
<input type="text" id="phone"
class="border p-2 w-full mb-3">

<label>Email</label>
<input type="email" id="email"
class="border p-2 w-full mb-3">
`;

break;

case "UPDATE_KYC":

fields.innerHTML = `
<label>Address</label>
<input type="text" id="address"
class="border p-2 w-full mb-3">

<label>ID Number</label>
<input type="text" id="id_number"
class="border p-2 w-full mb-3">
`;

break;

case "CLOSE_ACCOUNT":

fields.innerHTML = `
<label>Reason</label>
<textarea id="reason"
class="border p-2 w-full"></textarea>
`;

break;

case "ACCOUNT_UNLOCK_REQUEST":

fields.innerHTML = `
<label>Reason</label>
<textarea id="unlock_reason"
class="border p-2 w-full"></textarea>
`;

break;

}

}