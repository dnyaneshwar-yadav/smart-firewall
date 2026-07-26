// =====================================
// Smart Firewall Logs
// Optimized Version
// =====================================

let autoRefresh = true;
let logsLoading = false;
let logsInterval = null;


// =====================================
// Update Logs
// =====================================

async function updateLogs() {

    if (!autoRefresh)
        return;

    if (logsLoading)
        return;

    logsLoading = true;

    try {

        const response = await fetch("/logs-data");

        const data = await response.json();

        let html = "";

        data.logs.forEach(log => {

            const color =
                log[5] === "ALLOW"
                ? "#00ff99"
                : "#ff4d4d";

            html += `

            <tr>

                <td>${log[0]}</td>
                <td>${log[1]}</td>
                <td>${log[2]}</td>
                <td>${log[3]}</td>
                <td>${log[4]}</td>

                <td>

                    <span
                    style="
                    color:${color};
                    font-weight:bold;">

                        ${log[5]}

                    </span>

                </td>

                <td>${log[6]}</td>

            </tr>

            `;

        });

        document.getElementById("logs_table").innerHTML = html;

    }

    catch(error){

        console.error(error);

    }

    finally{

        logsLoading = false;

    }

}


// =====================================
// Search Detection
// =====================================

function checkRealtime(){

    const search =
        document.getElementById("search");

    const filter =
        document.getElementById("action");

    autoRefresh =
        search.value.trim() === "" &&
        filter.value === "ALL";

}


// =====================================
// Pause Refresh When Hidden
// =====================================

document.addEventListener("visibilitychange", () => {

    if(document.hidden){

        clearInterval(logsInterval);

    }

    else{

        updateLogs();

        logsInterval =
            setInterval(updateLogs, 3000);

    }

});


// =====================================
// Start
// =====================================

updateLogs();

logsInterval =
    setInterval(updateLogs, 3000);

setInterval(checkRealtime, 500);
