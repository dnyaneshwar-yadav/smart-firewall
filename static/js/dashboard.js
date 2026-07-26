// =====================================
// Smart Firewall Dashboard
// Optimized Version
// =====================================

let dashboardInterval = null;
let dashboardLoading = false;


// =====================================
// Update Dashboard
// =====================================

async function updateDashboard() {

    if (dashboardLoading)
        return;

    dashboardLoading = true;

    try {

        const response = await fetch("/dashboard-data");

        const data = await response.json();

        document.getElementById("total_packets").innerText =
            data.total_packets;

        document.getElementById("allowed_packets").innerText =
            data.allowed_packets;

        document.getElementById("blocked_packets").innerText =
            data.blocked_packets;

        document.getElementById("total_rules").innerText =
            data.total_rules;

        let html = "";

        data.recent_logs.forEach(log => {

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
                    <span style="color:${color};font-weight:bold;">
                        ${log[5]}
                    </span>
                </td>
                <td>${log[6]}</td>
            </tr>
            `;

        });

        document.getElementById("recent_logs").innerHTML = html;

    }

    catch (error) {

        console.error(error);

    }

    finally {

        dashboardLoading = false;

    }

}


// =====================================
// Pause Refresh when Tab Hidden
// =====================================

document.addEventListener("visibilitychange", () => {

    if (document.hidden) {

        clearInterval(dashboardInterval);

    }

    else {

        updateDashboard();

        dashboardInterval =
            setInterval(updateDashboard, 2000);

    }

});


// =====================================
// Start
// =====================================

updateDashboard();

dashboardInterval =
    setInterval(updateDashboard, 2000);
