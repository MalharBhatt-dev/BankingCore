document.addEventListener("DOMContentLoaded",loadRequestLogs);

async function loadRequestLogs(){
    try{
        const table = document.getElementById("request_logs_table");
        const data = await apiRequest("/requests/user");

        table.innerHTML = "";
        data.requests.forEach(req => {
            const parsed = JSON.parse(req.submission_data);
            const key = Object.keys(parsed)[0];
            const row = `
            <tr class="border-b">
            <td class="p-3">${req.request_id}</td>
            <td class="p-3">${req.account_number}</td>
            <td class="p-3">${key}</td>
            <td class="p-3">${req.submitted_at}</td>
            </tr>
            `;
            table.innerHTML += row;
        });
    }catch(error){
        console.log("Failed loading requests",error);
    }
}