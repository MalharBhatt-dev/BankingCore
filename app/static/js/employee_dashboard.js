document.addEventListener("DOMContentLoaded",loadRequests);

async function loadRequests(){

    try{

        const data = await apiRequest("/employee/requests");

        const table = document.getElementById("request_table");

        table.innerHTML = "";

        data.requests.forEach(req => {

            const row = `
            <tr class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition duration-200">
            <td class="p-3 px-6 text-center text-slate-900 dark:text-white font-medium">#${req.id}</td>
            <td class="p-3 px-6 text-center text-slate-600 dark:text-slate-300 font-mono">${req.account_number}</td>
            <td class="p-3 px-6 text-center">
                <span class="px-2.5 py-1 text-xs rounded-full bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-600 hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors">${req.query_type}</span>
            </td>
            <td class="p-3 px-6 text-left max-w-xs truncate" title="${req.description}">${req.description}</td>
            <td class="p-3 px-6 text-center">
                <div class="flex items-center justify-center gap-2">
                    <button onclick="approveRequest(${req.id})" class="bg-emerald-50 text-emerald-600 hover:bg-emerald-100 hover:scale-105 active:scale-95 dark:bg-emerald-900/30 dark:text-emerald-400 dark:hover:bg-emerald-900/50 border border-emerald-200 dark:border-emerald-800 px-3 py-1.5 rounded-lg text-xs font-semibold cursor-pointer transition-all">Approve</button>
                    <button onclick="rejectRequest(${req.id})" class="bg-red-50 text-red-600 hover:bg-red-100 hover:scale-105 active:scale-95 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50 border border-red-200 dark:border-red-800 px-3 py-1.5 rounded-lg text-xs font-semibold cursor-pointer transition-all">Reject</button>
                </div>
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