document.addEventListener("DOMContentLoaded",loadRequests);

async function loadRequests(){

    try{

        const data = await apiRequest("/employee/requests");

        const table = document.getElementById("request_table");

        table.innerHTML = "";

        data.requests.forEach(req => {

            const row = `
            <tr class="border-b hover:bg-gray-100">

            <td class="p-3">${req.id}</td>

            <td class="p-3">${req.account_number}</td>

            <td class="p-3">${req.query_type}</td>

            <td class="p-3">${req.description}</td>

            <td class="p-3 flex gap-2">

            <button
            onclick="approveRequest(${req.id})"
            class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">
            Approve
            </button>

            <button
            onclick="rejectRequest(${req.id})"
            class="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700">
            Reject
            </button>

            </td>

            </tr>
            `;

            table.innerHTML += row;

        });

    }
    catch(error){
        console.error("Failed loading requests:",error);
    }

}

async function approveRequest(id){

    try{

        const data = await apiRequest(
            `/employee/requests/${id}/approve`,
            "POST"
        );

        alert(data.message);

        loadRequests();

    }
    catch(error){
        console.error("Approval failed",error);
    }

}

async function rejectRequest(id){

    try{

        const data = await apiRequest(
            `/employee/requests/${id}/reject`,
            "POST"
        );

        alert(data.message);

        loadRequests();

    }
    catch(error){
        console.error("Reject failed",error);
    }

}