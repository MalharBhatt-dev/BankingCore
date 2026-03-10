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
            <tr class="border-b hover:bg-gray-100">
            <td class="p-3">${req.query_type}</td>
            <td class="p-3">${req.description}</td>
            <td class="p-3">${req.status}</td>
            <td class="p-3">${req.created_at}</td>
            </tr>
            `;

            table.innerHTML += row;

        });

    }
    catch(error){
        console.error("Failed loading requests",error);
    }
}