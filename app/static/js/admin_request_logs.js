document.addEventListener("DOMContentLoaded",loadRequestLogs);

async function loadRequestLogs(){
    try{
        const table = document.getElementById("request_logs_table");
        const data = await apiRequest("/requests/user");

        table.innerHTML = "";
        data.requests.forEach(req => {
            const parsed = JSON.parse(req.submission_data);
            const key = Object.keys(parsed)[0];
            const dateStr = new Date(req.submitted_at).toLocaleString("en-IN", {
                day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit"
            });
            const tagMap = {
                "checkbook_type": "Checkbook",
                "card_type": "Debit Card",
                "kyc_document": "KYC Update",
            };
            const reqType = tagMap[key] || key;
            const badgeClass = "bg-violet-100 dark:bg-violet-500/10 text-violet-600 dark:text-violet-400 border border-violet-200 dark:border-violet-500/20";
            
            const row = `
            <tr class="hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition duration-200">
            <td class="p-3 px-6 text-center font-mono text-zinc-500 dark:text-zinc-400 text-xs">#${req.request_id}</td>
            <td class="p-3 px-6 text-center font-mono text-zinc-900 dark:text-zinc-100 font-semibold">#${req.account_number}</td>
            <td class="p-3 px-6 text-center">
                <span class="px-3 py-1 text-xs rounded-full inline-block font-semibold ${badgeClass}">${reqType}</span>
            </td>
            <td class="p-3 px-6 text-center text-zinc-500 dark:text-zinc-400 text-xs tracking-wider">${dateStr !== "Invalid Date" ? dateStr : req.submitted_at}</td>
            </tr>
            `;
            table.innerHTML += row;
        });
    }catch(error){
        console.log("Failed loading requests",error);
    }
}